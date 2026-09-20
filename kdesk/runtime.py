"""Phase D: real workflow runtime.

16 node types: agent, skill, tool, subagent, approval, condition, loop,
parallel, validate, transform, notify, input, output, wait, fail, success.

Run state machine:
  CREATED -> PLANNING -> RUNNING -> WAITING_FOR_APPROVAL / WAITING_FOR_TOOL /
  VALIDATING / RETRYING / PAUSED -> ... -> COMPLETED | FAILED | CANCELLED

Deterministic execution: nodes run in dependency order; condition nodes pick a
branch; loop nodes re-fire their body up to max_iterations; parallel nodes run
their children in deterministic order. Approval and tool nodes block the run
until approve()/submit_tool_result(). Runs persist via to_dict/from_dict and
an optional RuntimeStore; every run gets an isolated AgentSession; the EventBus
records and broadcasts RuntimeEvents.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from kdesk.models import AgentSession, RuntimeEvent, ToolResult
from kdesk.registry import Catalog

NODE_TYPES = [
    "agent", "skill", "tool", "subagent", "approval", "condition", "loop",
    "parallel", "validate", "transform", "notify", "input", "output", "wait",
    "fail", "success",
]


class RunState(str, Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    RUNNING = "RUNNING"
    WAITING_FOR_TOOL = "WAITING_FOR_TOOL"
    VALIDATING = "VALIDATING"
    RETRYING = "RETRYING"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


TERMINAL = {RunState.FAILED, RunState.COMPLETED, RunState.CANCELLED}

TRANSITIONS: Dict[RunState, Set[RunState]] = {
    RunState.CREATED: {RunState.PLANNING},
    RunState.PLANNING: {RunState.RUNNING},
    RunState.RUNNING: {RunState.WAITING_FOR_APPROVAL, RunState.WAITING_FOR_TOOL,
                       RunState.VALIDATING, RunState.RETRYING, RunState.PAUSED,
                       RunState.COMPLETED, RunState.FAILED, RunState.CANCELLED},
    RunState.WAITING_FOR_APPROVAL: {RunState.RUNNING, RunState.FAILED},
    RunState.WAITING_FOR_TOOL: {RunState.RUNNING, RunState.RETRYING, RunState.FAILED},
    RunState.VALIDATING: {RunState.RUNNING, RunState.RETRYING, RunState.FAILED},
    RunState.RETRYING: {RunState.RUNNING},
    RunState.PAUSED: {RunState.RUNNING, RunState.CANCELLED},
    RunState.FAILED: set(),
    RunState.COMPLETED: set(),
    RunState.CANCELLED: set(),
}


class RunError(Exception):
    pass


class NodeState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class Node:
    id: str
    type: str
    config: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    branch: Optional[str] = None          # condition branch: "true" | "false"
    children: List[str] = field(default_factory=list)  # loop / parallel bodies
    max_iterations: int = 1
    attempts: int = 0
    max_attempts: int = 3
    state: NodeState = NodeState.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "type": self.type, "config": self.config,
            "depends_on": self.depends_on, "branch": self.branch,
            "children": self.children, "max_iterations": self.max_iterations,
            "attempts": self.attempts, "max_attempts": self.max_attempts,
            "state": self.state.value, "result": self.result, "error": self.error,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Node":
        n = cls(id=d["id"], type=d["type"], config=d.get("config") or {},
                depends_on=d.get("depends_on") or [], branch=d.get("branch"),
                children=d.get("children") or [],
                max_iterations=d.get("max_iterations", 1),
                attempts=d.get("attempts", 0), max_attempts=d.get("max_attempts", 3),
                state=NodeState(d.get("state", "PENDING")),
                result=d.get("result"), error=d.get("error"), meta=d.get("meta") or {})
        return n


# ----------------------------------------------------------------- EventBus
class EventBus:
    def __init__(self) -> None:
        self._listeners: List[Callable[[RuntimeEvent], None]] = []
        self.history: List[RuntimeEvent] = []

    def subscribe(self, fn: Callable[[RuntimeEvent], None]) -> Callable[[], None]:
        self._listeners.append(fn)
        return lambda: self._listeners.remove(fn)

    def publish(self, event: RuntimeEvent) -> None:
        self.history.append(event)
        for fn in list(self._listeners):
            fn(event)

    def emit(self, run_id: str, event_type: str, node_id: Optional[str] = None,
             payload: Optional[Dict[str, Any]] = None) -> RuntimeEvent:
        event = RuntimeEvent(type=event_type, run_id=run_id, node_id=node_id or "",
                             data=payload or {})
        self.publish(event)
        return event


# ------------------------------------------------------------------ Runtime
class WorkflowRuntime:
    """Deterministic node-based workflow runtime."""

    def __init__(self, catalog: Catalog, bus: Optional[EventBus] = None,
                 hooks: Optional[Dict[str, Callable]] = None):
        self.catalog = catalog
        self.bus = bus or EventBus()
        # hook overrides: e.g. {"agent": fn(node, ctx) -> result}
        self.hooks = hooks or {}

    # ------------------------------------------------------------ creation
    def create(self, workflow_id: str, nodes: List[Node], inputs: Optional[Dict[str, Any]] = None,
               run_id: Optional[str] = None, workflow_name: Optional[str] = None) -> "RuntimeRun":
        run_id = run_id or f"run-{uuid.uuid4().hex[:12]}"
        run = RuntimeRun(
            run_id=run_id, workflow_id=workflow_id,
            workflow_name=workflow_name or workflow_id,
            nodes={n.id: n for n in nodes}, inputs=dict(inputs or {}),
            bus=self.bus, hooks=self.hooks, catalog=self.catalog,
        )
        self.bus.emit(run_id, "run.created", payload={"workflow": workflow_id})
        return run


# -------------------------------------------------------------- RuntimeRun
class RuntimeRun:
    def __init__(self, run_id: str, workflow_id: str, workflow_name: str,
                 nodes: Dict[str, Node], inputs: Dict[str, Any], bus: EventBus,
                 hooks: Optional[Dict[str, Callable]] = None,
                 catalog: Optional[Catalog] = None):
        self.run_id = run_id
        self.workflow_id = workflow_id
        self.workflow_name = workflow_name
        self.nodes = nodes
        self.inputs = dict(inputs)
        self.variables: Dict[str, Any] = dict(inputs)
        self.outputs: Dict[str, Any] = {}
        self.state = RunState.CREATED
        self.session = AgentSession(session_id=f"session-{run_id}", agent_name=workflow_name)
        self.bus = bus
        self.hooks = hooks or {}
        self.catalog = catalog
        self._blocking: Optional[str] = None
        self.created_at = time.time()

    # -------------------------------------------------------- state machine
    def _transition(self, new: RunState) -> None:
        if new == self.state:
            return
        if new not in TRANSITIONS.get(self.state, set()):
            raise RunError(f"illegal transition {self.state.value} -> {new.value}")
        self.state = new
        self.bus.emit(self.run_id, f"run.{new.value.lower()}", payload={"workflow": self.workflow_id})

    # --------------------------------------------------------------- steps
    def start(self) -> "RuntimeRun":
        self._transition(RunState.PLANNING)
        self.bus.emit(self.run_id, "run.planning", payload={"nodes": sorted(self.nodes)})
        self._transition(RunState.RUNNING)
        self.advance()
        return self

    def advance(self) -> None:
        """Execute ready nodes one at a time; stop at blocking or terminal."""
        while self.state == RunState.RUNNING and not self._blocking:
            if not self._step():
                self._finish_if_done()
                return

    def _step(self) -> bool:
        ready = self._ready_nodes()
        if not ready:
            return False
        self._execute(ready[0])
        return True

    def _ready_nodes(self) -> List[str]:
        """Deterministic frontier: pending nodes whose deps all succeeded."""
        ready = []
        for nid in sorted(self.nodes):
            node = self.nodes[nid]
            if node.state != NodeState.PENDING:
                continue
            deps = (self.nodes[d] for d in node.depends_on if d in self.nodes)
            if all(d.state == NodeState.SUCCEEDED or d.state == NodeState.SKIPPED for d in deps):
                ready.append(nid)
        return ready

    def _finish_if_done(self) -> None:
        remaining = [n for n in self.nodes.values() if n.state == NodeState.PENDING]
        blocked = [n for n in remaining if n.depends_on]
        if not blocked:
            self._transition(RunState.COMPLETED)
            self.session.record_event("workflow.completed", {"run_id": self.run_id})
            self.bus.emit(self.run_id, "workflow.completed",
                          payload={"outputs": self.outputs})

    # -------------------------------------------------------------- execute
    def _execute(self, node_id: str) -> None:
        node = self.nodes[node_id]
        node.state = NodeState.RUNNING
        node.attempts += 1
        self.bus.emit(self.run_id, "node.start", node_id, {"type": node.type})
        try:
            self._dispatch(node)
        except RunError as exc:
            node.state = NodeState.FAILED
            node.error = str(exc)
            self._fail_run(node_id, str(exc))
        if node.state == NodeState.RUNNING:
            node.state = NodeState.SUCCEEDED
            self.bus.emit(self.run_id, "node.succeeded", node_id, {"result": node.result})
            # re-queue a parent loop so it can iterate again
            for other in self.nodes.values():
                if other.type == "loop" and node.id in other.children \
                        and other.state == NodeState.SUCCEEDED:
                    other.state = NodeState.PENDING
                    self.bus.emit(self.run_id, "loop.rerun", other.id, {"body": node.id})

    def _dispatch(self, node: Node) -> None:
        hook = self.hooks.get(node.type)
        if hook is not None:
            node.result = hook(node, self)
            return
        handler = getattr(self, f"_node_{node.type}", None)
        if handler is None:
            raise RunError(f"unknown node type: {node.type}")
        handler(node)

    # ---------------------------------------------------------- node types
    def _node_input(self, node: Node) -> None:
        key = node.config.get("key") or node.id
        value = node.config.get("value")
        node.result = {"key": key, "value": value}
        self.variables[key] = value

    def _node_transform(self, node: Node) -> None:
        expr = node.config.get("expr")
        if not expr:
            raise RunError(f"{node.id}: transform without expr")
        key = node.config.get("key")
        try:
            value = self._eval_expr(expr)
        except Exception as exc:
            raise RunError(f"{node.id}: transform failed: {exc}") from exc
        node.result = {"key": key, "value": value}
        if key:
            self.variables[key] = value

    def _node_condition(self, node: Node) -> None:
        expr = node.config.get("expr")
        if not expr:
            raise RunError(f"{node.id}: condition without expr")
        result = bool(self._eval_expr(expr))
        node.result = {"branch": "true" if result else "false"}
        self.bus.emit(self.run_id, "condition.evaluated", node.id,
                      {"expr": expr, "result": result})
        for other in self.nodes.values():
            if other is not node and other.branch is not None and other.state == NodeState.PENDING:
                if other.branch != node.result["branch"]:
                    other.state = NodeState.SKIPPED
                    self.bus.emit(self.run_id, "node.skipped", other.id, {})

    def _node_loop(self, node: Node) -> None:
        if not node.children:
            node.result = {"iterations": 0}
            return
        body = self.nodes[node.children[0]]
        iterations = node.meta.get("iterations", 0)
        if body.state in (NodeState.SUCCEEDED, NodeState.SKIPPED):
            if iterations >= node.max_iterations:
                node.result = {"iterations": iterations, "stopped": "max_iterations"}
                return
            try:
                keep = bool(self._eval_expr(node.config.get("expr", "True")))
            except Exception:
                keep = False
            if not keep:
                node.result = {"iterations": iterations, "stopped": "condition_false"}
                return
            body.state = NodeState.PENDING
            node.meta["iterations"] = iterations + 1
            node.result = {"iterations": iterations + 1, "rerun": True}
            return
        if body.state == NodeState.FAILED:
            raise RunError(f"{node.id}: loop body failed: {body.error}")
        node.meta["iterations"] = max(iterations, 1)
        node.result = {"iterations": node.meta["iterations"], "started": True}

    def _node_parallel(self, node: Node) -> None:
        pending = [n for n in node.children if n in self.nodes
                   and self.nodes[n].state == NodeState.PENDING]
        node.result = {"children": node.children, "pending": len(pending)}
        if pending:
            node.result["started"] = True

    def _node_approval(self, node: Node) -> None:
        self._blocking = node.id
        node.state = NodeState.WAITING
        self._transition(RunState.WAITING_FOR_APPROVAL)
        self.bus.emit(self.run_id, "approval.requested", node.id, node.config)

    def _node_tool(self, node: Node) -> None:
        self._blocking = node.id
        node.state = NodeState.WAITING
        self._transition(RunState.WAITING_FOR_TOOL)
        self.bus.emit(self.run_id, "tool.requested", node.id, node.config)

    def _node_wait(self, node: Node) -> None:
        self._blocking = node.id
        node.state = NodeState.WAITING
        self._transition(RunState.PAUSED)
        self.bus.emit(self.run_id, "wait.entered", node.id, node.config)

    def _node_fail(self, node: Node) -> None:
        message = node.config.get("message", "fail node reached")
        node.result = {"message": message}
        raise RunError(message)

    def _node_success(self, node: Node) -> None:
        node.result = {"message": node.config.get("message", "success")}
        self.outputs["success"] = node.result["message"]
        self._transition(RunState.COMPLETED)
        self.bus.emit(self.run_id, "workflow.completed", node.id,
                      {"outputs": self.outputs})

    def _node_agent(self, node: Node) -> None:
        agent = node.config.get("agent")
        if agent and self.catalog and self.catalog.get_agent(agent) is None:
            raise RunError(f"{node.id}: agent not in catalog: {agent}")
        description = None
        if agent and self.catalog:
            description = self.catalog.get_agent(agent).description
        node.result = {"agent": agent, "mode": "delegate", "description": description}
        self.session.record_event("agent.selected", {"agent": agent, "node": node.id})

    def _node_subagent(self, node: Node) -> None:
        self._node_agent(node)
        node.result["mode"] = "subagent"

    def _node_skill(self, node: Node) -> None:
        skill = node.config.get("skill")
        if skill and self.catalog and self.catalog.get_skill(skill) is None:
            raise RunError(f"{node.id}: skill not in catalog: {skill}")
        node.result = {"skill": skill, "loaded": True}
        self.session.record_event("skill.loaded", {"skill": skill, "node": node.id})

    def _node_validate(self, node: Node) -> None:
        checks = node.config.get("checks", [])
        failures = [c for c in checks if isinstance(c, str) and not self._eval_expr(c)]
        node.result = {"checks": len(checks), "failures": len(failures)}
        if failures:
            node.error = f"validation failed: {failures}"
            self._transition(RunState.VALIDATING)
            if node.attempts >= node.max_attempts:
                self._fail_run(node.id, node.error)
            else:
                node.state = NodeState.PENDING
                self._transition(RunState.RETRYING)
                self._transition(RunState.RUNNING)

    def _node_notify(self, node: Node) -> None:
        message = node.config.get("message", "")
        node.result = {"message": message}
        self.bus.emit(self.run_id, "notify", node.id, {"message": message})

    def _node_output(self, node: Node) -> None:
        key = node.config.get("key") or node.id
        value = node.config.get("value")
        if value is None and key in self.variables:
            value = self.variables[key]
        self.outputs[key] = value
        node.result = {"key": key, "value": value}

    # ------------------------------------------------------------ external
    def approve(self, node_id: str, approved: bool = True, note: Optional[str] = None) -> None:
        node = self._require_waiting(node_id, RunState.WAITING_FOR_APPROVAL)
        if not approved:
            node.state = NodeState.FAILED
            node.error = note or "rejected by user"
            self._transition(RunState.FAILED)
            return
        node.state = NodeState.SUCCEEDED
        node.result = {"approved": True, "note": note}
        self.session.record_event("approval.granted", {"node": node_id, "note": note})
        self._blocking = None
        self._transition(RunState.RUNNING)
        self.advance()

    def submit_tool_result(self, node_id: str, result: ToolResult) -> None:
        node = self._require_waiting(node_id, RunState.WAITING_FOR_TOOL)
        node.result = {"tool_result": result.to_dict() if hasattr(result, "to_dict") else result}
        self.session.record_event("tool.result", node.result)
        if result.success:
            node.state = NodeState.SUCCEEDED
            self._blocking = None
            self._transition(RunState.RUNNING)
            self.advance()
        else:
            if node.attempts >= node.max_attempts:
                node.state = NodeState.FAILED
                node.error = result.error or "tool failed"
                self._transition(RunState.FAILED)
            else:
                node.state = NodeState.PENDING
                self._blocking = None
                self._transition(RunState.RETRYING)
                self._transition(RunState.RUNNING)
                self.advance()

    def resume(self) -> None:
        if self.state != RunState.PAUSED:
            raise RunError(f"cannot resume from {self.state.value}")
        node = self.nodes[self._blocking] if self._blocking else None
        if node:
            node.state = NodeState.SUCCEEDED
            node.result = {"resumed": True}
        self._blocking = None
        self._transition(RunState.RUNNING)
        self.advance()

    def pause(self) -> None:
        if self.state != RunState.RUNNING:
            raise RunError(f"cannot pause from {self.state.value}")
        self._transition(RunState.PAUSED)

    def cancel(self, reason: Optional[str] = None) -> None:
        if self.state in TERMINAL:
            return
        for node in self.nodes.values():
            if node.state in (NodeState.PENDING, NodeState.RUNNING, NodeState.WAITING):
                node.state = NodeState.SKIPPED
        self._transition(RunState.CANCELLED)
        self.bus.emit(self.run_id, "run.cancelled", payload={"reason": reason})

    # -------------------------------------------------------------- helpers
    def _require_waiting(self, node_id: str, state: RunState) -> Node:
        if self.state != state:
            raise RunError(f"run is {self.state.value}, not {state.value}")
        node = self.nodes.get(node_id)
        if node is None or node.state != NodeState.WAITING:
            raise RunError(f"node {node_id} is not waiting")
        return node

    def _eval_expr(self, expr: str) -> Any:
        expr = str(expr)
        safe = {"variables": self.variables, "inputs": self.inputs,
                "outputs": self.outputs, "len": len, "str": str, "int": int,
                "float": float, "bool": bool, "min": min, "max": max, "sum": sum}
        code = re.sub(r"\b(?:__import__|eval|exec|open|globals|locals|compile)\b", "_", expr)
        if not all(c.isalnum() or c in " _()[]{}<>=!&|.,:'\"+-*/%#" for c in code):
            raise RunError(f"unsafe expression: {expr!r}")
        return eval(code, {"__builtins__": {}}, safe)  # noqa: S307 - sandboxed names

    def _fail_run(self, node_id: str, message: str) -> None:
        self._transition(RunState.FAILED)
        self.bus.emit(self.run_id, "run.failed", node_id, {"error": message})

    def status(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "workflow": self.workflow_name,
            "state": self.state.value,
            "nodes": {nid: {"type": n.type, "state": n.state.value}
                      for nid, n in sorted(self.nodes.items())},
            "blocking": self._blocking,
            "outputs": self.outputs,
        }

    # ---------------------------------------------------------- persistence
    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "workflow_id": self.workflow_id,
            "workflow_name": self.workflow_name,
            "state": self.state.value,
            "inputs": self.inputs,
            "variables": self.variables,
            "outputs": self.outputs,
            "blocking": self._blocking,
            "nodes": {nid: n.to_dict() for nid, n in self.nodes.items()},
            "session": {
                "session_id": self.session.session_id,
                "agent_name": self.session.agent_name,
                "platform": self.session.platform,
                "state": self.session.state,
                "context": self.session.context,
                "events": self.session.events,
            },
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], bus: EventBus) -> "RuntimeRun":
        run = cls(
            run_id=data["run_id"], workflow_id=data["workflow_id"],
            workflow_name=data["workflow_name"],
            nodes={nid: Node.from_dict(d) for nid, d in data["nodes"].items()},
            inputs=data.get("inputs") or {}, bus=bus,
        )
        run.variables = data.get("variables") or {}
        run.outputs = data.get("outputs") or {}
        run.state = RunState(data["state"])
        run._blocking = data.get("blocking")
        run.created_at = data.get("created_at", time.time())
        session = data.get("session") or {}
        run.session = AgentSession(session_id=session.get("session_id", f"session-{run.run_id}"),
                                   agent_name=session.get("agent_name", run.workflow_name))
        if session.get("platform"):
            run.session.platform = session["platform"]
        if session.get("state"):
            run.session.state = session["state"]
        if session.get("context"):
            run.session.context = session["context"]
        run.session.events = session.get("events") or []
        return run


# ------------------------------------------------------------------ Store
class RuntimeStore:
    """JSON persistence for runs under a directory (.kdesk/runs/<run_id>.json)."""

    def __init__(self, directory: Path):
        self.directory = Path(directory)

    def save(self, run: RuntimeRun) -> Path:
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self.directory / f"{run.run_id}.json"
        path.write_text(json.dumps(run.to_dict(), indent=2), encoding="utf-8")
        return path

    def load(self, run_id: str, bus: EventBus) -> RuntimeRun:
        path = self.directory / f"{run_id}.json"
        if not path.is_file():
            raise RunError(f"run not found: {run_id}")
        return RuntimeRun.from_dict(json.loads(path.read_text(encoding="utf-8")), bus)

    def list_runs(self) -> List[str]:
        if not self.directory.is_dir():
            return []
        return sorted(p.stem for p in self.directory.glob("*.json"))