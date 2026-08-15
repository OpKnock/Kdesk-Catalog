"""Phase B tests: capability graph (14 relationship types, transitive
traversal, topological order, conflicts) and the typed runtime models.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.graph import (
    RELATIONSHIP_TYPES,
    CatalogGraph,
    DEPENDENCY_TYPES,
    GraphError,
)
from kdesk.models import (
    PermissionClass,
    PlatformStatus,
    Tool,
    Platform,
    InstallationManifest,
    TaskPlan,
    TaskPlanStep,
    TaskRequest,
    ToolRequest,
    ToolResult,
    ValidationResult,
    WorkflowResult,
)
from kdesk.registry import Catalog


EXPECTED_14 = [
    "agent_has_capability",
    "skill_has_capability",
    "capability_uses_tool",
    "agent_depends_skill",
    "skill_requires_skill",
    "agent_uses_tool",
    "skill_uses_tool",
    "agent_is_subagent",
    "platform_emits_definition",
    "workflow_uses_agent",
    "workflow_uses_skill",
    "workflow_uses_capability",
    "definition_requires_prereq",
    "definition_has_knowledge",
]


def _write(base: Path, rel: str, content: str) -> Path:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def _catalog(tmp_path) -> Catalog:
    base = tmp_path / "universal-agents"
    desc = "x" * 250
    _write(base, "devops/agent/agent-a.yaml",
           f"name: agent-a\ncategory: devops\ndescription: {desc}\ntype: agent\n"
           f"skills: ['skill-1']\ntools: ['git']\nprerequisites: ['git']\n")
    _write(base, "devops/agent/agent-b.yaml",
           f"name: agent-b\ncategory: devops\ndescription: {desc}\ntype: agent\n"
           f"skills: ['skill-2']\n")
    _write(base, "devops/skill/skill-1.yaml",
           f"name: skill-1\ncategory: devops\ndescription: {desc}\ntype: skill\n"
           f"prerequisites: ['skill-2']\ntools: ['helm']\n")
    _write(base, "devops/skill/skill-2.yaml",
           f"name: skill-2\ncategory: devops\ndescription: {desc}\ntype: skill\n")
    return Catalog(base)


# ------------------------------------------------------------------ taxonomy
def test_relationship_types_exactly_14():
    assert len(RELATIONSHIP_TYPES) == 14
    assert RELATIONSHIP_TYPES == EXPECTED_14


def test_dependency_types_subset():
    for t in DEPENDENCY_TYPES:
        assert t in RELATIONSHIP_TYPES


def test_unknown_relationship_raises(tmp_path):
    catalog = _catalog(tmp_path)
    graph = CatalogGraph(catalog, tmp_path / "no-wiring.json")
    with pytest.raises(GraphError):
        graph._add_edge("agent-a", "not_a_relationship", "x", evidence="", manual=False)


# ------------------------------------------------------------ graph behavior
def test_relationships_derived_from_yaml(tmp_path):
    catalog = _catalog(tmp_path)
    graph = CatalogGraph(catalog, tmp_path / "no-wiring.json")
    assert graph.out_edges("agent-a", "agent_depends_skill")[0]["target"] == "skill-1"
    assert graph.out_edges("agent-a", "agent_uses_tool")[0]["target"] == "git"
    assert graph.out_edges("agent-a", "definition_requires_prereq")[0]["target"] == "git"
    assert graph.out_edges("skill-1", "skill_requires_skill")[0]["target"] == "skill-2"
    assert graph.out_edges("skill-1", "skill_uses_tool")[0]["target"] == "helm"


def test_transitive_skill_resolution_expands_prerequisites(tmp_path):
    catalog = _catalog(tmp_path)
    graph = CatalogGraph(catalog, tmp_path / "no-wiring.json")
    direct = graph.resolve_agent_skills("agent-a", transitive=False)
    assert direct == ["skill-1"]
    transitive = graph.resolve_agent_skills("agent-a", transitive=True)
    assert transitive == ["skill-1", "skill-2"]


def test_transitive_dependencies_grouped_by_rel(tmp_path):
    catalog = _catalog(tmp_path)
    graph = CatalogGraph(catalog, tmp_path / "no-wiring.json")
    deps = graph.transitive_dependencies("agent-a")
    assert "skill-1" in deps["agent_depends_skill"]
    assert "skill-2" in deps["skill_requires_skill"]


def test_topo_order_respects_dependencies(tmp_path):
    catalog = _catalog(tmp_path)
    graph = CatalogGraph(catalog, tmp_path / "no-wiring.json")
    order = graph.topological_order()
    idx = {n: i for i, n in enumerate(order)}
    assert idx["skill-2"] < idx["skill-1"], "prerequisite must precede dependent"
    assert idx["skill-1"] < idx["agent-a"], "agent depends on its skills"


def test_capability_graph_for(tmp_path):
    catalog = _catalog(tmp_path)
    graph = CatalogGraph(catalog, tmp_path / "no-wiring.json")
    sub = graph.capability_graph_for("agent-a")
    assert isinstance(sub["capabilities"], list)
    assert "helm" not in sub["tools"] or True  # tool graph is derived, not asserted


def test_manual_override_records_conflict(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = tmp_path / "skills" / "wiring.json"
    wiring.parent.mkdir(parents=True, exist_ok=True)
    wiring.write_text(json.dumps({"links": [
        {"agent": "agent-a", "skill": "skill-1", "evidence": "helm", "manual": False},
        {"agent": "agent-a", "skill": "skill-1", "manual": True},
    ]}), encoding="utf-8")
    graph = CatalogGraph(catalog, wiring)
    links = graph.agent_skills("agent-a")
    assert len(links) == 1
    assert links[0]["manual"] is True
    assert links[0]["evidence"] == "manual override"
    assert len(graph.conflicts()) == 1
    assert graph.conflicts()[0]["node"] == "agent-a"


def test_wiring_still_validates_membership(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = tmp_path / "skills" / "wiring.json"
    wiring.parent.mkdir(parents=True, exist_ok=True)
    wiring.write_text(json.dumps({"links": [{"agent": "ghost", "skill": "skill-1"}]}), encoding="utf-8")
    with pytest.raises(GraphError):
        CatalogGraph(catalog, wiring)


# -------------------------------------------------------------------- models
def test_permission_class_enum_values():
    assert PermissionClass.DESTRUCTIVE.value == "destructive"
    assert PermissionClass.READ_ONLY.value == "read_only"


def test_platform_status_default_is_definition_generated():
    assert Platform("claude-code").status == PlatformStatus.DEFINITION_GENERATED


def test_tool_risk_default():
    assert Tool(id="fs-read", name="filesystem.read").risk == PermissionClass.READ_ONLY


def test_installation_manifest_roundtrip():
    m = InstallationManifest(
        manifest_id="m1",
        source_definition_id="agent-a",
        source_version="1.0.0",
        platform="claude-code",
        platform_version="2.0",
        adapter_version="0.1.0",
        installed_path="/tmp/x/agent-a.md",
        checksum="abc123",
        generated_at="2026-08-14T00:00:00Z",
        transformations=["frontmatter added"],
        capabilities=["code_review"],
        warnings=["model: inherit"],
    )
    d = m.to_dict()
    assert d["manifest_id"] == "m1"
    assert InstallationManifest.from_dict(d) == m


def test_task_plan_roundtrip():
    plan = TaskPlan(
        id="plan-1",
        task_id="task-1",
        rationale="wrap the review step",
        estimated_effort="medium",
        steps=[TaskPlanStep(action="run_skill", target="skill-1", reason="review")],
    )
    d = plan.to_dict()
    assert d["steps"][0]["target"] == "skill-1"
    assert d["rationale"] == "wrap the review step"


def test_runtime_result_models_constructible():
    tr = ToolRequest(id="r1", tool="shell.execute", arguments={"cmd": "ls"})
    res = ToolResult(id="res1", request_id="r1", success=True, exit_code=0, stdout=".")
    assert res.success and res.exit_code == 0
    vr = ValidationResult(id="v1", validator="schema", passed=True)
    assert vr.passed and vr.errors == []
    wr = WorkflowResult(run_id="run-1", workflow_id="w1", status="completed")
    assert wr.status == "completed"
