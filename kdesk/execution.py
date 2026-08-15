"""Phase E: execution layer.

Tool registry, permission engine, evidence-based validation, retry/replan
policy, prompt-injection guard, and the subagent executor (native adapter
delegation vs. orchestrated plan execution via the workflow runtime).
"""
from __future__ import annotations

import fnmatch
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .models import (
    PermissionClass, PermissionPolicy, TaskPlan, Tool, ToolRequest,
    ToolResult, ValidationResult,
)
from .resolvers import TaskPlanner
from .runtime import Node, WorkflowRuntime

RISK_RANK: Dict[PermissionClass, int] = {
    PermissionClass.READ_ONLY: 0,
    PermissionClass.SAFE_WRITE: 1,
    PermissionClass.MODERATE: 2,
    PermissionClass.DESTRUCTIVE: 3,
    PermissionClass.PRIVILEGED: 4,
}

DEFAULT_APPROVAL_THRESHOLD = PermissionClass.MODERATE


class ExecutionError(Exception):
    """Raised when the execution layer cannot complete an operation."""


# ---------------------------------------------------------------------------
# Safe expression evaluation (same sandbox rules as the runtime).
# ---------------------------------------------------------------------------
_SAFE_EVAL_BLOCKED = re.compile(
    r"__import__|eval|exec|open|globals|locals|compile|getattr|setattr|delattr|"
    r"vars|dir|type|class|base|subclasses|mro"
)
_SAFE_EVAL_CHARS = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    " _+-*/%<>=!&|.,:()[]{}'\"#$@?\\^~`"
)


def safe_eval(expr: str, variables: Dict[str, Any]) -> Any:
    """Evaluate a restricted expression against a variable namespace."""
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("empty expression")
    if _SAFE_EVAL_BLOCKED.search(expr):
        raise ValueError(f"blocked construct in expression: {expr!r}")
    if any(c not in _SAFE_EVAL_CHARS for c in expr):
        raise ValueError(f"disallowed character in expression: {expr!r}")
    ns = {"variables": dict(variables), "__builtins__": {}}
    return eval(expr, ns, {})  # noqa: S307 - sandboxed: no builtins, char whitelist


# ---------------------------------------------------------------------------
# Tool registry.
# ---------------------------------------------------------------------------
class ToolRegistry:
    """Registry of tools the runtime can invoke, with risk metadata."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if not tool.id or not tool.name:
            raise ExecutionError("tool requires id and name")
        self._tools[tool.id] = tool

    def get(self, tool_id: str) -> Tool:
        if tool_id not in self._tools:
            raise ExecutionError(f"unknown tool: {tool_id}")
        return self._tools[tool_id]

    def has(self, tool_id: str) -> bool:
        return tool_id in self._tools

    def supported(self, tool_id: str, platform: str) -> bool:
        tool = self.get(tool_id)
        return tool.platform_support.get(platform, True)

    def list(self) -> List[Tool]:
        return [self._tools[k] for k in sorted(self._tools)]

    @classmethod
    def with_defaults(cls) -> "ToolRegistry":
        reg = cls()
        defaults = [
            Tool(id="grep", name="grep", description="search file contents",
                 category="filesystem", risk=PermissionClass.READ_ONLY),
            Tool(id="glob", name="glob", description="find files by pattern",
                 category="filesystem", risk=PermissionClass.READ_ONLY),
            Tool(id="read_file", name="read_file", description="read a file",
                 category="filesystem", risk=PermissionClass.READ_ONLY),
            Tool(id="http_get", name="http_get", description="GET an HTTP resource",
                 category="network", risk=PermissionClass.READ_ONLY),
            Tool(id="write_file", name="write_file", description="write a file",
                 category="filesystem", risk=PermissionClass.SAFE_WRITE),
            Tool(id="edit_file", name="edit_file", description="edit a file in place",
                 category="filesystem", risk=PermissionClass.SAFE_WRITE),
            Tool(id="git", name="git", description="run a git operation",
                 category="vcs", risk=PermissionClass.SAFE_WRITE),
            Tool(id="shell", name="shell", description="run a shell command",
                 category="process", risk=PermissionClass.MODERATE),
            Tool(id="remove", name="remove", description="delete a file or directory",
                 category="filesystem", risk=PermissionClass.DESTRUCTIVE),
            Tool(id="package_install", name="package_install",
                 description="install a software package system-wide",
                 category="process", risk=PermissionClass.PRIVILEGED),
        ]
        for t in defaults:
            reg.register(t)
        return reg


# ---------------------------------------------------------------------------
# Permission engine.
# ---------------------------------------------------------------------------
class PermissionDecision(Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    REQUIRE_APPROVAL = "require_approval"


@dataclass
class PermissionVerdict:
    decision: PermissionDecision
    reason: str = ""
    policy: Optional[PermissionPolicy] = None
    risk: Optional[PermissionClass] = None


class PermissionEngine:
    """Decides whether a tool request may proceed under a policy set."""

    def __init__(self, policies: Optional[List[PermissionPolicy]] = None,
                 approval_threshold: PermissionClass = DEFAULT_APPROVAL_THRESHOLD) -> None:
        self.policies: List[PermissionPolicy] = list(policies or [])
        self.approval_threshold = approval_threshold

    def add_policy(self, policy: PermissionPolicy) -> None:
        self.policies.append(policy)

    def _match(self, policy: PermissionPolicy, tool: Tool,
               arguments: Dict[str, Any]) -> bool:
        if policy.tool not in ("*", tool.id, tool.name):
            return False
        if policy.pattern == "*":
            return True
        for key, value in arguments.items():
            if fnmatch.fnmatch(str(value), policy.pattern):
                return True
        return False

    def decide(self, tool: Tool, arguments: Optional[Dict[str, Any]] = None) -> PermissionVerdict:
        arguments = arguments or {}
        matched: List[PermissionPolicy] = [
            p for p in self.policies if self._match(p, tool, arguments)
        ]
        denied = [p for p in matched if p.action == "deny"]
        if denied:
            return PermissionVerdict(PermissionDecision.DENIED,
                                     denied[0].reason or "denied by policy", denied[0], tool.risk)
        allowed = [p for p in matched if p.action == "allow"]
        if allowed:
            return PermissionVerdict(PermissionDecision.ALLOWED,
                                     f"allowed by policy {allowed[0].id}", allowed[0], tool.risk)
        if RISK_RANK[tool.risk] >= RISK_RANK[self.approval_threshold]:
            return PermissionVerdict(
                PermissionDecision.REQUIRE_APPROVAL,
                f"risk {tool.risk.value} requires approval", None, tool.risk)
        return PermissionVerdict(PermissionDecision.ALLOWED,
                                 f"risk {tool.risk.value} below threshold", None, tool.risk)

    def authorize(self, request: ToolRequest, registry: ToolRegistry) -> PermissionVerdict:
        return self.decide(registry.get(request.tool), request.arguments)


# ---------------------------------------------------------------------------
# Validation engine (evidence-based).
# ---------------------------------------------------------------------------
ValidationCheck = Union[Callable[[Dict[str, Any]], Tuple[bool, str]], "Dict[str, str]"]

class ValidationEngine:
    """Runs named checks and records per-check evidence."""

    def __init__(self) -> None:
        self._validators: Dict[str, Callable[[Dict[str, Any]], Tuple[bool, str]]] = {}

    def register(self, name: str,
                 fn: Callable[[Dict[str, Any]], Tuple[bool, str]]) -> None:
        self._validators[name] = fn

    def _run_check(self, name: str, check: Any, ctx: Dict[str, Any]) -> Tuple[bool, str]:
        if callable(check):
            ok, detail = check(ctx)
        elif isinstance(check, dict):
            if "expr" in check:
                try:
                    ok = bool(safe_eval(check["expr"], ctx))
                except Exception as exc:  # noqa: BLE001 - evaluation failure is evidence
                    return False, f"expression error: {exc}"
                detail = check.get("detail", "expression passed" if ok else "expression failed")
            else:
                raise ExecutionError(f"check {name!r} needs 'expr' or callable")
        else:
            raise ExecutionError(f"check {name!r} must be callable or dict")
        return ok, detail

    def validate(self, validation_id: str, validator: str, checks: List[Any],
                 context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        ctx = dict(context or {})
        evidence: Dict[str, Any] = {}
        errors: List[str] = []
        for name, check in checks.items() if isinstance(checks, dict) else enumerate(checks):
            try:
                ok, detail = self._run_check(str(name), check, ctx)
            except Exception as exc:  # noqa: BLE001 - a broken check is a failed check
                ok, detail = False, f"check crashed: {exc}"
            evidence[str(name)] = {"ok": ok, "detail": detail}
            if not ok:
                errors.append(f"{name}: {detail}")
        return ValidationResult(id=validation_id, validator=validator,
                                passed=not errors, evidence=evidence, errors=errors)


# ---------------------------------------------------------------------------
# Retry / replan policy.
# ---------------------------------------------------------------------------
class RetryAction(Enum):
    RETRY = "retry"
    FIX = "fix"
    REPLAN = "replan"
    ESCALATE = "escalate"
    ABORT = "abort"


@dataclass
class FailureClass:
    action: RetryAction
    reason: str = ""
    retryable: bool = False
    backoff: float = 0.0


_TRANSIENT = re.compile(
    r"timeout|timed out|connection (refused|reset)|temporar|transient|429|5\d\d|"
    r"try again|busy|overload|rate.?limit"
)
_FIXABLE = re.compile(
    r"syntax|parse error|not found|no such file|permission denied|invalid (arg|option)|"
    r"unknown (command|tool)|missing (arg|config)|wrong type"
)
_ESCALATE = re.compile(
    r"auth|credential|token|401|403|quota|billing|unpaid|forbidden"
)
_REPLAN = re.compile(
    r"unsupported|not supported|capabilit|platform|depends on|missing dependen|"
    r"no adapter|no integration"
)
_INJECTION = re.compile(
    r"ignore (previous|prior|all)|disregard|system prompt|you are now|"
    r"instructions in (this|the) (output|tool result)"
)


class RetryPolicy:
    """Classifies a failure and computes the next action + backoff."""

    def __init__(self, max_retries: int = 3, backoff_base: float = 1.0,
                 backoff_cap: float = 30.0, jitter: bool = False) -> None:
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_cap = backoff_cap
        self.jitter = jitter

    def backoff(self, attempt: int) -> float:
        value = min(self.backoff_base * (2 ** max(attempt - 1, 0)), self.backoff_cap)
        if self.jitter and value > 0:
            value = value * (0.5 + (time.time_ns() % 1000) / 2000.0)
        return round(value, 3)

    def classify(self, error: str, attempts: int) -> FailureClass:
        text = error or ""
        if _INJECTION.search(text):
            return FailureClass(RetryAction.ABORT, "suspicious instructions in output", False)
        if _TRANSIENT.search(text):
            retryable = attempts < self.max_retries
            return FailureClass(
                RetryAction.RETRY if retryable else RetryAction.ESCALATE,
                "transient failure" if retryable else "exhausted transient retries",
                retryable, self.backoff(attempts))
        if _FIXABLE.search(text):
            return FailureClass(RetryAction.FIX, "fixable input/command error", False)
        if _ESCALATE.search(text):
            return FailureClass(RetryAction.ESCALATE, "requires escalation", False)
        if _REPLAN.search(text):
            return FailureClass(RetryAction.REPLAN, "plan needs revision", False)
        return FailureClass(RetryAction.ABORT, "unclassified failure", False)


# ---------------------------------------------------------------------------
# Prompt-injection guard (boundary between untrusted tool output and context).
# ---------------------------------------------------------------------------
class PromptInjectionGuard:
    """Detects and neutralizes instructions smuggled in tool output."""

    _DIRECTIVE_RE = re.compile(
        r"(?i)(ignore|disregard|forget)\s+(previous|prior|all|above).{0,80}"
        r"|you\s+are\s+now\s+.{0,60}"
        r"|(do|must|need)\s+to\s+.{0,120}(prompt|instruction|command)"
    )

    def __init__(self, max_context_chars: int = 20000) -> None:
        self.max_context_chars = max_context_chars

    def contains_injection(self, text: str) -> bool:
        return bool(_INJECTION.search(text or "")) or bool(self._DIRECTIVE_RE.search(text or ""))

    def sanitize_for_context(self, text: str, max_chars: Optional[int] = None) -> str:
        """Strip directive-like blocks and truncate to the context budget."""
        limit = max_chars or self.max_context_chars
        clean = self._DIRECTIVE_RE.sub("[suspicious directive removed]", text or "")
        return clean[:limit]

    def trusted_sources(self) -> List[str]:
        return ["kdesk.registry", "kdesk.graph", "kdesk.stats"]


# ---------------------------------------------------------------------------
# Subagent executor: native (adapter) vs orchestrated (plan -> runtime).
# ---------------------------------------------------------------------------
@dataclass
class SubagentExecution:
    mode: str  # native | orchestrated
    run_id: str = ""
    state: str = ""
    results: Dict[str, Any] = field(default_factory=dict)
    events: List[str] = field(default_factory=list)
    error: str = ""


class SubagentExecutor:
    """Executes a TaskPlan: native delegation when an adapter supports it,
    otherwise orchestrated through the workflow runtime."""

    def __init__(self, catalog: Any, runtime: Optional[WorkflowRuntime] = None,
                 planner: Optional[TaskPlanner] = None) -> None:
        self.catalog = catalog
        self.runtime = runtime or WorkflowRuntime(catalog)
        self.planner = planner or TaskPlanner(catalog)

    def native(self, adapter: Any, agent_name: str, prompt: str,
               context: Optional[Dict[str, Any]] = None) -> SubagentExecution:
        invoke = getattr(adapter, "invoke_subagent", None)
        if not callable(invoke):
            raise ExecutionError(
                f"adapter {type(adapter).__name__} does not implement invoke_subagent; "
                "fall back to orchestrated mode")
        result = invoke(agent_name, prompt, context or {})
        return SubagentExecution(mode="native", results={"agent": agent_name, "result": result})

    def orchestrate(self, plan: TaskPlan,
                    inputs: Optional[Dict[str, Any]] = None) -> SubagentExecution:
        step_ids: Dict[int, str] = {id(step): _step_id(step) for step in plan.steps}
        nodes: List[Node] = []
        for step in plan.steps:
            step_id = step_ids[id(step)]
            deps = [step_ids[id(d)] for d in step.depends_on if id(d) in step_ids]
            if step.action == "run_agent":
                nodes.append(Node(id=step_id, type="agent",
                                  config={"agent": step.target},
                                  depends_on=deps))
            elif step.action == "load_skill":
                nodes.append(Node(id=step_id, type="skill",
                                  config={"skill": step.target},
                                  depends_on=deps))
            else:
                raise ExecutionError(f"unsupported plan action: {step.action}")
        run = self.runtime.create(f"plan-{plan.task_id if hasattr(plan, 'task_id') else 'task'}",
                                  nodes, inputs=inputs or {})
        run.start()
        results = {nid: n.result for nid, n in run.nodes.items()}
        return SubagentExecution(
            mode="orchestrated", run_id=run.run_id,
            state=run.state.value, results=results,
            events=[e.type for e in self.runtime.bus.history if e.run_id == run.run_id],
            error="")

    def run(self, request: Any, adapter: Optional[Any] = None) -> SubagentExecution:
        plan = self.planner.plan(request) if hasattr(self.planner, "plan") else request
        if adapter is not None:
            try:
                return self.native(adapter, request.desired_agents[0] if getattr(
                    request, "desired_agents", None) else "primary",
                    getattr(request, "goal", ""))
            except ExecutionError:
                return self.orchestrate(plan, getattr(request, "context", None) or {})
        return self.orchestrate(plan, getattr(request, "context", None) or {})


def _step_id(step: Any) -> str:
    for attr in ("step_id", "id", "target"):
        value = getattr(step, attr, None)
        if value:
            return f"{step.action}-{value}" if attr == "target" else str(value)
    return f"{step.action}-{hash(step)}"