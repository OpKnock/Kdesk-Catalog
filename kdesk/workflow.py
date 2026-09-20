"""Workflow engine: validate and (dry-run) execute workflow-v1 JSON steps."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.models import Workflow, WorkflowStep
from kdesk.registry import Catalog, default_repo_root


class WorkflowError(Exception):
    pass


class WorkflowEngine:
    def __init__(self, catalog: Catalog, workflows_dir: Optional[Path] = None):
        self.catalog = catalog
        self.workflows_dir = Path(workflows_dir) if workflows_dir else default_repo_root() / "workflows"

    # ------------------------------------------------------------------ load
    def load(self, workflow_id: str) -> Workflow:
        for path in self.workflows_dir.rglob("*.workflow.json"):
            wf = Workflow.from_file(path)
            if wf.id == workflow_id:
                return wf
        raise WorkflowError(f"workflow not found: {workflow_id}")

    def all(self) -> List[Workflow]:
        found = []
        if not self.workflows_dir.is_dir():
            return found
        for path in sorted(self.workflows_dir.rglob("*.workflow.json")):
            try:
                found.append(Workflow.from_file(path))
            except Exception:
                continue
        return found

    # --------------------------------------------------------------- validate
    def validate(self, wf: Workflow) -> List[str]:
        problems: List[str] = []
        if not wf.id:
            problems.append("missing id")
        if not wf.agent:
            problems.append("missing agent")
        elif self.catalog.get_agent(wf.agent) is None:
            problems.append(f"agent not in catalog: {wf.agent}")

        ids = wf.step_ids()
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            problems.append(f"duplicate step ids: {sorted(dupes)}")

        for step in wf.steps:
            problems.extend(self._validate_step(step, ids))
        return problems

    def _validate_step(self, step: WorkflowStep, all_ids: List[str]) -> List[str]:
        problems: List[str] = []
        if step.step_type == "skill":
            if not step.skill:
                problems.append(f"{step.id}: skill step without skill id")
            elif self.catalog.get_skill(step.skill) is None:
                problems.append(f"{step.id}: skill not in catalog: {step.skill}")
        elif step.step_type == "agent":
            if not step.agent:
                problems.append(f"{step.id}: agent step without agent id")
            elif self.catalog.get_agent(step.agent) is None:
                problems.append(f"{step.id}: agent not in catalog: {step.agent}")
        elif step.step_type == "capability":
            if not step.capability:
                problems.append(f"{step.id}: capability step without capability name")
            if step.requires and step.requires not in all_ids:
                problems.append(f"{step.id}: requires unknown step {step.requires!r}")
        else:
            problems.append(f"{step.id}: unknown step type {step.step_type!r}")
        return problems

    # ------------------------------------------------------------------ run
    def run(self, wf: Workflow, inputs: Optional[Dict[str, Any]] = None, dry_run: bool = True) -> Dict[str, Any]:
        """Execute steps in dependency order. Default is dry-run (no commands run).

        Capability steps are executed by invoking the first real CLI command of
        the named capability ONLY when dry_run=False and execution is explicitly
        requested; dry-run validates the wiring and returns planned actions.
        """
        problems = self.validate(wf)
        if problems:
            raise WorkflowError(f"workflow {wf.id} invalid: {problems}")

        order = self._topological_order(wf)
        results: Dict[str, Any] = {}
        for step_id in order:
            step = next(s for s in wf.steps if s.id == step_id)
            results[step_id] = self._execute_step(step, inputs or {}, dry_run, wf.agent)
        return results

    @staticmethod
    def _topological_order(wf: Workflow) -> List[str]:
        ids = wf.step_ids()
        index = {i: n for n, i in enumerate(ids)}
        deps: Dict[str, List[str]] = {i: [] for i in ids}
        for s in wf.steps:
            if s.requires and s.requires in index:
                deps[s.id].append(s.requires)
        order: List[str] = []
        visited: set = set()

        def visit(node: str) -> None:
            if node in visited:
                return
            visited.add(node)
            for d in deps[node]:
                visit(d)
            order.append(node)

        for i in ids:
            visit(i)
        return order

    def _execute_step(
        self, step: WorkflowStep, inputs: Dict[str, Any], dry_run: bool, workflow_agent: Optional[str]
    ) -> Dict[str, Any]:
        if step.step_type == "skill":
            skill = self.catalog.get_skill(step.skill)
            return {
                "step": step.id,
                "type": "skill",
                "skill": step.skill,
                "description": skill.description if skill else None,
                "action": "dry-run" if dry_run else "invoke",
            }
        if step.step_type == "agent":
            agent = self.catalog.get_agent(step.agent)
            return {
                "step": step.id,
                "type": "agent",
                "agent": step.agent,
                "description": agent.description if agent else None,
                "input": inputs,
                "action": "dry-run" if dry_run else "delegate",
            }
        # capability (resolved against the workflow's agent)
        agent = self.catalog.get_agent(workflow_agent)
        cap = None
        if agent:
            cap = next((c for c in agent.capabilities if c.name == step.capability), None)
        cmd = cap.commands[0] if cap and cap.commands else None
        return {
            "step": step.id,
            "type": "capability",
            "capability": step.capability,
            "tool": step.tool or (cap.tool_binaries()[0] if cap and cap.tool_binaries() else None),
            "command": cmd,
            "action": "dry-run" if dry_run else "run-command",
        }

    def summary(self) -> Dict[str, Any]:
        wfs = self.all()
        problems = 0
        for wf in wfs:
            problems += len(self.validate(wf))
        return {
            "workflows": len(wfs),
            "with_problems": problems,
            "files_scanned": len(wfs),
        }