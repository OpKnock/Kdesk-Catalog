"""Phase C tests: AgentResolver, SkillResolver, SkillLoader, TaskPlanner."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.graph import CatalogGraph
from kdesk.models import TaskPlan, TaskRequest
from kdesk.registry import Catalog
from kdesk.resolvers import AgentResolver, SkillLoader, SkillResolver, TaskPlanner, _tokens


def _catalog(tmp_path) -> Catalog:
    base = tmp_path / "universal-agents"
    desc = "x" * 250
    p = base / "devops" / "agent"
    p.mkdir(parents=True)
    (p / "git-workflow.yaml").write_text(
        f"name: git-workflow\ncategory: devops\ndescription: {desc}\ntype: agent\n"
        f"tags: ['git', 'ci']\nskills: ['git']\n",
        encoding="utf-8",
    )
    (p / "python-api.yaml").write_text(
        f"name: python-api\ncategory: backend\ndescription: {desc} python api security\ntype: agent\n"
        f"tags: ['python']\ntools: ['uvicorn']\n",
        encoding="utf-8",
    )
    s = base / "devops" / "skill"
    s.mkdir(parents=True)
    (s / "git.yaml").write_text(
        f"name: git\ncategory: devops\ndescription: {desc}\ntype: skill\n"
        f"prerequisites: ['git-lfs']\n",
        encoding="utf-8",
    )
    (s / "git-lfs.yaml").write_text(
        f"name: git-lfs\ncategory: devops\ndescription: {desc}\ntype: skill\n",
        encoding="utf-8",
    )
    (s / "hadolint.yaml").write_text(
        f"name: hadolint\ncategory: code-quality\ndescription: {desc} dockerfile lint\ntype: skill\n",
        encoding="utf-8",
    )
    return Catalog(base)


def _graph(tmp_path):
    catalog = _catalog(tmp_path)
    return catalog, CatalogGraph(catalog, tmp_path / "no-wiring.json")


# ------------------------------------------------------------ AgentResolver
def test_agent_exact_name_wins(tmp_path):
    catalog, _ = _graph(tmp_path)
    top = AgentResolver(catalog).resolve("git-workflow")
    assert top[0].agent == "git-workflow"
    assert top[0].score >= 0.9


def test_agent_ranks_by_signal_strength(tmp_path):
    catalog, _ = _graph(tmp_path)
    top = AgentResolver(catalog).resolve("python api security")
    assert top[0].agent == "python-api"


def test_agent_explanation_lists_signals(tmp_path):
    catalog, _ = _graph(tmp_path)
    top = AgentResolver(catalog).resolve("git")
    assert any("->" in s for s in top[0].signals)


def test_agent_no_match_returns_empty(tmp_path):
    catalog, _ = _graph(tmp_path)
    assert AgentResolver(catalog).resolve("zzz-nonexistent-topic") == []


def test_agent_resolution_is_deterministic(tmp_path):
    catalog, _ = _graph(tmp_path)
    r1 = AgentResolver(catalog).resolve("git ci")
    r2 = AgentResolver(catalog).resolve("git ci")
    assert [c.agent for c in r1] == [c.agent for c in r2]


# ------------------------------------------------------------ SkillResolver
def test_skill_required_topic_hard_requires(tmp_path):
    catalog, graph = _graph(tmp_path)
    matches = SkillResolver(catalog, graph).resolve("dockerfile lint", required_topics=["hadolint"])
    assert matches[0].skill == "hadolint"
    assert matches[0].status == "required"
    assert matches[0].confidence == 1.0


def test_skill_resolution_statuses(tmp_path):
    catalog, graph = _graph(tmp_path)
    matches = SkillResolver(catalog, graph).resolve("git branch")
    git = next(m for m in matches if m.skill == "git")
    assert git.status == "required"
    assert "git-lfs" in git.dependencies


def test_skill_rejected_when_excluded(tmp_path):
    catalog, graph = _graph(tmp_path)
    matches = SkillResolver(catalog, graph).resolve("git", excluded=["git"])
    assert any(m.skill == "git" and m.status == "rejected" for m in matches)


# ------------------------------------------------------------- SkillLoader
def test_loader_prerequisites_first(tmp_path):
    catalog, graph = _graph(tmp_path)
    order = SkillLoader(catalog, graph).load_order(["git"])
    assert order.index("git-lfs") < order.index("git")


def test_loader_respects_budget_and_max(tmp_path):
    catalog, graph = _graph(tmp_path)
    order = SkillLoader(catalog, graph).load_order(["git", "hadolint"], budget=10, max_skills=1)
    assert len(order) == 1


def test_loader_skips_unknown_skills(tmp_path):
    catalog, graph = _graph(tmp_path)
    assert SkillLoader(catalog, graph).load_order(["does-not-exist"]) == []


# ------------------------------------------------------------- TaskPlanner
def test_planner_produces_plan(tmp_path):
    catalog, graph = _graph(tmp_path)
    plan = TaskPlanner(catalog, graph).plan(
        TaskRequest(id="t1", goal="python api security review", desired_skills=["git"])
    )
    assert isinstance(plan, TaskPlan)
    assert plan.task_id == "t1"
    assert plan.id == "plan-t1"
    assert plan.steps, "plan must contain steps"
    assert plan.steps[0].action == "run_agent"
    assert plan.steps[0].target == "python-api"


def test_planner_skill_steps_in_load_order(tmp_path):
    catalog, graph = _graph(tmp_path)
    plan = TaskPlanner(catalog, graph).plan(TaskRequest(id="t2", goal="git workflow"))
    skill_steps = [s.target for s in plan.steps if s.action == "load_skill"]
    if "git" in skill_steps and "git-lfs" in skill_steps:
        assert skill_steps.index("git-lfs") < skill_steps.index("git")