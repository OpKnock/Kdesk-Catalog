"""Phase K engine: the request -> execution orchestrator.

Pipeline per master spec:
  REQUEST_RECEIVED -> INTENT_CLASSIFIED -> RESOLUTION_COMPLETED ->
  PLAN_CREATED -> POLICY_EVALUATED -> ENVIRONMENT_CHECKED ->
  (per step: STEP_STARTED, TOOL_EXECUTED, ARTIFACT_CREATED,
   APPROVAL_REQUESTED / APPROVAL_GRANTED / APPROVAL_DENIED) ->
  EXECUTION_SUCCEEDED | EXECUTION_FAILED | EXECUTION_BLOCKED |
  EXECUTION_TIMEOUT | EXECUTION_CANCELLED

Everything is persisted under <root>/.kdesk/runtime/: an executions.jsonl
index, per-execution JSON records, per-execution event logs, artifacts with
checksums, and an approvals store. Statuses follow the master spec:
PENDING, RUNNING, WAITING_APPROVAL, SUCCESS, PARTIAL, FAILED, BLOCKED,
CANCELLED, TIMEOUT.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.executor import ExecutionContextError, ToolExecutor, analyze_python_project, validate_expected
from kdesk.indexes import RuntimeIndexes
from kdesk.policy import (
    ApprovalState,
    ApprovalStore,
    Decision,
    PolicyDecision,
    PolicyEngine,
    now_iso,
)
from kdesk.planning import ExecutionPlan, ExecutionStep, PlanBuilder
from kdesk.registry import Catalog
from kdesk.resolve import ResolveResult, Resolver
from kdesk.security import REDACTED, _PATTERNS

STATUS_PENDING = "PENDING"
STATUS_RUNNING = "RUNNING"
STATUS_WAITING_APPROVAL = "WAITING_APPROVAL"
STATUS_SUCCESS = "SUCCESS"
STATUS_PARTIAL = "PARTIAL"
STATUS_FAILED = "FAILED"
STATUS_BLOCKED = "BLOCKED"
STATUS_CANCELLED = "CANCELLED"
STATUS_TIMEOUT = "TIMEOUT"

EVENT_REQUEST_RECEIVED = "REQUEST_RECEIVED"
EVENT_INTENT_CLASSIFIED = "INTENT_CLASSIFIED"
EVENT_RESOLUTION_COMPLETED = "RESOLUTION_COMPLETED"
EVENT_PLAN_CREATED = "PLAN_CREATED"
EVENT_POLICY_EVALUATED = "POLICY_EVALUATED"
EVENT_ENVIRONMENT_CHECKED = "ENVIRONMENT_CHECKED"
EVENT_STEP_STARTED = "STEP_STARTED"
EVENT_TOOL_EXECUTED = "TOOL_EXECUTED"
EVENT_ARTIFACT_CREATED = "ARTIFACT_CREATED"
EVENT_APPROVAL_REQUESTED = "APPROVAL_REQUESTED"
EVENT_APPROVAL_GRANTED = "APPROVAL_GRANTED"
EVENT_APPROVAL_DENIED = "APPROVAL_DENIED"
EVENT_VALIDATION_FAILED = "VALIDATION_FAILED"
EVENT_STEP_FAILED = "STEP_FAILED"
EVENT_STEP_RETRY = "STEP_RETRY"
EVENT_EXECUTION_SUCCEEDED = "EXECUTION_SUCCEEDED"
EVENT_EXECUTION_FAILED = "EXECUTION_FAILED"
EVENT_EXECUTION_BLOCKED = "EXECUTION_BLOCKED"
EVENT_EXECUTION_TIMEOUT = "EXECUTION_TIMEOUT"
EVENT_EXECUTION_CANCELLED = "EXECUTION_CANCELLED"
EVENT_EXECUTION_PAUSED = "EXECUTION_PAUSED"
EVENT_EXECUTION_RESUMED = "EXECUTION_RESUMED"

_EXECUTION_STATUS_EVENTS = {
    STATUS_SUCCESS: EVENT_EXECUTION_SUCCEEDED,
    STATUS_FAILED: EVENT_EXECUTION_FAILED,
    STATUS_BLOCKED: EVENT_EXECUTION_BLOCKED,
    STATUS_TIMEOUT: EVENT_EXECUTION_TIMEOUT,
    STATUS_CANCELLED: EVENT_EXECUTION_CANCELLED,
}


def redact_all(obj: Any) -> Any:
    """Recursively redact known secret patterns from any JSON-able object."""
    if isinstance(obj, str):
        for regex in _PATTERNS.values():
            import re

            obj = re.sub(regex, REDACTED, obj)
        return obj
    if isinstance(obj, dict):
        return {k: redact_all(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_all(v) for v in obj]
    return obj


def sha256_text(content: str) -> str:
    import hashlib

    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class RuntimeDir:
    """Persistent runtime directory layout under <root>/.kdesk/runtime/."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.dir = self.root / ".kdesk" / "runtime"
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "executions").mkdir(exist_ok=True)
        (self.dir / "events").mkdir(exist_ok=True)
        (self.dir / "artifacts").mkdir(exist_ok=True)
        self.approvals = ApprovalStore(self.dir)

    @property
    def index_path(self) -> Path:
        return self.dir / "executions.jsonl"

    def append_index(self, record: Dict[str, Any]) -> None:
        with open(self.index_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")

    def execution_path(self, execution_id: str) -> Path:
        return self.dir / "executions" / f"{execution_id}.json"

    def events_path(self, execution_id: str) -> Path:
        return self.dir / "events" / f"{execution_id}.jsonl"

    def artifacts_dir(self, execution_id: str) -> Path:
        path = self.dir / "artifacts" / execution_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def list_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        if not self.index_path.exists():
            return []
        records = []
        with open(self.index_path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                live = self.load_execution(str(record.get("execution_id", "")))
                if live is not None:
                    record = live
                records.append(record)
        return list(reversed(records))[:limit]

    def load_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        path = self.execution_path(execution_id)
        if not path.is_file():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    def save_execution(self, record: Dict[str, Any]) -> None:
        self.execution_path(record["execution_id"]).write_text(
            json.dumps(record, indent=2, default=str, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def append_event(self, execution_id: str, event_type: str,
                     data: Optional[Dict[str, Any]] = None) -> None:
        with open(self.events_path(execution_id), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(
                {"type": event_type, "timestamp": now_iso(), "data": redact_all(data or {})}
            ) + "\n")

    def load_events(self, execution_id: str) -> List[Dict[str, Any]]:
        path = self.events_path(execution_id)
        if not path.is_file():
            return []
        events = []
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except ValueError:
                    continue
        return events


@dataclass
class StepOutcome:
    index: int
    status: str  # SUCCESS | FAILED | BLOCKED | WAITING_APPROVAL | SKIPPED
    started_at: str = ""
    duration_ms: int = 0
    output_summary: str = ""
    artifact: Optional[Dict[str, Any]] = None
    error: str = ""
    decision: str = ""


@dataclass
class ExecutionResult:
    execution_id: str
    request: str
    intent: Dict[str, Any] = field(default_factory=dict)
    candidates: List[Dict[str, Any]] = field(default_factory=list)
    status: str = STATUS_PENDING
    steps: List[Dict[str, Any]] = field(default_factory=list)
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    missing_requirements: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    error: str = ""
    duration_ms: int = 0
    started_at: str = ""
    finished_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "request": self.request,
            "intent": self.intent,
            "candidates": self.candidates,
            "status": self.status,
            "steps": self.steps,
            "artifacts": self.artifacts,
            "missing_requirements": self.missing_requirements,
            "warnings": self.warnings,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }


class Engine:
    """Orchestrates request -> execution with persistence."""

    def __init__(self, root: Path, catalog: Optional[Catalog] = None,
                 policy: Optional[PolicyEngine] = None):
        self.root = Path(root)
        self.catalog = catalog or Catalog.from_repo(self.root)
        self.runtime = RuntimeDir(self.root)
        self.policy = policy or PolicyEngine()
        self.resolver = Resolver(self.catalog, RuntimeIndexes.from_catalog(self.catalog))
        self.builder = PlanBuilder(self.policy)

    # ------------------------------------------------------------- resolve
    def resolve(self, request: str, top: int = 8,
                probe_environment: bool = True) -> ResolveResult:
        return self.resolver.resolve(request, top=top, probe_environment=probe_environment)

    def why(self, request: str, target: str) -> Dict[str, Any]:
        return self.resolver.explain(request, target)

    def plan(self, request: str) -> ExecutionPlan:
        result = self.resolver.resolve(request, probe_environment=True)
        plan = self.builder.build(result)
        self.builder.evaluate(plan)
        return plan

    # --------------------------------------------------------------- run
    def run(self, request: str, base: Optional[Path] = None,
            auto_approve: bool = False, timeout_s: float = 120.0,
            execution_id: Optional[str] = None,
            dry_run: bool = False) -> ExecutionResult:
        execution_id = execution_id or f"{time.time_ns():x}"
        base = (Path(base) if base else self.root).resolve()
        started = now_iso()
        t0 = time.monotonic()
        record: Dict[str, Any] = {
            "execution_id": execution_id,
            "request": request,
            "status": STATUS_PENDING,
            "started_at": started,
            "base": str(base),
            "auto_approve": auto_approve,
        }
        self.runtime.append_index(record)
        self.runtime.append_event(execution_id, EVENT_REQUEST_RECEIVED, {"request": request})
        result = ExecutionResult(execution_id=execution_id, request=request,
                                 started_at=started)
        try:
            resolution = self.resolver.resolve(request, probe_environment=True)
        except Exception as exc:  # noqa: BLE001 - persist as failure
            return self._fail(result, record, t0, f"resolution failed: {exc}")
        result.intent = resolution.intent
        result.candidates = [c.to_dict() for c in resolution.candidates]
        result.missing_requirements = dict(resolution.missing_requirements)
        self.runtime.append_event(execution_id, EVENT_INTENT_CLASSIFIED, resolution.intent)
        self.runtime.append_event(execution_id, EVENT_RESOLUTION_COMPLETED,
                                  {"candidates": result.candidates})
        plan = self.builder.build(resolution)
        self.builder.evaluate(plan)
        record["plan"] = plan.to_dict()
        self.runtime.append_event(execution_id, EVENT_PLAN_CREATED, plan.to_dict())
        self.runtime.append_event(execution_id, EVENT_POLICY_EVALUATED,
                                  {"notes": plan.policy_notes})
        if resolution.environment:
            self.runtime.append_event(execution_id, EVENT_ENVIRONMENT_CHECKED,
                                      {"present": sorted(resolution.environment),
                                       "missing": sorted(resolution.missing_requirements)})
        if dry_run:
            record["status"] = STATUS_PENDING
            record["plan_only"] = True
            self.runtime.save_execution(record)
            result.status = STATUS_PENDING
            result.steps = [s.to_dict() for s in plan.steps]
            result.duration_ms = int((time.monotonic() - t0) * 1000)
            result.finished_at = now_iso()
            return result
        return self._execute_plan(result, record, plan, base, auto_approve, timeout_s, t0)

    def _execute_plan(self, result: ExecutionResult, record: Dict[str, Any],
                      plan: ExecutionPlan, base: Path, auto_approve: bool,
                      timeout_s: float, t0: float) -> ExecutionResult:
        execution_id = result.execution_id
        executor = ToolExecutor(base)
        result.status = STATUS_RUNNING
        record["status"] = STATUS_RUNNING
        self.runtime.save_execution(record)
        outcomes: List[StepOutcome] = []
        overall_t0 = time.monotonic()
        for step in plan.steps:
            if time.monotonic() - overall_t0 > timeout_s:
                return self._finalize(result, record, outcomes, STATUS_TIMEOUT,
                                      t0, "execution exceeded timeout budget")
            if step.decision.decision == Decision.DENIED:
                outcomes.append(StepOutcome(
                    index=step.index, status="BLOCKED",
                    decision=step.decision.decision.value,
                    error=step.decision.reason))
                self.runtime.append_event(execution_id, EVENT_STEP_FAILED,
                                          {"step": step.index, "reason": step.decision.reason})
                result.warnings.append(f"step {step.index} blocked: {step.decision.reason}")
                continue
            if step.decision.decision == Decision.REQUIRE_APPROVAL:
                if not auto_approve:
                    outcomes.append(StepOutcome(
                        index=step.index, status="WAITING_APPROVAL",
                        decision=step.decision.decision.value,
                        error=step.decision.reason))
                    self.runtime.append_event(execution_id, EVENT_APPROVAL_REQUESTED,
                                              {"step": step.index, "tool": step.tool,
                                               "risk": step.risk, "reason": step.decision.reason})
                    record["status"] = STATUS_WAITING_APPROVAL
                    record["approval_step"] = step.index
                    result.status = STATUS_WAITING_APPROVAL
                    self.runtime.save_execution(record)
                    self._apply_outcomes(result, record, outcomes)
                    return result
                approval = self.runtime.approvals.request(
                    execution_id, step.index, step.tool, step.inputs, step.risk)
                self.runtime.approvals.set_state(
                    execution_id, step.index, ApprovalState.AUTO_APPROVED,
                    note="auto-approve flag", decided_by="kdesk")
                self.runtime.append_event(execution_id, EVENT_APPROVAL_GRANTED,
                                          {"step": step.index, "approval": approval.to_dict()})
            outcome = self._run_step(executor, step, execution_id, t0)
            outcomes.append(outcome)
            if outcome.status == "FAILED":
                result.error = outcome.error
        status = STATUS_SUCCESS
        if any(o.status == "FAILED" for o in outcomes):
            status = STATUS_PARTIAL if any(o.status == "SUCCESS" for o in outcomes) else STATUS_FAILED
        elif any(o.status == "BLOCKED" for o in outcomes):
            status = STATUS_BLOCKED
        return self._finalize(result, record, outcomes, status, t0,
                              result.error or "")

    def _run_step(self, executor: ToolExecutor, step: ExecutionStep,
                  execution_id: str, t0: float) -> StepOutcome:
        outcome = StepOutcome(index=step.index, status="SUCCESS",
                              started_at=now_iso())
        self.runtime.append_event(execution_id, EVENT_STEP_STARTED,
                                  {"step": step.index, "action": step.action,
                                   "target": step.target, "tool": step.tool})
        step_t0 = time.monotonic()
        try:
            if step.action == "analyze" and step.tool == "analyze_project":
                target = Path(str(step.inputs.get("path", ".")))
                if not target.is_absolute():
                    target = executor.base / target
                if not target.is_dir():
                    raise ExecutionContextError(f"analyze target is not a directory: {target}")
                report = analyze_python_project(target)
                ok = True
                summary = f"analyzed {report['files']} python files"
                output = report
                result = None
            elif step.action == "write":
                args = {"path": str(step.inputs.get("path", "report.md")),
                        "content": str(step.inputs.get("content", ""))}
                result = executor.execute("write_file", args, timeout=step.timeout_s)
                ok, summary, output = result.success, result.stdout, result.output
            else:
                args = dict(step.inputs)
                args.setdefault("path", ".")
                tool_id = step.tool if step.tool != "builtin" else "analyze_project"
                result = executor.execute_with_retry(tool_id, args,
                                                     timeout=step.timeout_s, retries=1)
                ok, summary, output = result.success, result.stdout, result.output
            outcome.duration_ms = int((time.monotonic() - step_t0) * 1000)
            outcome.output_summary = (summary or "")[:500]
            artifact = self._persist_artifact(execution_id, step.index, output,
                                              step.target, summary or "")
            if artifact:
                outcome.artifact = artifact
                self.runtime.append_event(execution_id, EVENT_ARTIFACT_CREATED,
                                          {"step": step.index, "artifact": artifact})
            if not ok:
                outcome.status = "FAILED"
                outcome.error = (getattr(result, "error", "") or "step failed")[:500]
                self.runtime.append_event(execution_id, EVENT_STEP_FAILED,
                                          {"step": step.index, "error": outcome.error})
                return outcome
            if not validate_expected(result, step.expected_output):
                outcome.status = "FAILED"
                outcome.error = f"expected output '{step.expected_output}' not found"
                self.runtime.append_event(execution_id, EVENT_VALIDATION_FAILED,
                                          {"step": step.index, "expected": step.expected_output})
                return outcome
            self.runtime.append_event(execution_id, EVENT_TOOL_EXECUTED,
                                      {"step": step.index, "tool": step.tool,
                                       "success": True})
            return outcome
        except Exception as exc:  # noqa: BLE001
            outcome.status = "FAILED"
            outcome.error = str(exc)[:500]
            outcome.duration_ms = int((time.monotonic() - step_t0) * 1000)
            self.runtime.append_event(execution_id, EVENT_STEP_FAILED,
                                      {"step": step.index, "error": outcome.error})
            return outcome

    def _persist_artifact(self, execution_id: str, step_index: int, output: Any,
                          target: str, summary: str) -> Optional[Dict[str, Any]]:
        if output is None:
            return None
        payload = json.dumps(output, default=str, sort_keys=True)
        checksum = sha256_text(payload)
        path = self.runtime.artifacts_dir(execution_id) / f"step-{step_index}.json"
        path.write_text(payload, encoding="utf-8")
        return {
            "execution_id": execution_id,
            "step": step_index,
            "target": target,
            "path": str(path.relative_to(self.root)),
            "checksum": checksum,
            "bytes": len(payload),
            "summary": summary[:200],
        }

    def _finalize(self, result: ExecutionResult, record: Dict[str, Any],
                  outcomes: List[StepOutcome], status: str, t0: float,
                  error: str) -> ExecutionResult:
        result.status = status
        result.error = error
        result.duration_ms = int((time.monotonic() - t0) * 1000)
        result.finished_at = now_iso()
        record["status"] = status
        record["error"] = error
        record["duration_ms"] = result.duration_ms
        record["finished_at"] = result.finished_at
        self.runtime.save_execution(record)
        self._apply_outcomes(result, record, outcomes)
        event = _EXECUTION_STATUS_EVENTS.get(status, EVENT_EXECUTION_PAUSED)
        self.runtime.append_event(result.execution_id, event,
                                  {"status": status, "error": error})
        return result

    def _apply_outcomes(self, result: ExecutionResult, record: Dict[str, Any],
                        outcomes: List[StepOutcome]) -> None:
        for outcome in outcomes:
            step = {
                "index": outcome.index,
                "status": outcome.status,
                "started_at": outcome.started_at,
                "duration_ms": outcome.duration_ms,
                "output_summary": outcome.output_summary,
                "artifact": outcome.artifact,
                "error": outcome.error,
                "decision": outcome.decision,
            }
            if not any(s["index"] == outcome.index for s in result.steps):
                result.steps.append(step)
            if outcome.artifact and not any(
                a["path"] == outcome.artifact["path"] for a in result.artifacts
            ):
                result.artifacts.append(outcome.artifact)

    def _fail(self, result: ExecutionResult, record: Dict[str, Any],
              t0: float, error: str) -> ExecutionResult:
        result.status = STATUS_FAILED
        result.error = error
        result.duration_ms = int((time.monotonic() - t0) * 1000)
        result.finished_at = now_iso()
        record["status"] = STATUS_FAILED
        record["error"] = error
        self.runtime.save_execution(record)
        self.runtime.append_event(result.execution_id, EVENT_EXECUTION_FAILED,
                                  {"error": error})
        return result

    # ----------------------------------------------------- history/inspect
    def history(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self.runtime.list_history(limit)

    def inspect(self, execution_id: str) -> Optional[Dict[str, Any]]:
        record = self.runtime.load_execution(execution_id)
        if record is None:
            return None
        events = self.runtime.load_events(execution_id)
        artifacts = []
        artifacts_dir = self.runtime.artifacts_dir(execution_id)
        if artifacts_dir.is_dir():
            for path in sorted(artifacts_dir.glob("step-*.json")):
                try:
                    artifacts.append({
                        "path": str(path.relative_to(self.root)),
                        "size": path.stat().st_size,
                    })
                except OSError:
                    continue
        approvals = [a.to_dict() for a in self.runtime.approvals.list_for(execution_id)]
        return {
            "execution": redact_all(record),
            "events": events[-200:],
            "events_count": len(events),
            "artifacts": artifacts,
            "approvals": approvals,
        }

    # ------------------------------------------------------------ approval
    def approve(self, execution_id: str, step_index: int, approved: bool,
                note: str = "", decided_by: str = "kdesk") -> Optional[Dict[str, Any]]:
        record = self.runtime.load_execution(execution_id)
        if record is None:
            return None
        approval = self.runtime.approvals.get(execution_id, step_index)
        if approval is None:
            approval = self.runtime.approvals.request(
                execution_id, step_index, "write_file", {}, "review_required")
        state = ApprovalState.APPROVED if approved else ApprovalState.REJECTED
        updated = self.runtime.approvals.set_state(execution_id, step_index, state,
                                                   note=note, decided_by=decided_by)
        self.runtime.append_event(
            execution_id,
            EVENT_APPROVAL_GRANTED if approved else EVENT_APPROVAL_DENIED,
            {"step": step_index, "note": note, "decided_by": decided_by},
        )
        return updated.to_dict() if updated else None

    def resume(self, execution_id: str, base: Optional[Path] = None,
               timeout_s: float = 120.0, auto_approve: bool = False) -> Optional[ExecutionResult]:
        record = self.runtime.load_execution(execution_id)
        if record is None:
            return None
        request = str(record.get("request", ""))
        step_index = int(record.get("approval_step", -1))
        plan_data = record.get("plan") or {}
        plan = self._plan_from_dict(plan_data)
        if plan is None:
            return None
        plan = self._replan_if_needed(request, step_index)
        base = (Path(base) if base else Path(str(record.get("base", self.root)))).resolve()
        result = ExecutionResult(execution_id=execution_id, request=request,
                                 started_at=str(record.get("started_at", now_iso())))
        result.intent = dict(record.get("intent") or {})
        result.candidates = list(record.get("candidates") or [])
        result.missing_requirements = dict(record.get("missing_requirements") or {})
        self.runtime.append_event(execution_id, EVENT_EXECUTION_RESUMED, {"step": step_index})
        pending = [s for s in plan.steps if s.index >= step_index or s.index >= 0]
        if step_index >= 0:
            pending = [s for s in pending if s.index > step_index]
        plan.steps = pending
        t0 = time.monotonic()
        return self._execute_plan(result, record, plan, base,
                                  auto_approve=auto_approve, timeout_s=timeout_s, t0=t0)

    def _plan_from_dict(self, data: Dict[str, Any]) -> Optional[ExecutionPlan]:
        try:
            steps = [
                ExecutionStep(
                    index=int(s["index"]),
                    action=str(s.get("action", "capability")),
                    target=str(s.get("target", "")),
                    description=str(s.get("description", "")),
                    tool=str(s.get("tool", "builtin")),
                    request=str(s.get("request", "")),
                    inputs=dict(s.get("inputs") or {}),
                    expected_output=str(s.get("expected_output", "")),
                    risk=str(s.get("risk", "safe")),
                    decision=PolicyDecision(decision=Decision(str(s.get("decision", "allowed"))),
                                            reason=str(s.get("decision_reason", ""))),
                    timeout_s=float(s.get("timeout_s", 30.0)),
                    depends_on=[int(i) for i in (s.get("depends_on") or [])],
                    mode=str(s.get("mode", "local")),
                )
                for s in data.get("steps", [])
            ]
            return ExecutionPlan(
                request=str(data.get("request", "")),
                steps=steps,
                policy_notes=list(data.get("policy_notes") or []),
                intent=str(data.get("intent", "general")),
                candidates=list(data.get("candidates") or []),
            )
        except (KeyError, TypeError, ValueError):
            return None

    def _replan_if_needed(self, request: str, step_index: int) -> ExecutionPlan:
        result = self.resolver.resolve(request, probe_environment=False)
        plan = self.builder.build(result)
        self.builder.evaluate(plan)
        return plan