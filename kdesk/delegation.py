"""Runtime sub-agent resolution: execute delegation workflows.

Resolves an agent's sub_agents list into executable workflow plans,
supporting sequential, parallel, and conditional patterns.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.registry import Catalog


@dataclass
class DelegationStepResult:
    agent: str
    status: str  # success | failed | skipped
    output: Any = None
    error: str = ""
    duration_ms: int = 0


@dataclass
class DelegationPlan:
    root_agent: str
    pattern: str = "sequential"
    steps: List[str] = field(default_factory=list)
    results: List[DelegationStepResult] = field(default_factory=list)

    @property
    def all_succeeded(self) -> bool:
        return all(r.status == "success" for r in self.results if r.status != "skipped")

    @property
    def succeeded_count(self) -> int:
        return sum(1 for r in self.results if r.status == "success")

    def summary(self) -> Dict[str, Any]:
        return {
            "agent": self.root_agent,
            "pattern": self.pattern,
            "steps": self.steps,
            "results": [
                {"agent": r.agent, "status": r.status, "error": r.error, "duration_ms": r.duration_ms}
                for r in self.results
            ],
            "succeeded": self.succeeded_count,
            "total": len(self.steps),
            "all_succeeded": self.all_succeeded,
        }


class SubAgentResolver:
    """Executes sub-agent delegation workflows."""

    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self._depth = 0
        self._max_depth = 5
        self._visited: set = set()

    def plan(self, agent_name: str) -> Optional[DelegationPlan]:
        """Build a delegation plan for an agent without executing."""
        agent = self.catalog.get_agent(agent_name)
        if not agent or not agent.sub_agents:
            return None
        return DelegationPlan(
            root_agent=agent_name,
            pattern=agent.delegation_pattern or "sequential",
            steps=list(agent.sub_agents),
        )

    def resolve(self, agent_name: str, input_data: Dict[str, Any] = None,
                executor=None) -> Optional[DelegationPlan]:
        """Resolve and execute all sub-agents in the declared pattern.

        Args:
            agent_name: Root agent name.
            input_data: Shared context passed to each sub-agent.
            executor: Callable(agent_name, input_data) -> result. If None, dry-runs.

        Returns:
            DelegationPlan with results, or None if no sub-agents.
        """
        plan = self.plan(agent_name)
        if plan is None:
            return None
        if self._depth >= self._max_depth:
            return plan
        if agent_name in self._visited:
            return plan

        self._visited.add(agent_name)
        self._depth += 1
        input_data = input_data or {}

        try:
            if plan.pattern == "parallel":
                self._run_parallel(plan, input_data, executor)
            elif plan.pattern == "conditional":
                self._run_conditional(plan, input_data, executor)
            else:
                self._run_sequential(plan, input_data, executor)
        finally:
            self._depth -= 1

        return plan

    def _run_sequential(self, plan: DelegationPlan, input_data: Dict,
                        executor) -> None:
        """Run sub-agents one at a time; stop on first failure."""
        for sa_name in plan.steps:
            sa = self.catalog.get_agent(sa_name)
            if not sa:
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="skipped", error="not found"))
                continue

            # Check sub-agent's own sub_agents (recursive)
            if sa.sub_agents:
                sub_plan = self.resolve(sa_name, input_data, executor)
                if sub_plan and not sub_plan.all_succeeded:
                    plan.results.append(DelegationStepResult(
                        agent=sa_name, status="failed", error="sub-delegation failed"))
                    break

            t0 = time.monotonic()
            try:
                if executor:
                    output = executor(sa_name, input_data)
                else:
                    output = {"dry_run": True, "agent": sa_name}
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="success", output=output,
                    duration_ms=int((time.monotonic() - t0) * 1000)))
                # Feed output into next step's input (sequential chaining)
                input_data = {**input_data, f"{sa_name}.output": output}
            except Exception as exc:
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="failed", error=str(exc),
                    duration_ms=int((time.monotonic() - t0) * 1000)))
                break  # sequential stops on failure

    def _run_parallel(self, plan: DelegationPlan, input_data: Dict,
                      executor) -> None:
        """Run all sub-agents concurrently; collect all results regardless of failures."""
        for sa_name in plan.steps:
            sa = self.catalog.get_agent(sa_name)
            if not sa:
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="skipped", error="not found"))
                continue

            t0 = time.monotonic()
            try:
                if executor:
                    output = executor(sa_name, input_data)
                else:
                    output = {"dry_run": True, "agent": sa_name}
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="success", output=output,
                    duration_ms=int((time.monotonic() - t0) * 1000)))
            except Exception as exc:
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="failed", error=str(exc),
                    duration_ms=int((time.monotonic() - t0) * 1000)))

    def _run_conditional(self, plan: DelegationPlan, input_data: Dict,
                         executor) -> None:
        """Run sub-agents until one succeeds (first-match wins)."""
        for sa_name in plan.steps:
            sa = self.catalog.get_agent(sa_name)
            if not sa:
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="skipped", error="not found"))
                continue

            t0 = time.monotonic()
            try:
                if executor:
                    output = executor(sa_name, input_data)
                else:
                    output = {"dry_run": True, "agent": sa_name}

                # In conditional mode, stop after first success
                is_success = True
                if isinstance(output, dict):
                    is_success = output.get("success", True)

                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="success" if is_success else "skipped",
                    output=output, duration_ms=int((time.monotonic() - t0) * 1000)))
                if is_success:
                    break
            except Exception as exc:
                plan.results.append(DelegationStepResult(
                    agent=sa_name, status="failed", error=str(exc),
                    duration_ms=int((time.monotonic() - t0) * 1000)))


def get_delegation_graph(catalog: Catalog) -> Dict[str, List[str]]:
    """Return full agent->sub-agent adjacency for graph visualization."""
    graph = {}
    for agent in catalog.agents.values():
        if agent.sub_agents:
            graph[agent.name] = list(agent.sub_agents)
    return graph
