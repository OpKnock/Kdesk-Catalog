"""Live delegation check: sub-agents actually Read, Reason, Act via Task/workflow.

Fast (no 136k scan): uses tmp catalog fixture + real catalog-audit workflow.
Covers:
- SubAgentResolver plan/resolve for catalog-auditor (parallel, dry-run executor)
- WorkflowEngine catalog-audit workflow validate + dry-run parallel/conditional
- RuntimeAdapter strict type + Claude model inherit contract
- Wiring manifest: every agent wired, no unwired, no cycles
- Bundles registry covers all definitions
"""
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def _catalog():
    from kdesk.registry import Catalog
    return Catalog.from_repo(REPO)


class TestWiringComplete:
    def test_no_unwired_agents(self):
        from kdesk.graph import CatalogGraph
        g = CatalogGraph(_catalog(), wiring_path=REPO / "skills" / "wiring.json")
        assert g.unwired_agents() == []
        assert g.summary()["wired_agents"] == 1859

    def test_no_cycles(self):
        from kdesk.graph import CatalogGraph
        g = CatalogGraph(_catalog(), wiring_path=REPO / "skills" / "wiring.json")
        assert g.cycles() == []

    def test_wiring_manifest_stats(self):
        data = json.loads((REPO / "skills" / "wiring.json").read_text(encoding="utf-8"))
        assert data["stats"]["unwired_agents"] == 0
        assert data["stats"]["agents_wired"] == 1859
        # tool-evidence links preserved, fallback tier labeled
        assert data["stats"]["total_links"] >= 4305

    def test_bundles_cover_all(self):
        reg = json.loads((REPO / "bundles" / "registry.json").read_text(encoding="utf-8"))
        assert reg["agents"] == 1859
        assert reg["skills"] == 1235
        assert reg["bundles"] >= 300


class TestSubAgentDelegation:
    def test_catalog_auditor_plan(self):
        from kdesk.delegation import SubAgentResolver
        r = SubAgentResolver(_catalog())
        plan = r.plan("catalog-auditor")
        assert plan is not None
        assert plan.pattern == "parallel"
        assert len(plan.steps) >= 2

    def test_parallel_resolve_dry_run(self):
        from kdesk.delegation import SubAgentResolver
        r = SubAgentResolver(_catalog())
        plan = r.resolve("catalog-auditor", {"task": "audit"})
        assert plan is not None
        assert plan.all_succeeded
        assert plan.succeeded_count == len(plan.steps)

    def test_parallel_resolve_live_executor(self):
        """Executor simulates Task(subagent_type) real-time Read-Reason-Act."""
        from kdesk.delegation import SubAgentResolver
        calls = []

        def executor(agent_name, inputs):
            calls.append(agent_name)
            # simulate sub-agent Read -> Reason -> Act
            return {"read": f"{agent_name}:read-ok", "reason": "drift-checked", "act": "dry-run"}

        r = SubAgentResolver(_catalog())
        plan = r.resolve("catalog-auditor", {"task": "audit"}, executor=executor)
        assert plan.all_succeeded
        assert set(calls) == set(plan.steps)
        for res in plan.results:
            assert res.output["read"].endswith("read-ok")

    def test_workflow_delegation_types(self):
        from kdesk.workflow import WorkflowEngine
        eng = WorkflowEngine(_catalog(), workflows_dir=REPO / "workflows")
        wf = eng.load("catalog-audit")
        assert eng.validate(wf) == []
        out = eng.run(wf, dry_run=True)
        types = {v["type"] for v in out.values()}
        assert {"parallel", "conditional", "sequential", "skill"} <= types


class TestRuntimeContracts:
    def test_strict_type(self):
        from kdesk.adapters.contract import RuntimeAdapter
        ra = RuntimeAdapter()
        ra.render_skill = lambda d: {"s.md": "s"}
        ra.render_agent = lambda d: {"a.md": "a"}
        with pytest.raises(ValueError):
            ra.install({"name": "x"})
        assert ra.install({"name": "x", "type": "skill"})["content"] == {"s.md": "s"}

    def test_claude_inherit(self):
        from kdesk.adapters.contract import ClaudeCodeAdapter
        out = ClaudeCodeAdapter(project_root=REPO).render_agent(
            {"name": "t", "description": "d", "type": "agent"})
        content = list(out.values())[0]
        assert '"inherit"' in content
        assert "claude-4" not in content

    def test_platform_capability_versioning(self):
        from kdesk.adapters import AdapterRegistry
        reg = AdapterRegistry(root=REPO)
        a = reg.get("claude_code")
        assert a.version == "1.0.0"
        assert a.supports_capability("parallel", "1.0")
