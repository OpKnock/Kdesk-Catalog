"""kdesk unit tests: workflow engine."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.models import Workflow
from kdesk.registry import Catalog
from kdesk.workflow import WorkflowEngine, WorkflowError


def _catalog(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    (base / "devops" / "skill").mkdir(parents=True)
    (base / "devops" / "agent" / "agent-a.yaml").write_text(
        """
name: agent-a
category: devops
description: Agent A description that is long enough to pass minimum thresholds.
version: "1.0.0"
type: agent
capabilities:
  - name: run
    description: Run a thing.
    commands: ["helm lint ./chart"]
""",
        encoding="utf-8",
    )
    (base / "devops" / "skill" / "skill-1.yaml").write_text(
        """
name: skill-1
category: devops
description: Skill one description that is long enough to pass minimum thresholds.
version: "1.0.0"
type: skill
""",
        encoding="utf-8",
    )
    return Catalog(base)


def _workflows(tmp_path):
    wf_dir = tmp_path / "workflows"
    wf_dir.mkdir(exist_ok=True)
    (wf_dir / "wf-good.workflow.json").write_text(
        json.dumps(
            {
                "id": "wf-good",
                "name": "Good",
                "agent": "agent-a",
                "steps": [
                    {"id": "s1", "type": "skill", "skill": "skill-1"},
                    {"id": "s2", "type": "capability", "capability": "run", "requires": "s1"},
                ],
            }
        ),
        encoding="utf-8",
    )
    (wf_dir / "wf-bad.workflow.json").write_text(
        json.dumps(
            {
                "id": "wf-bad",
                "name": "Bad",
                "agent": "ghost-agent",
                "steps": [
                    {"id": "s1", "type": "skill", "skill": "ghost-skill"},
                    {"id": "s2", "type": "mystery", "capability": "x"},
                ],
            }
        ),
        encoding="utf-8",
    )
    return wf_dir


def test_workflow_load_and_validate_ok(tmp_path):
    catalog = _catalog(tmp_path)
    engine = WorkflowEngine(catalog, workflows_dir=_workflows(tmp_path))
    wf = engine.load("wf-good")
    assert engine.validate(wf) == []


def test_workflow_validate_problems(tmp_path):
    catalog = _catalog(tmp_path)
    engine = WorkflowEngine(catalog, workflows_dir=_workflows(tmp_path))
    wf = engine.load("wf-bad")
    problems = engine.validate(wf)
    assert any("ghost-agent" in p for p in problems)
    assert any("ghost-skill" in p for p in problems)
    assert any("mystery" in p for p in problems)


def test_workflow_missing_raises(tmp_path):
    catalog = _catalog(tmp_path)
    engine = WorkflowEngine(catalog, workflows_dir=_workflows(tmp_path))
    with pytest.raises(WorkflowError):
        engine.load("nope")


def test_workflow_dry_run(tmp_path):
    catalog = _catalog(tmp_path)
    engine = WorkflowEngine(catalog, workflows_dir=_workflows(tmp_path))
    wf = engine.load("wf-good")
    results = engine.run(wf, dry_run=True)
    assert results["s1"]["action"] == "dry-run"
    assert results["s2"]["action"] == "dry-run"
    assert results["s2"]["tool"] == "helm"


def test_workflow_run_invalid_raises(tmp_path):
    catalog = _catalog(tmp_path)
    engine = WorkflowEngine(catalog, workflows_dir=_workflows(tmp_path))
    wf = engine.load("wf-bad")
    with pytest.raises(WorkflowError):
        engine.run(wf, dry_run=True)


def test_workflow_topological_order_respects_requires(tmp_path):
    catalog = _catalog(tmp_path)
    engine = WorkflowEngine(catalog, workflows_dir=_workflows(tmp_path))
    wf = engine.load("wf-good")
    order = engine._topological_order(wf)
    assert order.index("s1") < order.index("s2")


def test_workflow_summary(tmp_path):
    catalog = _catalog(tmp_path)
    engine = WorkflowEngine(catalog, workflows_dir=_workflows(tmp_path))
    summary = engine.summary()
    assert summary["workflows"] == 2
    assert summary["with_problems"] >= 1
    assert summary["files_scanned"] == 2