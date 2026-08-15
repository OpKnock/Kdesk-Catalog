"""kdesk unit tests: CLI end-to-end (subprocess, no network)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

CLI = str(Path(__file__).resolve().parents[1] / "kdesk" / "cli.py")
REPO = str(Path(__file__).resolve().parents[1])


def _run(args, cwd):
    import os

    env = dict(os.environ)
    env["PYTHONPATH"] = REPO + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, CLI] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
        timeout=120,
    )


@pytest.fixture()
def mini_repo(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    (base / "devops" / "skill").mkdir(parents=True)
    (base / "devops" / "agent" / "agent-a.yaml").write_text(
        """
name: agent-a
category: devops
description: Agent A with capabilities for helm and kubectl operations.
version: "1.0.0"
type: agent
skills: ["skill-1"]
capabilities:
  - name: run
    description: Run.
    commands: ["helm lint ./chart"]
""",
        encoding="utf-8",
    )
    (base / "devops" / "skill" / "skill-1.yaml").write_text(
        """
name: skill-1
category: devops
description: Skill one for helm linting workflows.
version: "1.0.0"
type: skill
""",
        encoding="utf-8",
    )
    (tmp_path / "workflows").mkdir()
    (tmp_path / "workflows" / "wf-good.workflow.json").write_text(
        json.dumps(
            {
                "id": "wf-good",
                "name": "Good",
                "agent": "agent-a",
                "steps": [
                    {"id": "s1", "type": "skill", "skill": "skill-1"},
                    {"id": "s2", "type": "capability", "capability": "run", "requires": "s1"},
                ],
                "_provenance": {
                    "generated_by": "Kdesk-Catalog yaml-to-json",
                    "generator_version": "1.0.0",
                    "schema": "workflow-v1",
                    "source": "universal-agents/devops/agent/agent-a.yaml",
                },
            }
        ),
        encoding="utf-8",
    )
    return tmp_path


def test_cli_version():
    r = _run(["--version"], Path.cwd())
    assert r.returncode == 0
    assert "kdesk" in r.stdout


def test_cli_registry_stats(mini_repo):
    r = _run(["registry", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["agents"] == 1
    assert data["skills"] == 1


def test_cli_registry_search(mini_repo):
    r = _run(["registry", "--search", "helm", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    assert "agent-a" in r.stdout


def test_cli_graph_agent(mini_repo):
    r = _run(["graph", "--agent", "agent-a", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    assert "skill-1" in r.stdout


def test_cli_workflow_validate(mini_repo):
    r = _run(["workflow", "--validate", "wf-good", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    assert "OK" in r.stdout


def test_cli_workflow_run_dry(mini_repo):
    r = _run(["workflow", "--run", "wf-good", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    assert "dry-run" in r.stdout


def test_cli_adapters(mini_repo):
    r = _run(["adapters", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["platforms"] == 45


def test_cli_doctor(mini_repo):
    r = _run(["doctor", "--platform", "cursor", "--base", str(mini_repo), "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    assert "NOT_GENERATED" in r.stdout or "MISSING" in r.stdout


def test_cli_security_clean(mini_repo):
    r = _run(["security", "--json", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0


def test_cli_provenance(mini_repo):
    r = _run(["provenance", "--root", str(mini_repo)], mini_repo)
    # agents/skills JSON dirs do not exist yet: JSON side scans nothing -> verified only if
    # no JSON files exist. Should not crash.
    assert r.returncode == 0


def test_cli_unknown_command(mini_repo):
    r = _run(["nonsense"], mini_repo)
    assert r.returncode == 2


def test_cli_adapters_single(mini_repo):
    r = _run(["adapters", "--platform", "claude_code", "--root", str(mini_repo)], mini_repo)
    assert r.returncode == 0
    assert "claude_code" in r.stdout