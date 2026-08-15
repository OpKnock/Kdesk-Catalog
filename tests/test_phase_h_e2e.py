"""Phase H: end-to-end tests + real subagent delegation."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kdesk.adapters import AdapterRegistry  # noqa: E402
from kdesk.adapters.contract import ClaudeCodeAdapter  # noqa: E402
from kdesk.doctor import Doctor  # noqa: E402
from kdesk.execution import ToolResult  # noqa: E402
from kdesk.installer import Installer  # noqa: E402
from kdesk.registry import Catalog  # noqa: E402
from kdesk.runtime import (  # noqa: E402
    EventBus, Node, RuntimeRun, RuntimeStore, RunState, WorkflowRuntime)


@pytest.fixture
def emission_root(tmp_path):
    return tmp_path / "root"


@pytest.fixture
def proj(tmp_path):
    return tmp_path / "proj"


@pytest.fixture
def registry(emission_root):
    reg = AdapterRegistry(emission_root)
    out = emission_root / "platform-agents" / "cursor"
    out.mkdir(parents=True)
    (out / "code-review.mdc").write_text(
        "---\ndescription: review\n---\nReview all PRs.\n", encoding="utf-8")
    (out / "accessibility.mdc").write_text(
        "---\ndescription: a11y\n---\nRun a11y audits.\n", encoding="utf-8")
    return reg


# ------------------------------------------------- emission -> install chain
def test_e2e_emission_install_doctor_drift_uninstall(registry, proj):
    installer = Installer(registry, base=proj)
    result = installer.install("cursor", target="project", base=proj)
    assert result["results"][0]["copied"] == 2
    assert (proj / ".cursor" / "rules" / "code-review.mdc").is_file()

    doctor = Doctor(registry, base=proj)
    check = doctor.check("cursor")
    assert check["status"] == "OK"
    assert check["scanned_files"] == 2

    assert installer.drift("cursor", base=proj)["clean"] is True

    (proj / ".cursor" / "rules" / "accessibility.mdc").write_text(
        "tampered", encoding="utf-8")
    drift = installer.drift("cursor", base=proj)
    assert drift["clean"] is False
    assert ".cursor/rules/accessibility.mdc" in drift["platforms"]["cursor"]["modified"]

    installer.uninstall("cursor", base=proj)
    assert not (proj / ".cursor" / "rules").exists()
    assert installer.status(base=proj)["installs"] == 0


# ------------------------------------------------- real catalog -> runtime
def _write_universal(root: Path) -> None:
    agent = root / "web" / "agent" / "reviewer.yaml"
    agent.parent.mkdir(parents=True)
    agent.write_text(
        "name: reviewer\ndisplay_name: Code Reviewer\ndescription: Reviews "
        "diffs for bugs and style.\nplatforms:\n  claude_code:\n    "
        "tools: [read, grep]\n", encoding="utf-8")
    skill = root / "web" / "skill" / "check.yaml"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "name: check\ndisplay_name: Check\ndescription: Runs checks.\n"
        "platforms:\n  claude_code:\n    prompts: [do it]\n",
        encoding="utf-8")


def test_e2e_catalog_workflow_runtime_persisted(tmp_path):
    universal = tmp_path / "universal-agents"
    _write_universal(universal)
    catalog = Catalog(universal)
    assert catalog.get_agent("reviewer") is not None
    assert catalog.get_skill("check") is not None

    runtime = WorkflowRuntime(catalog)
    run = runtime.create("e2e-flow", [
        Node("in", "input", config={"key": "subject", "value": "pr-1"}),
        Node("agent", "agent", config={"agent": "reviewer"},
             depends_on=["in"]),
        Node("out", "output", config={"key": "subject"},
             depends_on=["agent"]),
    ], inputs={})
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.outputs["subject"] == "pr-1"
    assert run.nodes["agent"].result["mode"] == "delegate"

    store = RuntimeStore(tmp_path / "runs")
    path = store.save(run)
    assert path.is_file()
    restored = store.load(run.run_id, EventBus())
    assert restored.state == RunState.COMPLETED
    assert restored.outputs["subject"] == "pr-1"
    assert restored.nodes["agent"].result["mode"] == "delegate"


# ------------------------------------------------- approval + retry gates
def test_e2e_approval_gate_blocks_then_continues(tmp_path):
    runtime = WorkflowRuntime(Catalog.__new__(Catalog))
    run = runtime.create("gate", [
        Node("a", "approval", config={"reason": "destructive"},
             depends_on=[]),
        Node("b", "notify", config={"message": "done"}, depends_on=["a"]),
    ])
    run.start()
    assert run.state == RunState.WAITING_FOR_APPROVAL
    run.approve("a", note="ok")
    assert run.state == RunState.COMPLETED
    assert run.nodes["b"].result["message"] == "done"


def test_e2e_validation_retry_then_fail(tmp_path):
    runtime = WorkflowRuntime(Catalog.__new__(Catalog))
    run = runtime.create("validate-fail", [
        Node("v", "validate", config={
            "checks": ["variables['x'] == 1"],
            "max_attempts": 1},
             max_attempts=1),
    ], inputs={"x": 2})
    run.start()
    assert run.state == RunState.FAILED
    assert "validation failed" in run.nodes["v"].error


# --------------------------------------------------- subagent delegation
@pytest.fixture
def fake_claude(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    argv_log = tmp_path / "argv.txt"
    csc = (Path(os.environ.get("WINDIR", r"C:\Windows")) /
           "Microsoft.NET" / "Framework64" / "v4.0.30319" / "csc.exe")
    if not csc.is_file():
        pytest.skip("csc.exe not available to build the claude shim")
    shim_cs = bin_dir / "shim.cs"
    shim_cs.write_text(
        "using System;\n"
        "using System.IO;\n"
        "class Shim {\n"
        f"  static int Main(string[] args) {{\n"
        f"    File.WriteAllText(@\"{argv_log}\", string.Join(\"|\", args));\n"
        "    Console.WriteLine(\"delegated-ok\");\n"
        "    return 0;\n"
        "  }\n"
        "}\n", encoding="utf-8")
    subprocess.run([str(csc), "/nologo", "/target:exe",
                    f"/out:{bin_dir / 'claude.exe'}", str(shim_cs)],
                   check=True, capture_output=True)
    monkeypatch.setenv("PATH", str(bin_dir) + os.pathsep + os.environ["PATH"])
    return argv_log


def test_e2e_subagent_delegation_via_cli(tmp_path, fake_claude):
    adapter = ClaudeCodeAdapter(project_root=tmp_path, home=tmp_path)
    assert adapter.detect() is True
    result = adapter.invoke_subagent("reviewer", "review this diff")
    assert result.success is True
    assert "delegated-ok" in result.stdout
    args = fake_claude.read_text(encoding="utf-8").strip()
    assert "review this diff" in args
    assert "--agent" in args
    assert "reviewer" in args


def test_e2e_subagent_honest_failure_without_cli(tmp_path):
    adapter = ClaudeCodeAdapter(project_root=tmp_path, home=tmp_path)
    assert adapter.detect() is False
    result = adapter.invoke_subagent("reviewer", "review this diff")
    assert result.success is False
    assert "not installed" in result.error
    assert isinstance(result, ToolResult)