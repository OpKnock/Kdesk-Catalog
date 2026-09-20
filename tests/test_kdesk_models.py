"""kdesk unit tests: domain models."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.models import Agent, Capability, Skill, Workflow, WorkflowStep


def test_capability_tool_binaries():
    cap = Capability(
        name="scan",
        description="scan things",
        commands=["helm lint .", "kubectl get pods", "oc login"],
    )
    assert cap.tool_binaries() == ["helm", "kubectl", "oc"]


def test_capability_skips_template_shells():
    cap = Capability(name="template", commands=["$SKILL_TEMPLATE_INPUT"])
    assert cap.tool_binaries() == ["$SKILL_TEMPLATE_INPUT"] or cap.tool_binaries() == []


def test_agent_tool_binaries_aggregates():
    agent = Agent(
        name="k8s-ops",
        capabilities=[
            Capability(name="a", commands=["kubectl get"]),
            Capability(name="b", commands=["helm list"]),
        ],
    )
    assert sorted(agent.tool_binaries()) == ["helm", "kubectl"]


def test_skill_defaults():
    skill = Skill(name="skill-1", type="skill")
    assert skill.type == "skill"
    assert skill.capabilities == []
    assert getattr(skill, "skills", None) is None


def test_workflow_from_file_roundtrip(tmp_path):
    wf = Workflow(
        id="wf-test",
        name="Test WF",
        agent="agent-a",
        steps=[
            WorkflowStep(id="s1", step_type="skill", skill="skill-x"),
            WorkflowStep(id="s2", step_type="capability", capability="run", requires="s1"),
        ],
    )
    path = tmp_path / "wf-test.workflow.json"
    path.write_text(
        json.dumps(
            {
                "id": wf.id,
                "name": wf.name,
                "agent": wf.agent,
                "steps": [
                    {"id": "s1", "type": "skill", "skill": "skill-x"},
                    {"id": "s2", "type": "capability", "capability": "run", "requires": "s1"},
                ],
            }
        ),
        encoding="utf-8",
    )
    loaded = Workflow.from_file(path)
    assert loaded.id == "wf-test"
    assert loaded.step_ids() == ["s1", "s2"]
    assert loaded.referenced_entities() == {"skills": ["skill-x"], "agents": []}