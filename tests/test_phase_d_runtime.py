"""Phase D tests: workflow runtime (16 node types, state machine, events, persistence)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.models import ToolResult
from kdesk.registry import Catalog
from kdesk.runtime import (
    EventBus, NODE_TYPES, Node, NodeState, RunError, RunState, RuntimeStore,
    RuntimeRun, WorkflowRuntime,
)
from kdesk.runtime import TRANSITIONS, TERMINAL


@pytest.fixture(scope="module")
def catalog():
    return Catalog(Path(__file__).resolve().parents[1] / "universal-agents")


@pytest.fixture()
def rt(catalog):
    return WorkflowRuntime(catalog)


def _run(rt, nodes, **kw):
    return rt.create("wf-test", nodes, **kw)


# -------------------------------------------------------------- node types
def test_sixteen_node_types_defined():
    assert len(NODE_TYPES) == 16
    assert set(NODE_TYPES) == {
        "agent", "skill", "tool", "subagent", "approval", "condition", "loop",
        "parallel", "validate", "transform", "notify", "input", "output",
        "wait", "fail", "success",
    }


def test_every_node_type_has_handler(rt):
    for ntype in NODE_TYPES:
        run = _run(rt, [Node(id="n1", type=ntype)])
        assert getattr(RuntimeRun, f"_node_{ntype}", None) is not None, ntype


def test_unknown_node_type_fails(rt):
    run = _run(rt, [Node(id="n1", type="bogus")])
    run.start()
    assert run.state == RunState.FAILED
    assert run.nodes["n1"].state == NodeState.FAILED


# ----------------------------------------------------------- state machine
def test_created_to_completed(rt):
    run = _run(rt, [Node(id="n1", type="notify", config={"message": "hi"})])
    assert run.state == RunState.CREATED
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.nodes["n1"].state == NodeState.SUCCEEDED


def test_terminal_states_are_terminal():
    assert TERMINAL == {RunState.FAILED, RunState.COMPLETED, RunState.CANCELLED}
    for state in TERMINAL:
        assert TRANSITIONS[state] == set()


def test_illegal_transition_raises(rt):
    run = _run(rt, [Node(id="n1", type="notify")])
    with pytest.raises(RunError):
        run._transition(RunState.RUNNING)  # CREATED -> RUNNING is illegal


# --------------------------------------------------------------- approval
def test_approval_flow(rt):
    run = _run(rt, [
        Node(id="ap", type="approval", config={"prompt": "proceed?"}),
        Node(id="sk", type="skill", config={"skill": "docker"}, depends_on=["ap"]),
    ])
    run.start()
    assert run.state == RunState.WAITING_FOR_APPROVAL
    assert run._blocking == "ap"
    run.approve("ap")
    assert run.state == RunState.COMPLETED
    assert run.nodes["ap"].result == {"approved": True, "note": None}


def test_approval_rejection_fails_run(rt):
    run = _run(rt, [Node(id="ap", type="approval")])
    run.start()
    run.approve("ap", approved=False, note="no")
    assert run.state == RunState.FAILED
    assert "no" in (run.nodes["ap"].error or "")


def test_approve_wrong_state_raises(rt):
    run = _run(rt, [Node(id="ap", type="approval")])
    run.start()
    run.approve("ap")
    with pytest.raises(RunError):
        run.approve("ap")  # run already completed


# ------------------------------------------------------------------- tools
def test_tool_retry_then_success(rt):
    run = _run(rt, [Node(id="tl", type="tool", max_attempts=3)])
    run.start()
    assert run.state == RunState.WAITING_FOR_TOOL
    run.submit_tool_result("tl", ToolResult(id="1", request_id="r", success=False, error="e1"))
    assert run.state == RunState.WAITING_FOR_TOOL  # retried (re-blocked)
    assert run.nodes["tl"].attempts == 2
    run.submit_tool_result("tl", ToolResult(id="2", request_id="r", success=True))
    assert run.state == RunState.COMPLETED
    assert run.nodes["tl"].state == NodeState.SUCCEEDED


def test_tool_max_attempts_fails(rt):
    run = _run(rt, [Node(id="tl", type="tool", max_attempts=1)])
    run.start()
    run.submit_tool_result("tl", ToolResult(id="1", request_id="r", success=False, error="boom"))
    assert run.state == RunState.FAILED
    assert "boom" in (run.nodes["tl"].error or "")


# -------------------------------------------------------------- condition
def test_condition_true_branch(rt):
    run = _run(rt, [
        Node(id="i", type="input", config={"key": "x", "value": 1}),
        Node(id="c", type="condition", config={"expr": "variables['x'] == 1"}, depends_on=["i"]),
        Node(id="t", type="notify", config={"message": "true"}, depends_on=["c"], branch="true"),
        Node(id="f", type="notify", config={"message": "false"}, depends_on=["c"], branch="false"),
    ])
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.nodes["t"].state == NodeState.SUCCEEDED
    assert run.nodes["f"].state == NodeState.SKIPPED
    assert run.nodes["c"].result == {"branch": "true"}


# ------------------------------------------------------------------- loop
def test_loop_condition_stops(rt):
    run = _run(rt, [
        Node(id="lp", type="loop", config={"expr": "variables.get('n', 0) < 3"},
             children=["body"], max_iterations=10),
        Node(id="body", type="transform",
             config={"expr": "variables.get('n', 0) + 1", "key": "n"}, depends_on=["lp"]),
    ])
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.variables.get("n") == 3
    assert run.nodes["lp"].meta.get("iterations") == 3
    assert run.nodes["lp"].result.get("stopped") == "condition_false"


def test_loop_max_iterations(rt):
    run = _run(rt, [
        Node(id="lp", type="loop", config={"expr": "True"}, children=["body"], max_iterations=4),
        Node(id="body", type="transform",
             config={"expr": "variables.get('n', 0) + 1", "key": "n"}, depends_on=["lp"]),
    ])
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.nodes["lp"].result.get("stopped") == "max_iterations"
    assert run.nodes["lp"].meta.get("iterations") == 4
    assert run.variables.get("n") == 4


# --------------------------------------------------------------- parallel
def test_parallel_runs_all_children(rt):
    run = _run(rt, [
        Node(id="par", type="parallel", children=["a", "b"]),
        Node(id="a", type="notify", config={"message": "a"}, depends_on=["par"]),
        Node(id="b", type="notify", config={"message": "b"}, depends_on=["par"]),
    ])
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.nodes["a"].state == NodeState.SUCCEEDED
    assert run.nodes["b"].state == NodeState.SUCCEEDED


# ------------------------------------------------------------- transform
def test_transform_updates_variables(rt):
    run = _run(rt, [
        Node(id="i", type="input", config={"key": "n", "value": 2}),
        Node(id="t", type="transform", config={"expr": "variables['n'] * 10", "key": "result"}, depends_on=["i"]),
        Node(id="o", type="output", config={"key": "result"}, depends_on=["t"]),
    ])
    run.start()
    assert run.outputs.get("result") == 20
    assert run.variables.get("result") == 20


def test_transform_bad_expr_fails(rt):
    run = _run(rt, [Node(id="t", type="transform", config={"expr": "1 / 0"})])
    run.start()
    assert run.state == RunState.FAILED
    assert "transform failed" in (run.nodes["t"].error or "")


# -------------------------------------------------------------- validate
def test_validate_pass(rt):
    run = _run(rt, [
        Node(id="i", type="input", config={"key": "x", "value": 5}),
        Node(id="v", type="validate", config={"checks": ["variables['x'] > 0"]}, depends_on=["i"]),
    ])
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.nodes["v"].result == {"checks": 1, "failures": 0}


def test_validate_fail_without_retries(rt):
    run = _run(rt, [
        Node(id="i", type="input", config={"key": "x", "value": -1}),
        Node(id="v", type="validate",
             config={"checks": ["variables['x'] > 0"]}, max_attempts=1, depends_on=["i"]),
    ])
    run.start()
    assert run.state == RunState.FAILED


# ---------------------------------------------------------- fail / success
def test_fail_node_fails_run(rt):
    run = _run(rt, [Node(id="f", type="fail", config={"message": "stop here"})])
    run.start()
    assert run.state == RunState.FAILED
    assert "stop here" in (run.nodes["f"].error or "")


def test_success_node_completes(rt):
    run = _run(rt, [Node(id="s", type="success", config={"message": "done"})])
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.outputs.get("success") == "done"


# -------------------------------------------------------- wait/pause/cancel
def test_wait_pause_resume(rt):
    run = _run(rt, [Node(id="w", type="wait")])
    run.start()
    assert run.state == RunState.PAUSED
    run.resume()
    assert run.state == RunState.COMPLETED


def test_pause_and_cancel(rt):
    run = _run(rt, [Node(id="n1", type="notify")])
    run.start()
    assert run.state == RunState.COMPLETED
    run2 = _run(rt, [Node(id="w", type="wait")])
    run2.start()
    run2.cancel(reason="user abort")
    assert run2.state == RunState.CANCELLED


def test_resume_wrong_state_raises(rt):
    run = _run(rt, [Node(id="n1", type="notify")])
    run.start()
    with pytest.raises(RunError):
        run.resume()


# ------------------------------------------------------------------- hooks
def test_hooks_override_handler(rt):
    hooked = WorkflowRuntime(rt.catalog, hooks={"agent": lambda node, run: {"hooked": True}})
    run = hooked.create("wf-hook", [Node(id="a", type="agent", config={"agent": "git-workflow"})])
    run.start()
    assert run.state == RunState.COMPLETED
    assert run.nodes["a"].result == {"hooked": True}


def test_agent_node_unknown_agent_fails(rt):
    run = _run(rt, [Node(id="a", type="agent", config={"agent": "no-such-agent"})])
    run.start()
    assert run.state == RunState.FAILED
    assert "not in catalog" in (run.nodes["a"].error or "")


# ------------------------------------------------------------------- event
def test_event_bus_records_history(rt):
    assert len(rt.bus.history) == 0
    _run(rt, [Node(id="n1", type="notify")]).start()
    types = [e.type for e in rt.bus.history]
    assert "run.created" in types
    assert "run.planning" in types
    assert "workflow.completed" in types


def test_event_bus_subscribe(rt):
    seen = []
    rt.bus.subscribe(lambda e: seen.append(e.type))
    _run(rt, [Node(id="n1", type="notify")]).start()
    assert "run.created" in seen


# -------------------------------------------------------------- persistence
def test_store_round_trip(tmp_path, rt):
    run = _run(rt, [
        Node(id="i", type="input", config={"key": "k", "value": 1}),
        Node(id="o", type="output", config={"key": "k"}, depends_on=["i"]),
    ])
    run.start()
    store = RuntimeStore(tmp_path / "runs")
    path = store.save(run)
    assert path.is_file()
    restored = store.load(run.run_id, EventBus())
    assert restored.run_id == run.run_id
    assert restored.state == RunState.COMPLETED
    assert restored.outputs == run.outputs
    assert restored.session.events == run.session.events


def test_store_list_and_missing(tmp_path, rt):
    store = RuntimeStore(tmp_path / "runs")
    run = _run(rt, [Node(id="n1", type="notify")])
    run.start()
    store.save(run)
    assert store.list_runs() == [run.run_id]
    with pytest.raises(RunError):
        store.load("run-missing", EventBus())


# ------------------------------------------------------------------ session
def test_session_isolation_per_run(rt):
    r1 = _run(rt, [Node(id="n1", type="notify")])
    r2 = _run(rt, [Node(id="n1", type="notify")])
    r1.start()
    r2.start()
    assert r1.session.session_id != r2.session.session_id
    assert any(e["type"] == "workflow.completed" for e in r1.session.events)


def test_status_shape(rt):
    run = _run(rt, [Node(id="n1", type="notify")])
    run.start()
    status = run.status()
    assert status["run_id"] == run.run_id
    assert status["state"] == "COMPLETED"
    assert status["nodes"]["n1"]["state"] == "SUCCEEDED"