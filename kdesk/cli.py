"""kdesk CLI - Universal Agent/Skill/Workflow registry orchestration.

Exit codes: 0 = success, 1 = fatal error, 2 = usage error,
3 = problems found (validation, drift, doctor, audits).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk import __version__
from kdesk.adapters import AdapterRegistry, SupportLevel
from kdesk.capabilities import CapabilityIndex
from kdesk.doctor import Doctor
from kdesk.duplicates import DuplicateDetector, DuplicatePolicy
from kdesk.engine import (STATUS_BLOCKED, STATUS_CANCELLED, STATUS_FAILED,
                          STATUS_TIMEOUT, STATUS_WAITING_APPROVAL, Engine)
from kdesk.graph import CatalogGraph
from kdesk.installer import Installer, InstallError
from kdesk.license import LicenseAudit, LicensePolicy
from kdesk.provenance import Provenance, verify_wiring
from kdesk.quality import QualityReport
from kdesk.registry import Catalog, CatalogError, default_repo_root
from kdesk.security import scan_repo
from kdesk.stats import StatsError, compute as compute_stats, format_table, write_baseline
from kdesk.workflow import WorkflowEngine, WorkflowError
from kdesk.verify import run_verify


def _out(data: Any, fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        if isinstance(data, dict) and "rows" in data:
            for row in data["rows"]:
                print(row)
        else:
            print(json.dumps(data, indent=2, default=str))


def _catalog(args) -> Catalog:
    root = Path(args.root) if args.root else default_repo_root()
    return Catalog.from_repo(root)


def _subprocess_ok(argv: List[str], root: Path,
                   timeout: float = 120.0) -> tuple:
    import subprocess
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, cwd=str(root),
            timeout=timeout, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"
    detail = (proc.stdout or "").strip()
    if proc.returncode != 0 and proc.stderr.strip():
        detail = f"{detail}\n{proc.stderr.strip()}"
    return proc.returncode, detail


def _cmd_stats(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    try:
        stats = compute_stats(root)
    except StatsError as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 1
    if args.baseline:
        path = write_baseline(root)
        print(f"baseline written: {path}", flush=True)
        return 0
    if args.format == "table":
        print(format_table(stats))
        return 0
    print(json.dumps(stats, indent=2, default=str))
    return 0


def _cmd_registry(args) -> int:
    catalog = _catalog(args)
    if args.search:
        hits = catalog.search(args.search)
        for h in hits:
            print(f"{h.type:6s} {h.name:40s} {h.category}")
        return 0
    stats = catalog.stats()
    if args.errors and catalog.errors:
        for e in catalog.errors[:50]:
            print(f"ERROR: {e}")
    print(json.dumps(stats, indent=2, default=str))
    return 1 if catalog.errors else 0


def _cmd_graph(args) -> int:
    catalog = _catalog(args)
    root = Path(args.root) if args.root else default_repo_root()
    graph = CatalogGraph(catalog, wiring_path=root / "skills" / "wiring.json")
    if args.agent:
        for link in graph.agent_skills(args.agent):
            print(f"{args.agent} -> {link['skill']}  [evidence={link['evidence']}, manual={link['manual']}]")
        return 0
    print(json.dumps(graph.summary(), indent=2, default=str))
    return 0


def _cmd_capabilities(args) -> int:
    catalog = _catalog(args)
    idx = CapabilityIndex(list(catalog.agents.values()) + list(catalog.skills.values()))
    if args.tool:
        for defn, cap in idx.capabilities_for_tool(args.tool):
            print(f"{defn} :: {cap}")
        return 0
    print(json.dumps(idx.summary(), indent=2, default=str))
    return 0


def _cmd_workflow(args) -> int:
    catalog = _catalog(args)
    root = Path(args.root) if args.root else default_repo_root()
    engine = WorkflowEngine(catalog, workflows_dir=root / "workflows")
    if args.validate:
        wf = engine.load(args.validate)
        problems = engine.validate(wf)
        if problems:
            for p in problems:
                print(f"PROBLEM: {p}")
            return 3
        print(f"OK: {wf.id} ({len(wf.steps)} steps)")
        return 0
    if args.run:
        wf = engine.load(args.run)
        try:
            result = engine.run(wf, dry_run=not args.execute)
        except WorkflowError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(json.dumps(result, indent=2, default=str))
        return 0
    print(json.dumps(engine.summary(), indent=2, default=str))
    return 0


def _cmd_adapters(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    summary = adapters.summary()
    if args.platform:
        a = adapters.get(args.platform)
        if a is None:
            print(f"UNKNOWN platform: {args.platform}")
            return 1
        print(json.dumps(a.verify(), indent=2, default=str))
        return 0
    _out(summary, args.format)
    return 0


def _cmd_install(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters, dry_run=args.dry_run,
                          home_dir=Path(args.home) if args.home else None)
    try:
        result = installer.install(
            args.platform, target=args.target,
            base=Path(args.base) if args.base else None,
            scope=args.scope, tool=args.tool,
            agents=set(args.agents.split(",")) if args.agents else None,
            category=set(args.category.split(",")) if args.category else None,
            link=args.link)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        if str(exc).startswith(("unknown scope", "unknown tool",
                                "filter (scope", "filter (tool",
                                "filter (agents", "filter (category")):
            return 2
        return 1
    total = sum(r.get("files", 0) for r in result.get("results", []))
    if args.platform == "opencode" and total > 119:
        print(f"WARNING: opencode supports ~119 subagents upstream; "
              f"{total} definitions selected, excess will not be usable",
              file=sys.stderr)
    print(json.dumps(result, indent=2, default=str))
    return 0


def _cmd_uninstall(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters, dry_run=args.dry_run)
    try:
        result = installer.uninstall(args.platform,
                                     base=Path(args.base) if args.base else None)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, indent=2, default=str))
    return 0


def _cmd_drift(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters)
    try:
        report = installer.drift(args.platform,
                                 base=Path(args.base) if args.base else None)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["clean"] else 3


def _cmd_status(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters)
    print(json.dumps(installer.status(base=Path(args.base) if args.base else None),
                     indent=2, default=str))
    return 0


def _cmd_rollback(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters, dry_run=args.dry_run)
    try:
        result = installer.rollback(args.platform,
                                    base=Path(args.base) if args.base else None)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, indent=2, default=str))
    return 0


def _cmd_doctor(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    doctor = Doctor(adapters, base=Path(args.base) if args.base else None)
    if args.platform:
        check = doctor.check(args.platform)
        print(json.dumps(check, indent=2, default=str))
        return 0
    summary = doctor.summary()
    _out(summary, args.format)
    return 0


def _cmd_security(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    report = scan_repo(root, root / "reports" / "security-exceptions.json")
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        for f in report["findings"]:
            print(f"[{f['severity']}] {f['definition']} {f['field']} -> {f['pattern']}")
        if not report["findings"]:
            print("no secrets detected")
    return 3 if report["blocking_count"] else 0


def _cmd_provenance(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    if args.wiring:
        result = verify_wiring(root)
    else:
        result = Provenance(root).verify()
    print(json.dumps(result, indent=2, default=str))
    return 3 if result.get("problems") else 0


def _cmd_quality(args) -> int:
    catalog = _catalog(args)
    report = QualityReport(catalog).score()
    _out(report, args.format)
    return 3 if report["low_score_count"] else 0


def _cmd_license(args) -> int:
    catalog = _catalog(args)
    root = Path(args.root) if args.root else default_repo_root()
    policy = LicensePolicy.load(root / "reports" / "license-policy.json")
    report = LicenseAudit(catalog).audit(policy=policy)
    _out(report, args.format)
    return 3 if report["unresolved_count"] else 0


def _cmd_duplicates(args) -> int:
    catalog = _catalog(args)
    root = Path(args.root) if args.root else default_repo_root()
    policy = DuplicatePolicy.load(root / "reports" / "duplicate-classifications.json")
    report = DuplicateDetector(catalog).detect(policy=policy)
    _out(report, args.format)
    return 3 if report["unresolved_count"] else 0


def _cmd_resolve(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    result = engine.resolve(args.request, top=args.top,
                            probe_environment=not args.no_env_probe)
    data = result.to_dict()
    if not args.json:
        print(f"intent: {data.get('intent', {}).get('intent', 'unknown')}")
        for i, cand in enumerate(data.get("candidates", []), 1):
            print(f"  {i}. {cand.get('name')} [{cand.get('definition_type')}] "
                  f"score={cand.get('score')} risk={cand.get('risk')}")
        if data.get("missing_requirements"):
            print("missing requirements:")
            for name, info in data["missing_requirements"].items():
                print(f"  - {name}: {info}")
    else:
        print(json.dumps(data, indent=2, default=str))
    return 0 if data.get("candidates") else 3


def _cmd_why(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    data = engine.why(args.request, args.target)
    if data is None:
        print(f"UNKNOWN target: {args.target}")
        return 1
    print(json.dumps(data, indent=2, default=str))
    return 0


def _cmd_plan(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    plan = engine.plan(args.request)
    data = plan.to_dict()
    if not args.json:
        print(f"steps: {len(data.get('steps', []))}")
        for step in data.get("steps", []):
            decision = step.get("decision", "allowed")
            print(f"  {step.get('index')}. [{decision}] {step.get('description')}")
    else:
        print(json.dumps(data, indent=2, default=str))
    return 0


def _cmd_run(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    base = Path(args.base) if args.base else Path.cwd()
    if args.execution_id:
        existing = engine.inspect(args.execution_id)
        if existing is not None and existing["execution"]["status"] == STATUS_WAITING_APPROVAL:
            step = int(existing["execution"].get("approval_step", -1))
            approvals = [a for a in existing["approvals"] if a.get("step") == step]
            if any(a.get("state") in ("approved", "auto_approved") for a in approvals):
                result = engine.resume(args.execution_id, base=base,
                                       timeout_s=args.timeout,
                                       auto_approve=args.auto_approve)
            else:
                state = approvals[-1]["state"] if approvals else "pending"
                print(f"execution {args.execution_id} is waiting at step {step} "
                      f"(state={state}); approve it first", file=sys.stderr)
                return 3
        else:
            result = engine.run(args.request, base=base,
                                auto_approve=args.auto_approve,
                                timeout_s=args.timeout,
                                execution_id=args.execution_id)
    else:
        result = engine.run(args.request, base=base,
                            auto_approve=args.auto_approve,
                            timeout_s=args.timeout,
                            execution_id=args.execution_id,
                            dry_run=args.dry_run)
    data = result.to_dict()
    if not args.json:
        print(f"execution: {data['execution_id']} status={data['status']} "
              f"steps={len(data.get('steps', []))} artifacts={len(data.get('artifacts', []))}")
        if data.get("error"):
            print(f"error: {data['error']}")
    else:
        print(json.dumps(data, indent=2, default=str))
    if data["status"] == STATUS_BLOCKED:
        return 3
    if data["status"] in (STATUS_FAILED, STATUS_TIMEOUT, STATUS_CANCELLED):
        return 1
    return 0


def _cmd_history(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    print(json.dumps(engine.history(limit=args.limit), indent=2, default=str))
    return 0


def _cmd_inspect(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    data = engine.inspect(args.execution_id)
    if data is None:
        print(f"UNKNOWN execution: {args.execution_id}")
        return 1
    print(json.dumps(data, indent=2, default=str))
    return 0


def _cmd_approve(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    updated = engine.approve(args.execution_id, args.step, args.decision == "yes",
                             note=args.note, decided_by=args.by)
    if updated is None:
        print(f"UNKNOWN execution: {args.execution_id}")
        return 1
    print(json.dumps(updated, indent=2, default=str))
    return 0


def _cmd_verify(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    summary = run_verify(root, fast=args.fast, skip=args.skip)
    counts = summary.get("checks", {})
    if args.json:
        print(json.dumps(summary, indent=2, default=str))
    else:
        width = max((len(r["name"]) for r in summary["results"]), default=8)
        for r in summary["results"]:
            print(f"  {r['status']:5s} {r['name']:<{width}} {r['detail']}")
        print(f"kdesk {__version__} verify: {summary['status']} "
              f"({counts.get('PASS', 0)} pass, {counts.get('FAIL', 0)} fail, "
              f"{counts.get('SKIP', 0)} skip)")
    if summary["status"] == "FAIL":
        return 3
    if summary["status"] == "ERROR":
        return 1
    return 0


def _cmd_schema(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    code, detail = _subprocess_ok(
        [sys.executable, "scripts/schema-check.py"], root, timeout=600)
    if detail:
        print(detail)
    if code != 0:
        print(f"FATAL: schema-check failed (exit {code})", file=sys.stderr)
    return code


def _cmd_wiring(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    result = verify_wiring(root)
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        for issue in result.get("problems", []):
            print(f"PROBLEM: {issue}")
        print(f"wiring: {len(result.get('verified', []))} verified, "
              f"{len(result.get('problems', []))} problems")
    return 3 if result.get("problems") else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kdesk", description="Universal AI Agent + Skill + Workflow Registry")
    p.add_argument("--version", action="version", version=f"kdesk {__version__}")
    p.add_argument("--root", default=None, help="repository root (default: derived from package location)")
    sub = p.add_subparsers(dest="command")

    root_parent = argparse.ArgumentParser(add_help=False)
    root_parent.add_argument("--root", default=None, help="repository root (default: derived from package location)")

    st = sub.add_parser("stats", parents=[root_parent], help="authoritative catalog statistics")
    st.add_argument("--format", choices=["json", "table"], default="json")
    st.add_argument("--baseline", action="store_true", help="write reports/baseline-stats.json")

    r = sub.add_parser("registry", parents=[root_parent], help="catalog queries and stats")
    r.add_argument("--search", default=None, help="text search over names/descriptions/tags")
    r.add_argument("--errors", action="store_true", help="print load errors")

    g = sub.add_parser("graph", parents=[root_parent], help="agent->skill wiring graph")
    g.add_argument("--agent", default=None, help="show skills for an agent")

    c = sub.add_parser("capabilities", parents=[root_parent], help="capability/tool index")
    c.add_argument("--tool", default=None, help="capabilities invoking a tool")

    w = sub.add_parser("workflow", parents=[root_parent], help="workflow engine")
    w.add_argument("--validate", metavar="ID", help="validate a workflow")
    w.add_argument("--run", metavar="ID", help="run a workflow (dry-run by default)")
    w.add_argument("--execute", action="store_true", help="actually run capability commands")

    a = sub.add_parser("adapters", parents=[root_parent], help="platform adapter matrix")
    a.add_argument("--platform", default=None, help="single platform")
    a.add_argument("--format", choices=["json", "table"], default="json")

    i = sub.add_parser("install", parents=[root_parent], help="install platform artifacts")
    i.add_argument("platform")
    i.add_argument("--target", choices=["project", "home"], default="project")
    i.add_argument("--base", default=None, help="install base dir")
    i.add_argument("--home", default=None, help="home dir for ~-prefixed targets")
    i.add_argument("--scope", choices=None, default=None,
                   help="restrict install to one definition kind (agents|skills)")
    i.add_argument("--tool", default=None,
                   help="restrict install to definitions invoking a tool")
    i.add_argument("--agents", default=None,
                   help="restrict install to comma-separated definition ids")
    i.add_argument("--category", default=None,
                   help="restrict install to comma-separated categories")
    i.add_argument("--link", action="store_true",
                   help="create symlinks instead of copying")
    i.add_argument("--dry-run", action="store_true")

    u = sub.add_parser("uninstall", parents=[root_parent], help="remove installed artifacts")
    u.add_argument("platform")
    u.add_argument("--base", default=None, help="install base dir")
    u.add_argument("--dry-run", action="store_true")

    dr = sub.add_parser("drift", parents=[root_parent], help="detect modified/missing installs")
    dr.add_argument("--platform", default=None, help="single platform (default: all)")
    dr.add_argument("--base", default=None, help="install base dir")

    stt = sub.add_parser("status", parents=[root_parent], help="show installation manifest")
    stt.add_argument("--base", default=None, help="install base dir")

    rb = sub.add_parser("rollback", parents=[root_parent], help="restore from backup")
    rb.add_argument("platform")
    rb.add_argument("--base", default=None, help="install base dir")
    rb.add_argument("--dry-run", action="store_true")

    d = sub.add_parser("doctor", parents=[root_parent], help="verify installations")
    d.add_argument("--platform", default=None)
    d.add_argument("--base", default=None)
    d.add_argument("--format", choices=["json", "table"], default="json")

    s = sub.add_parser("security", parents=[root_parent], help="secret scan")
    s.add_argument("--json", action="store_true")

    pv = sub.add_parser("provenance", parents=[root_parent], help="JSON->YAML traceability")
    pv.add_argument("--wiring", action="store_true", help="verify wiring evidence instead")

    q = sub.add_parser("quality", parents=[root_parent], help="content quality report")
    q.add_argument("--format", choices=["json", "table"], default="json")

    l = sub.add_parser("license", parents=[root_parent], help="license audit")
    l.add_argument("--format", choices=["json", "table"], default="json")

    du = sub.add_parser("duplicates", parents=[root_parent], help="duplicate family detection")
    du.add_argument("--format", choices=["json", "table"], default="json")

    rv = sub.add_parser("resolve", parents=[root_parent],
                        help="classify intent and find candidate definitions")
    rv.add_argument("request")
    rv.add_argument("--top", type=int, default=8)
    rv.add_argument("--no-env-probe", action="store_true")
    rv.add_argument("--json", action="store_true")

    wh = sub.add_parser("why", parents=[root_parent],
                        help="explain why a definition matched a request")
    wh.add_argument("request")
    wh.add_argument("target")

    pn = sub.add_parser("plan", parents=[root_parent],
                        help="build and evaluate an execution plan")
    pn.add_argument("request")
    pn.add_argument("--json", action="store_true")

    rn = sub.add_parser("run", parents=[root_parent],
                        help="run the full orchestration pipeline")
    rn.add_argument("request")
    rn.add_argument("--base", default=None, help="project base dir (default: cwd)")
    rn.add_argument("--auto-approve", action="store_true")
    rn.add_argument("--timeout", type=float, default=120.0)
    rn.add_argument("--execution-id", default=None)
    rn.add_argument("--dry-run", action="store_true")
    rn.add_argument("--json", action="store_true")

    h = sub.add_parser("history", parents=[root_parent],
                       help="list past executions")
    h.add_argument("--limit", type=int, default=20)

    ins = sub.add_parser("inspect", parents=[root_parent],
                         help="show execution record, events, artifacts, approvals")
    ins.add_argument("execution_id")

    ap = sub.add_parser("approve", parents=[root_parent],
                        help="approve or reject a pending step")
    ap.add_argument("execution_id")
    ap.add_argument("step", type=int)
    ap.add_argument("decision", choices=["yes", "no"])
    ap.add_argument("--note", default="")
    ap.add_argument("--by", default="kdesk")

    vf = sub.add_parser("verify", parents=[root_parent],
                        help="run the platform verification gate")
    vf.add_argument("--fast", action="store_true", help="skip slow checks")
    vf.add_argument("--skip", default=None, help="comma-separated check names to skip")
    vf.add_argument("--json", action="store_true")

    sc = sub.add_parser("schema", parents=[root_parent],
                        help="run the source schema check")
    sc.add_argument("--json", action="store_true")

    wg = sub.add_parser("wiring", parents=[root_parent],
                        help="verify agent->skill wiring evidence")
    wg.add_argument("--json", action="store_true")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    handlers = {
        "stats": _cmd_stats,
        "registry": _cmd_registry,
        "graph": _cmd_graph,
        "capabilities": _cmd_capabilities,
        "workflow": _cmd_workflow,
        "adapters": _cmd_adapters,
        "install": _cmd_install,
        "uninstall": _cmd_uninstall,
        "drift": _cmd_drift,
        "status": _cmd_status,
        "rollback": _cmd_rollback,
        "doctor": _cmd_doctor,
        "security": _cmd_security,
        "provenance": _cmd_provenance,
        "quality": _cmd_quality,
        "license": _cmd_license,
        "duplicates": _cmd_duplicates,
        "resolve": _cmd_resolve,
        "why": _cmd_why,
        "plan": _cmd_plan,
        "run": _cmd_run,
        "history": _cmd_history,
        "inspect": _cmd_inspect,
        "approve": _cmd_approve,
        "verify": _cmd_verify,
        "schema": _cmd_schema,
        "wiring": _cmd_wiring,
    }
    handler = handlers.get(args.command)
    if handler is None:
        build_parser().print_help()
        return 2
    try:
        return handler(args)
    except CatalogError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())