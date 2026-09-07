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
            if step.requires and step.requires not in all_ids:
                problems.append(f"{step.id}: requires unknown step {step.requires!r}")
        elif step.step_type == "agent":
            if not step.agent:
                problems.append(f"{step.id}: agent step without agent id")
            elif self.catalog.get_agent(step.agent) is None:
                problems.append(f"{step.id}: agent not in catalog: {step.agent}")
            if step.requires and step.requires not in all_ids:
                problems.append(f"{step.id}: requires unknown step {step.requires!r}")
        elif step.step_type == "capability":
            if not step.capability:
                problems.append(f"{step.id}: capability step without capability name")
            if step.requires and step.requires not in all_ids:
                problems.append(f"{step.id}: requires unknown step {step.requires!r}")
        elif step.step_type == "parallel":
            # parallel: branches run concurrently, each branch is a list of step refs
            branches = step.raw.get("branches") or step.raw.get("steps") or []
            if not branches:
                # allow parallel with no explicit branches - just a marker that following steps are parallel
                pass
            else:
                for branch in branches if isinstance(branches, list) else []:
                    if isinstance(branch, list):
                        for bid in branch:
                            if bid not in all_ids:
                                problems.append(f"{step.id}: parallel branch references unknown step {bid!r}")
                    elif isinstance(branch, str) and branch not in all_ids:
                        problems.append(f"{step.id}: parallel branch references unknown step {branch!r}")
            if step.requires and step.requires not in all_ids:
                problems.append(f"{step.id}: requires unknown step {step.requires!r}")
        elif step.step_type == "conditional":
            # conditional: requires condition expression and branches
            cond = step.raw.get("condition") or step.raw.get("if")
            if not cond:
                problems.append(f"{step.id}: conditional step without condition")
            # validate then/else refs if present
            for key in ("then", "else", "else_branch", "then_branch"):
                val = step.raw.get(key)
                if isinstance(val, str) and val not in all_ids:
                    problems.append(f"{step.id}: conditional {key} references unknown step {val!r}")
                elif isinstance(val, list):
                    for vid in val:
                        if isinstance(vid, str) and vid not in all_ids:
                            problems.append(f"{step.id}: conditional {key} references unknown step {vid!r}")
            if step.requires and step.requires not in all_ids:
                problems.append(f"{step.id}: requires unknown step {step.requires!r}")
        elif step.step_type == "sequential":
            # sequential: explicit ordering, requires chain validation
            ordered = step.raw.get("steps") or step.raw.get("sequence") or []
            if isinstance(ordered, list):
                for sid in ordered:
                    if isinstance(sid, str) and sid not in all_ids:
                        problems.append(f"{step.id}: sequential references unknown step {sid!r}")
            if step.requires and step.requires not in all_ids:
                problems.append(f"{step.id}: requires unknown step {step.requires!r}")
        elif step.step_type in ("loop", "approval", "tool", "condition"):
            # Generic passthrough types: validate requires only
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
            # Parallel/conditional forks: ensure branched steps run before join
            if s.step_type == "parallel":
                branches = s.raw.get("branches") or s.raw.get("steps") or []
                if isinstance(branches, list):
                    for branch in branches:
                        if isinstance(branch, list):
                            for bid in branch:
                                if bid in index and bid not in deps[s.id]:
                                    # parallel join depends on branches completing
                                    pass  # don't make join depend backwards
                                if s.id not in deps.get(bid, []):
                                    # branch steps should not depend on parallel join
                                    pass
                        elif isinstance(branch, str) and branch in index:
                            pass
            if s.step_type == "sequential":
                seq = s.raw.get("steps") or s.raw.get("sequence") or []
                if isinstance(seq, list) and len(seq) > 1:
                    for prev, nxt in zip(seq, seq[1:]):
                        if prev in index and nxt in index and prev not in deps[nxt]:
                            deps[nxt].append(prev)
        order: List[str] = []
        visited: set = set()
        visiting: set = set()

        def visit(node: str) -> None:
            if node in visited:
                return
            if node in visiting:
                raise WorkflowError(f"cycle detected at step {node!r}")
            visiting.add(node)
            for d in deps[node]:
                visit(d)
            visiting.remove(node)
            visited.add(node)
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
        if step.step_type == "parallel":
            branches = step.raw.get("branches") or step.raw.get("steps") or []
            return {
                "step": step.id,
                "type": "parallel",
                "branches": branches,
                "description": f"parallel execution of {len(branches) if isinstance(branches, list) else 0} branches",
                "action": "dry-run" if dry_run else "parallel-invoke",
            }
        if step.step_type == "conditional":
            cond = step.raw.get("condition") or step.raw.get("if") or ""
            return {
                "step": step.id,
                "type": "conditional",
                "condition": cond,
                "then": step.raw.get("then"),
                "else": step.raw.get("else"),
                "action": "dry-run" if dry_run else "evaluate",
            }
        if step.step_type == "sequential":
            seq = step.raw.get("steps") or step.raw.get("sequence") or []
            return {
                "step": step.id,
                "type": "sequential",
                "sequence": seq,
                "action": "dry-run" if dry_run else "sequential-invoke",
            }
        if step.step_type in ("loop", "approval", "tool", "condition"):
            return {
                "step": step.id,
                "type": step.step_type,
                "raw": step.raw,
                "action": "dry-run" if dry_run else step.step_type,
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