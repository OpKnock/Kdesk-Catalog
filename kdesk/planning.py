"""Phase K planning: build an ExecutionPlan from a resolution.

A plan is a list of steps. Each step has a deterministic action
(skill_load | capability | analyze | write | report), a target, an input
request, an expected output, a risk class, an approval decision and a
timeout. When multiple candidates chain (output of A feeds required input
of B), contracts are composed via `compatibility`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from kdesk.contracts import Contract, compatibility
from kdesk.policy import Decision, PolicyDecision, PolicyEngine
from kdesk.resolve import ResolveResult

STEP_TIMEOUTS = {"analyze": 30.0, "capability": 60.0, "skill_load": 10.0,
                 "write": 10.0, "report": 10.0}


@dataclass
class ExecutionStep:
    index: int
    action: str  # skill_load | capability | analyze | write | report
    target: str
    description: str = ""
    tool: str = "builtin"
    request: str = ""
    inputs: Dict[str, Any] = field(default_factory=dict)
    expected_output: str = ""
    risk: str = "safe"
    decision: PolicyDecision = field(default_factory=lambda: PolicyDecision(
        decision=Decision.ALLOWED, reason="not evaluated yet"))
    timeout_s: float = 30.0
    depends_on: List[int] = field(default_factory=list)
    mode: str = "local"  # local | subprocess | orchestrated

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "action": self.action,
            "target": self.target,
            "description": self.description,
            "tool": self.tool,
            "request": self.request,
            "inputs": self.inputs,
            "expected_output": self.expected_output,
            "risk": self.risk,
            "decision": self.decision.decision.value,
            "decision_reason": self.decision.reason,
            "timeout_s": self.timeout_s,
            "depends_on": self.depends_on,
            "mode": self.mode,
        }


@dataclass
class ExecutionPlan:
    request: str
    steps: List[ExecutionStep] = field(default_factory=list)
    policy_notes: List[str] = field(default_factory=list)
    intent: str = "general"
    candidates: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request": self.request,
            "intent": self.intent,
            "candidates": self.candidates,
            "policy_notes": self.policy_notes,
            "steps": [s.to_dict() for s in self.steps],
        }


class PlanBuilder:
    """Deterministic plan construction from a ResolveResult."""

    def __init__(self, policy: PolicyEngine):
        self.policy = policy

    def build(self, result: ResolveResult, top_candidates: int = 2) -> ExecutionPlan:
        steps: List[ExecutionStep] = []
        notes: List[str] = []
        candidates = result.candidates[:top_candidates]
        if not candidates:
            steps.append(self._step(len(steps), "report", "no-candidate",
                                    "nothing actionable; report unresolved request",
                                    request=result.request))
            return ExecutionPlan(result.request, steps, notes, result.intent["intent"], [])

        primary = candidates[0]
        steps.append(self._candidate_step(0, primary, result.request,
                                          inputs={"goal": result.request}))
        chained = []
        for other in candidates[1:]:
            if other.contract is None or primary.contract is None:
                continue
            comp = compatibility(primary.contract, other.contract)
            if not comp["missing"] and comp["score"] >= 0.5:
                chained.append((other, comp))
                break
        for other, comp in chained:
            idx = len(steps)
            steps.append(self._candidate_step(idx, other, result.request,
                                              inputs={"goal": result.request,
                                                      "previous_outputs": comp["matched"]},
                                              depends_on=[0]))
            notes.append(
                f"composed {primary.name} -> {other.name} "
                f"(contract match {comp['score']:.2f}, satisfied {comp['matched']})"
            )
        if steps and steps[-1].action not in ("write", "report"):
            steps.append(self._step(len(steps), "report", "aggregate",
                                    "aggregate execution results into a final report",
                                    request=result.request, depends_on=[0]))
        if result.missing_requirements:
            notes.append(
                "missing runtimes: " + ", ".join(sorted(result.missing_requirements))
            )
        return ExecutionPlan(result.request, steps, notes, result.intent["intent"],
                             [c.name for c in candidates])

    def evaluate(self, plan: ExecutionPlan) -> ExecutionPlan:
        """Apply policy decisions to every step in place."""
        for step in plan.steps:
            step.decision = self.policy.decide(step.tool, step.inputs, step.risk)
        return plan

    def _candidate_step(self, index: int, candidate, request: str,
                        inputs: Dict[str, Any], depends_on: Optional[List[int]] = None
                        ) -> ExecutionStep:
        risk = candidate.contract.risk if candidate.contract else "safe"
        if candidate.definition_type == "skill":
            action = "skill_load"
            tool = "builtin"
            mode = "local"
        elif candidate.name == "code-reviewer" or "analy" in candidate.name:
            action = "analyze"
            tool = "analyze_project"
            mode = "local"
        else:
            action = "capability"
            tool = "builtin"
            mode = "local"
        expected = candidate.contract.output_names()[:1]
        return ExecutionStep(
            index=index,
            action=action,
            target=candidate.name,
            description=(candidate.contract.capabilities[:1] or ["execute"])[0],
            tool=tool,
            request=request,
            inputs=inputs,
            expected_output=expected[0] if expected else "report",
            risk=risk,
            timeout_s=STEP_TIMEOUTS.get(action, 30.0),
            depends_on=depends_on or [],
            mode=mode,
        )

    @staticmethod
    def _step(index: int, action: str, target: str, description: str,
              request: str, inputs: Optional[Dict[str, Any]] = None,
              depends_on: Optional[List[int]] = None) -> ExecutionStep:
        return ExecutionStep(
            index=index,
            action=action,
            target=target,
            description=description,
            request=request,
            inputs=inputs or {},
            risk="safe",
            timeout_s=STEP_TIMEOUTS.get(action, 10.0),
            depends_on=depends_on or [],
            mode="local",
        )