"""Phase F: runtime adapter contract tests."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kdesk.adapters.contract import (  # noqa: E402
    ClaudeCodeAdapter,
    CodexCliAdapter,
    CursorAdapter,
    RuntimeAdapterRegistry,
    RUNTIME_ADAPTERS,
)
from kdesk.execution import ExecutionError  # noqa: E402


@pytest.fixture
def project_root(tmp_path):
    return tmp_path / "repo"


@pytest.fixture
def home(tmp_path):
    return tmp_path / "home"


@pytest.fixture
def adapter_registry(project_root, home):
    return RuntimeAdapterRegistry(project_root, home)


@pytest.fixture
def agent_def():
    return {
        "name": "code-reviewer",
        "description": "Reviews diffs for correctness and style.",
        "tools": ["read", "grep"],
        "model": "claude-4",
        "body": "# Code Reviewer\n\nReviews pull requests.",
    }


@pytest.fixture
def skill_def():
    return {
        "skill": "pact",
        "description": "Contract testing with Pact.",
        "body": "# Pact\n\n## When to Use\n\nContract testing.",
    }


# ---------------------------------------------------------------- registry
def test_runtime_registry_covers_real_platforms(adapter_registry):
    assert adapter_registry.names() == ["claude_code", "codex_cli", "cursor"]
    assert adapter_registry.get("cursor") is not None
    assert adapter_registry.get("nope") is None


def test_detect_all_returns_bools(adapter_registry):
    found = adapter_registry.detect_all()
    assert set(found) == {"claude_code", "codex_cli", "cursor"}
    assert all(isinstance(v, bool) for v in found.values())


def test_version_all_returns_none_when_missing(adapter_registry):
    versions = adapter_registry.version_all()
    assert all(v is None for v in versions.values())


def test_capabilities_all_structure(adapter_registry):
    caps = adapter_registry.capabilities_all()
    for platform in ("claude_code", "codex_cli", "cursor"):
        assert "invoke_subagent" in caps[platform]
        assert "validate" in caps[platform]


# ------------------------------------------------------------- capabilities
def test_claude_subagent_capability_requires_detect(project_root, home, monkeypatch):
    adapter = ClaudeCodeAdapter(project_root, home)
    monkeypatch.setattr("shutil.which", lambda name: None)
    assert not adapter.capabilities().invoke_subagent


def test_cursor_never_claims_subagents(project_root, home):
    adapter = CursorAdapter(project_root, home)
    assert not adapter.subagents
    assert not adapter.capabilities().invoke


def test_codex_never_claims_subagents(project_root, home):
    adapter = CodexCliAdapter(project_root, home)
    assert not adapter.subagents


def test_claude_detects_home_config_dir(project_root, home):
    (home / ".claude").mkdir(parents=True)
    adapter = ClaudeCodeAdapter(project_root, home)
    assert adapter.detect()


def test_cursor_detects_project_config_dir(project_root, home):
    (project_root / ".cursor").mkdir(parents=True)
    adapter = CursorAdapter(project_root, home)
    assert adapter.detect()


# ------------------------------------------------------------------- paths
def test_claude_paths(project_root, home):
    adapter = ClaudeCodeAdapter(project_root, home)
    paths = adapter.paths()
    assert paths["agents_dir"] == str(home / ".claude" / "agents")
    assert paths["skills_dir"] == str(home / ".claude" / "skills")


def test_codex_paths(project_root, home):
    adapter = CodexCliAdapter(project_root, home)
    assert adapter.paths()["skills_dir"] == str(project_root / ".agents" / "skills")


# ------------------------------------------------------------------ render
def test_claude_renders_agent_frontmatter(project_root, home, agent_def):
    adapter = ClaudeCodeAdapter(project_root, home)
    rendered = adapter.render_agent(agent_def)
    rel = ".claude/agents/code-reviewer.md"
    assert set(rendered) == {rel}
    content = rendered[rel]
    assert content.startswith("---\n")
    fm = json.loads(content.split("---\n")[1].replace("\n", "\n").splitlines()[0][7:]) \
        if False else None
    assert "name: \"code-reviewer\"" in content
    assert "description: \"Reviews diffs" in content
    assert "tools:" in content
    assert content.endswith("\n")
    assert "# Code Reviewer" in content


def test_claude_renders_skill_skilmd(project_root, home, skill_def):
    adapter = ClaudeCodeAdapter(project_root, home)
    rendered = adapter.render_skill(skill_def)
    assert set(rendered) == {".claude/skills/pact/SKILL.md"}
    assert rendered[".claude/skills/pact/SKILL.md"].startswith("---\n")
    assert "name: \"pact\"" in rendered[".claude/skills/pact/SKILL.md"]


def test_codex_renders_skill(project_root, home, skill_def):
    adapter = CodexCliAdapter(project_root, home)
    rendered = adapter.render_skill(skill_def)
    assert set(rendered) == {".agents/skills/pact/SKILL.md"}
    assert "## When to Use" in rendered[".agents/skills/pact/SKILL.md"]


def test_cursor_renders_mdc_rule(project_root, home, agent_def):
    adapter = CursorAdapter(project_root, home)
    rendered = adapter.render_rules(agent_def)
    assert set(rendered) == {".cursor/rules/code-reviewer.mdc"}
    assert rendered[".cursor/rules/code-reviewer.mdc"].startswith("---\n")
    assert "alwaysApply: false" in rendered[".cursor/rules/code-reviewer.mdc"]


# ---------------------------------------------------------------- validate
def test_validate_accepts_good_frontmatter(project_root, home, agent_def):
    adapter = ClaudeCodeAdapter(project_root, home)
    rendered = adapter.render_agent(agent_def)
    result = adapter.validate(rendered)
    assert result.passed
    assert result.validator == "claude_code"
    assert len(result.evidence) == 1


def test_validate_rejects_empty_content(project_root, home):
    adapter = ClaudeCodeAdapter(project_root, home)
    result = adapter.validate({".claude/agents/x.md": ""})
    assert not result.passed
    assert any("empty" in e for e in result.errors)


def test_validate_rejects_missing_frontmatter(project_root, home):
    adapter = CursorAdapter(project_root, home)
    result = adapter.validate({".cursor/rules/x.mdc": "no frontmatter here"})
    assert not result.passed


# ----------------------------------------------------------------- install
def test_install_plans_targets(project_root, home, agent_def):
    adapter = ClaudeCodeAdapter(project_root, home)
    plan = adapter.install(agent_def)
    assert plan["adapter"] == "claude_code"
    assert plan["dry_run"] is True
    assert ".claude/agents/code-reviewer.md" in plan["targets"]
    assert plan["targets"][".claude/agents/code-reviewer.md"].startswith(
        str(project_root))


def test_uninstall_returns_plan(project_root, home):
    adapter = CursorAdapter(project_root, home)
    plan = adapter.uninstall(".cursor/rules/code-reviewer.mdc")
    assert plan["action"] == "uninstall"
    assert plan["dry_run"] is True


def test_update_returns_plan(project_root, home, agent_def):
    adapter = CodexCliAdapter(project_root, home)
    plan = adapter.update(agent_def)
    assert plan["action"] == "update"
    assert plan["definition"] == "code-reviewer"


# --------------------------------------------------------------- invocation
def test_launch_missing_binary_returns_result(project_root, home, monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)
    adapter = ClaudeCodeAdapter(project_root, home)
    result = adapter.launch(["-p", "hi"])
    assert not result.success
    assert "not installed" in result.error


def test_invoke_claude_missing_cli(project_root, home, monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)
    adapter = ClaudeCodeAdapter(project_root, home)
    result = adapter.invoke("hello")
    assert not result.success
    assert "not installed" in result.error


def test_invoke_codex_missing_cli(project_root, home, monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)
    adapter = CodexCliAdapter(project_root, home)
    result = adapter.invoke("hello")
    assert not result.success
    assert "not installed" in result.error


def test_cursor_invoke_is_unsupported(project_root, home):
    adapter = CursorAdapter(project_root, home)
    result = adapter.invoke("hello")
    assert not result.success
    assert "no headless" in result.error.lower()


def test_subagent_raises_for_cursor(project_root, home):
    adapter = CursorAdapter(project_root, home)
    with pytest.raises(ExecutionError):
        adapter.invoke_subagent("any", "prompt")


def test_subagent_raises_for_codex(project_root, home):
    adapter = CodexCliAdapter(project_root, home)
    with pytest.raises(ExecutionError):
        adapter.invoke_subagent("any", "prompt")


def test_subagent_missing_cli_returns_result(project_root, home, monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)
    adapter = ClaudeCodeAdapter(project_root, home)
    result = adapter.invoke_subagent("code-reviewer", "review this")
    assert not result.success
    assert "not installed" in result.error


# ----------------------------------------------------------- mcp + permissions
def test_claude_mcp_config_none_when_missing(project_root, home):
    adapter = ClaudeCodeAdapter(project_root, home)
    assert adapter.get_mcp_config() is None


def test_claude_reads_mcp_config(project_root, home):
    mcp = home / ".claude" / ".mcp.json"
    mcp.parent.mkdir(parents=True)
    mcp.write_text(json.dumps({"mcpServers": {"filesystem": {}}}), encoding="utf-8")
    adapter = ClaudeCodeAdapter(project_root, home)
    assert adapter.has_mcp_config()
    assert adapter.get_mcp_config()["mcpServers"] == {"filesystem": {}}


def test_permission_models_structured(project_root, home):
    assert ClaudeCodeAdapter(project_root, home).get_permission_model()["model"] == \
        "permission-modes"
    assert CodexCliAdapter(project_root, home).get_permission_model()["model"] == \
        "sandbox"
    assert CursorAdapter(project_root, home).get_permission_model()["model"] == \
        "allowlist-rules"


# ------------------------------------------------------------ limitations
def test_explain_limitations_is_honest(project_root, home):
    cursor = CursorAdapter(project_root, home)
    assert "subagent" in cursor.explain_limitations().lower()
    assert "invoke/invoke_subagent are unsupported" in cursor.explain_limitations()
    claude = ClaudeCodeAdapter(project_root, home)
    assert "claude" in claude.explain_limitations().lower()
    codex = CodexCliAdapter(project_root, home)
    assert "subagent" in codex.explain_limitations().lower()


def test_runtime_adapters_cover_emitted_platforms():
    assert {"claude_code", "cursor", "codex_cli"} <= set(RUNTIME_ADAPTERS)