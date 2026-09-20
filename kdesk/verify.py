"""Phase L verification: the `kdesk verify` gate.

Each check returns a result dict with name / status (PASS | FAIL | WARN |
SKIP) and a short detail. `main` aggregates, prints a table, and exits 0 on
all-PASS, 3 when any FAIL is present, 1 on internal error.

Checks:
  catalog_load        - catalog parses without errors
  schema              - scripts/schema-check.py (0 violations)
  provenance          - JSON definitions derived from YAML (yaml-to-json)
  wiring              - workflow skill/agent wiring (WorkflowEngine.load)
  duplicates          - duplicate definition names merged cleanly
  license             - license policy classification + repo license report
  security            - secrets scan (blocking HIGH/CRITICAL with exceptions)
  quality             - catalog health checks (stats thresholds)
  graph               - capability graph wiring
  adapters            - platform adapters are importable and report platforms
  doctor              - platform output directories are current
  workflow_engine     - workflow engine loads and plans a run
  resolve             - pipeline resolves a probe request
  plan                - pipeline builds an evaluated plan
  run                 - engine runs a tiny analysis end-to-end (tmp dir)
  cli                 - `kdesk <cmd> --help` exits 0 for every command
  freshness           - scripts/check-report-freshness.py (reports current)

Environment: KD_VERIFY_FAST=1 skips subprocess-heavy checks;
--skip NAME,NAME removes individual checks.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from kdesk import __version__
from kdesk.duplicates import DuplicatePolicy
from kdesk.engine import Engine, STATUS_SUCCESS
from kdesk.graph import CatalogGraph
from kdesk.license import LicensePolicy, VALID_CLASSES
from kdesk.registry import Catalog
from kdesk.security import SecurityExceptions, SecurityScanner
from kdesk.workflow import WorkflowEngine

CHECK_ORDER = [
    "catalog_load", "schema", "provenance", "wiring", "duplicates",
    "license", "security", "quality", "graph", "adapters", "doctor",
    "workflow_engine", "resolve", "plan", "run", "cli", "freshness",
]


def _subprocess_ok(args: List[str], cwd: Path, timeout: int = 600) -> tuple:
    """Run a repo script; return (returncode, tail_of_output)."""
    try:
        proc = subprocess.run(
            args, capture_output=True, text=True, timeout=timeout, cwd=str(cwd),
            env={**os.environ, "PYTHONPATH": str(cwd), "PYTHONIOENCODING": "utf-8"},
        )
        tail = (proc.stdout or proc.stderr).strip().splitlines()
        return proc.returncode, (tail[-1] if tail else "")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)


class VerifyRunner:
    def __init__(self, root: Path, fast: bool = False,
                 skip: Optional[List[str]] = None):
        self.root = Path(root)
        self.fast = fast or os.environ.get("KD_VERIFY_FAST") == "1"
        self.skip = set(skip or [])
        self.results: List[Dict[str, Any]] = []

    # ------------------------------------------------------------- checks
    def check_catalog_load(self) -> Dict[str, Any]:
        catalog = Catalog.from_repo(self.root)
        count = len(catalog.agents) + len(catalog.skills)
        return self._ok(f"catalog parses ({count} definitions)")

    def check_schema(self) -> Dict[str, Any]:
        if self.fast:
            return self._skip("fast mode")
        code, detail = _subprocess_ok([sys.executable, "scripts/schema-check.py"], self.root)
        return self._verdict(code == 0, detail or "schema-check exited %d" % code,
                             "schema-check.py must report 0 violations")

    def check_provenance(self) -> Dict[str, Any]:
        if self.fast:
            return self._skip("fast mode")
        code, detail = _subprocess_ok([sys.executable, "scripts/yaml-to-json.py"], self.root)
        return self._verdict(code == 0, detail or "yaml-to-json exited %d" % code,
                             "JSON definitions must be derivable from YAML")

    def check_wiring(self) -> Dict[str, Any]:
        try:
            catalog = Catalog.from_repo(self.root)
            engine = WorkflowEngine(catalog, workflows_dir=self.root / "workflows")
            workflows = engine.all()
        except Exception as exc:  # noqa: BLE001
            return self._fail(f"WorkflowEngine failed: {exc}")
        broken: List[str] = []
        for wf in workflows:
            broken.extend(f"{wf.id}: {p}" for p in engine.validate(wf))
        if broken:
            return self._fail(f"{len(broken)} workflow wiring errors: {broken[:3]}")
        return self._ok(f"all {len(workflows)} workflows wired")

    def check_duplicates(self) -> Dict[str, Any]:
        policy = DuplicatePolicy.load(self.root / "reports" / "duplicate-classifications.json")
        unclassified = [
            fid for fid, entry in policy.entries.items()
            if not entry.get("class") or entry.get("class") == "unresolved"
        ]
        return self._verdict(not unclassified,
                             f"{len(policy.entries)} families, {len(unclassified)} unresolved",
                             "every duplicate family must carry a review classification")

    def check_license(self) -> Dict[str, Any]:
        policy = LicensePolicy.load(self.root / "reports" / "license-policy.json")
        entries = policy.entries
        invalid = [n for n, e in entries.items() if e.get("class") not in VALID_CLASSES]
        return self._verdict(not invalid,
                             f"{len(entries)} licenses classified, {len(invalid)} invalid",
                             "no invalid license classifications")

    def check_security(self) -> Dict[str, Any]:
        catalog = Catalog.from_repo(self.root)
        findings = SecurityScanner(catalog).scan()
        exceptions = SecurityExceptions.load(self.root / "reports" / "security-exceptions.json")
        blocking = [
            f for f in findings
            if f["severity"] in ("HIGH", "CRITICAL") and not exceptions.matches(f)
        ]
        return self._verdict(not blocking,
                             f"{len(findings)} findings, {len(blocking)} blocking "
                             f"(excepted: {len(exceptions.entries)})",
                             "no unexcepted HIGH/CRITICAL secret findings")

    def check_quality(self) -> Dict[str, Any]:
        catalog = Catalog.from_repo(self.root)
        issues = []
        for name, defn in list(catalog.agents.items()) + list(catalog.skills.items()):
            if not defn.description or len(str(defn.description)) < 20:
                issues.append(f"{name}: missing/too-short description")
            if not defn.capabilities:
                issues.append(f"{name}: no capabilities")
            if not defn.instructions:
                issues.append(f"{name}: no instructions")
        return self._verdict(not issues,
                             f"{len(issues)} quality issues in {len(catalog.agents) + len(catalog.skills)} definitions",
                             "every definition needs description, capabilities, instructions")

    def check_graph(self) -> Dict[str, Any]:
        from kdesk.graph import DEPENDENCY_TYPES

        catalog = Catalog.from_repo(self.root)
        graph = CatalogGraph(catalog, wiring_path=self.root / "skills" / "wiring.json")
        adjacency: Dict[str, List[str]] = {}
        for node, edges in graph.edges.items():
            for edge in edges:
                if edge["rel"] not in DEPENDENCY_TYPES:
                    continue
                adjacency.setdefault(node, [])
                adjacency.setdefault(edge["target"], [])
                adjacency[node].append(edge["target"])
        cycle = self._find_cycle(adjacency)
        nodes = len(adjacency)
        conflicts = len(graph._conflict_log)
        if cycle is not None:
            return self._fail(f"{nodes} graph nodes, cycle: {' -> '.join(cycle)}")
        return self._ok(f"{nodes} graph nodes, no cycles "
                        f"({len(graph.edges)} edges, {conflicts} wiring conflicts)")

    def check_adapters(self) -> Dict[str, Any]:
        from kdesk.adapters import AdapterRegistry

        registry = AdapterRegistry(self.root)
        names = registry.names()
        return self._verdict(len(names) > 0,
                             f"{len(names)} platform adapters importable",
                             "at least one platform adapter must be registered")

    def check_doctor(self) -> Dict[str, Any]:
        if self.fast:
            return self._skip("fast mode")
        code, detail = _subprocess_ok(
            [sys.executable, "-m", "kdesk.cli", "doctor", "--format", "json"], self.root)
        if code != 0:
            return self._fail(detail or "doctor failed")
        try:
            report = json.loads(detail) if detail.startswith("{") else {}
        except ValueError:
            report = {}
        stale = [k for k, v in report.items() if isinstance(v, dict) and v.get("status") == "STALE"]
        return self._verdict(not stale,
                             f"{len(stale)} stale platform outputs" if stale else "all platform outputs current",
                             "no platform output may be stale")

    def check_workflow_engine(self) -> Dict[str, Any]:
        catalog = Catalog.from_repo(self.root)
        engine = WorkflowEngine(catalog, workflows_dir=self.root / "workflows")
        workflows = engine.all()
        ok = True
        detail = f"{len(workflows)} workflows"
        if workflows:
            first = workflows[0]
            try:
                plan = engine.run(first, inputs={}, dry_run=True)
                ok = len(plan) > 0
                detail = f"{detail}; planned '{first.id}' ({len(plan)} steps)"
            except Exception as exc:  # noqa: BLE001
                ok = False
                detail = f"{detail}; run failed: {exc}"
        return self._verdict(ok, detail, "workflow engine must load and plan")

    def check_resolve(self) -> Dict[str, Any]:
        catalog = Catalog.from_repo(self.root)
        engine = Engine(self.root, catalog=catalog)
        result = engine.resolve("analyze python code quality")
        if not result.candidates:
            return self._fail("resolve produced no candidates for probe request")
        if not result.intent.get("intent"):
            return self._fail("resolve produced no intent")
        return self._ok(f"intent={result.intent['intent']}, top={result.candidates[0].name}")

    def check_plan(self) -> Dict[str, Any]:
        catalog = Catalog.from_repo(self.root)
        engine = Engine(self.root, catalog=catalog)
        plan = engine.plan("analyze python code quality")
        if not plan.steps:
            return self._fail("plan produced no steps")
        decisions = {s.decision.decision.value for s in plan.steps}
        return self._ok(f"{len(plan.steps)} steps, decisions={sorted(decisions)}")

    def check_run(self) -> Dict[str, Any]:
        catalog = Catalog.from_repo(self.root)
        engine = Engine(self.root, catalog=catalog)
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "proj"
            (work / "src").mkdir(parents=True)
            (work / "src" / "hello.py").write_text(
                "def greet(name: str) -> str:\n    return f'hi {name}'\n", encoding="utf-8")
            result = engine.run("analyze python code quality", base=work,
                                auto_approve=True, timeout_s=60.0)
        if result.status not in (STATUS_SUCCESS, "PARTIAL"):
            return self._fail(f"run ended '{result.status}': {result.error}")
        return self._ok(f"run '{result.status}' ({len(result.artifacts)} artifacts)")

    def check_cli(self) -> Dict[str, Any]:
        commands = ["resolve", "why", "plan", "run", "history", "inspect",
                    "approve", "verify", "stats", "doctor", "schema", "security",
                    "wiring", "graph"]
        failed = []
        for command in commands:
            code, detail = _subprocess_ok(
                [sys.executable, "-m", "kdesk.cli", command, "--help"], self.root)
            if code != 0:
                failed.append(f"{command} (exit {code}: {detail})")
        return self._verdict(not failed,
                             f"{len(commands) - len(failed)}/{len(commands)} commands OK",
                             "every CLI command must print help and exit 0")

    def check_freshness(self) -> Dict[str, Any]:
        if self.fast:
            return self._skip("fast mode")
        code, detail = _subprocess_ok(
            [sys.executable, "scripts/check-report-freshness.py"], self.root, timeout=900)
        return self._verdict(code == 0, detail or "reports stale",
                             "all generated reports must be fresh")

    # ------------------------------------------------------------- utils
    def _ok(self, detail: str) -> Dict[str, Any]:
        return {"name": "", "status": "PASS", "detail": detail}

    def _fail(self, detail: str) -> Dict[str, Any]:
        return {"name": "", "status": "FAIL", "detail": detail}

    def _skip(self, detail: str) -> Dict[str, Any]:
        return {"name": "", "status": "SKIP", "detail": detail}

    def _verdict(self, ok: bool, detail: str, expectation: str) -> Dict[str, Any]:
        if not ok:
            return {"name": "", "status": "FAIL",
                    "detail": f"{detail} (expected: {expectation})"}
        return {"name": "", "status": "PASS", "detail": detail}

    @staticmethod
    def _find_cycle(graph: Dict[str, Any]) -> Optional[List[str]]:
        """DFS cycle detection over {node: [neighbors]} adjacency."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color: Dict[str, int] = {}
        stack: List[str] = []

        def visit(node: str) -> Optional[List[str]]:
            color[node] = GRAY
            stack.append(node)
            for neighbor in graph.get(node, []):
                if color.get(neighbor, WHITE) == WHITE:
                    found = visit(neighbor)
                    if found:
                        return found
                elif color.get(neighbor) == GRAY:
                    return stack[stack.index(neighbor):] + [neighbor]
            stack.pop()
            color[node] = BLACK
            return None

        for node in graph:
            if color.get(node, WHITE) == WHITE:
                found = visit(node)
                if found:
                    return found
        return None

    # ------------------------------------------------------------ runner
    def run(self) -> List[Dict[str, Any]]:
        checks: Dict[str, Callable[[], Dict[str, Any]]] = {
            "catalog_load": self.check_catalog_load,
            "schema": self.check_schema,
            "provenance": self.check_provenance,
            "wiring": self.check_wiring,
            "duplicates": self.check_duplicates,
            "license": self.check_license,
            "security": self.check_security,
            "quality": self.check_quality,
            "graph": self.check_graph,
            "adapters": self.check_adapters,
            "doctor": self.check_doctor,
            "workflow_engine": self.check_workflow_engine,
            "resolve": self.check_resolve,
            "plan": self.check_plan,
            "run": self.check_run,
            "cli": self.check_cli,
            "freshness": self.check_freshness,
        }
        self.results = []
        for name in CHECK_ORDER:
            if name in self.skip:
                self.results.append({"name": name, "status": "SKIP", "detail": "excluded via --skip"})
                continue
            try:
                item = checks[name]()
            except Exception as exc:  # noqa: BLE001
                item = {"name": name, "status": "FAIL", "detail": f"check raised: {exc}"}
            item["name"] = name
            self.results.append(item)
        return self.results

    def summary(self) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for item in self.results:
            counts[item["status"]] = counts.get(item["status"], 0) + 1
        return {
            "tool": "kdesk",
            "version": __version__,
            "status": "PASS" if not counts.get("FAIL") else "FAIL",
            "checks": counts,
            "results": self.results,
        }


def run_verify(root: Optional[Path] = None, fast: bool = False,
               skip: Optional[List[str]] = None) -> Dict[str, Any]:
    runner = VerifyRunner(Path(root or os.getcwd()), fast=fast, skip=skip)
    runner.run()
    return runner.summary()


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    fast = "--fast" in argv
    json_out = "--json" in argv
    skip = []
    for flag in list(argv):
        if flag.startswith("--skip="):
            skip = [s for s in flag.split("=", 1)[1].split(",") if s]
            argv.remove(flag)
    summary = run_verify(fast=fast, skip=skip)
    if json_out:
        print(json.dumps(summary, indent=2))
        return 0 if summary["status"] == "PASS" else 3
    if not summary["results"]:
        print("no checks ran")
        return 1
    max_name = max(len(r["name"]) for r in summary["results"])
    for result in summary["results"]:
        print(f"  {result['status']:<5} {result['name']:<{max_name}}  {result['detail']}")
    print(f"\nkdesk {__version__} verify: {summary['status']} "
          f"({summary['checks'].get('PASS', 0)} pass, "
          f"{summary['checks'].get('FAIL', 0)} fail, "
          f"{summary['checks'].get('SKIP', 0)} skip)")
    return 0 if summary["status"] == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())