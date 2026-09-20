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
from kdesk.policy import PolicyEngine, PolicyEngineV2
from kdesk.provenance import Provenance, verify_wiring
from kdesk.quality import QualityReport
from kdesk.registry import Catalog, CatalogError, default_repo_root
from kdesk.security import scan_repo
from kdesk.stats import StatsError, compute as compute_stats, format_table, write_baseline
from kdesk.verify import run_verify
from kdesk.workflow import WorkflowEngine, WorkflowError
from kdesk.delegation import SubAgentResolver
from kdesk.versioning import VersionResolver, build_available_versions
from kdesk.telemetry import summary as telemetry_summary
from kdesk.marketplace import Marketplace


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
        stats = compute_stats(root, fast=args.fast)
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
    """Doctor command with multiple modes."""
    registry = Path(args.root).resolve() if args.root else default_repo_root()
    adapters = AdapterRegistry(registry)
    base = Path(args.base).resolve() if args.base else Path.cwd()
    doctor = Doctor(adapters, base=base, registry_root=registry)

    # CI mode: run diagnostics and exit with code based on threshold
    if args.ci:
        return _cmd_doctor_ci(args, doctor)

    # Route to appropriate mode
    if args.mode == "check":
        return _cmd_doctor_check(args, doctor)
    elif args.mode == "diagnose":
        return _cmd_doctor_diagnose(args, doctor)
    elif args.mode == "fix":
        return _cmd_doctor_fix(args, doctor)
    elif args.mode == "scan":
        return _cmd_doctor_scan(args, doctor)
    else:
        # Default to check for backwards compatibility
        return _cmd_doctor_check(args, doctor)


def _cmd_doctor_check(args, doctor=None) -> int:
    """Original install verification."""
    if doctor is None:
        registry = Path(args.root).resolve() if args.root else default_repo_root()
        adapters = AdapterRegistry(registry)
        doctor = Doctor(adapters, base=Path(args.base).resolve() if args.base else Path.cwd())
    if args.platform:
        check = doctor.check(args.platform)
        _out(check, args.format)
        return 0
    summary = doctor.summary()
    _out(summary, args.format)
    return 0


def _cmd_doctor_diagnose(args, doctor=None) -> int:
    """Run full diagnostic pipeline."""
    if doctor is None:
        registry = Path(args.root).resolve() if args.root else default_repo_root()
        adapters = AdapterRegistry(registry)
        doctor = Doctor(adapters, base=Path(args.base).resolve() if args.base else Path.cwd(), registry_root=Path(args.root).resolve() if args.root else default_repo_root())

    result = doctor.diagnose(
        platform=args.platform,
        project_root=Path(args.project_root).resolve() if args.project_root else None,
        fix=args.fix,
        dry_run=args.dry_run,
    )

    report = result["report"]
    fix_report = result["fix_report"]

    if args.json:
        output = {"report": report.to_dict()}
        if fix_report:
            output["fix_report"] = fix_report.to_dict()
        print(json.dumps(output, indent=2, default=str))
    else:
        print(doctor.format_report(report, verbose=args.verbose))

    if fix_report:
        print("")
        print(doctor.format_fix_report(fix_report))

    # Exit code based on errors
    if report.error_count > 0:
        return 3
    return 0


def _cmd_doctor_ci(args, doctor=None) -> int:
    """CI mode: run diagnostics and exit with code based on health threshold."""
    if doctor is None:
        registry = Path(args.root).resolve() if args.root else default_repo_root()
        adapters = AdapterRegistry(registry)
        doctor = Doctor(adapters, base=Path(args.base).resolve() if args.base else Path.cwd(), registry_root=Path(args.root).resolve() if args.root else default_repo_root())

    if not args.platform:
        print("Error: --platform required for CI mode", file=sys.stderr)
        return 1

    project_root = Path(args.project_root).resolve() if args.project_root else Path.cwd()
    scan_result = doctor.scan_project(project_root)
    issues = doctor.analyze_compatibility(scan_result, args.platform)

    from kdesk.diagnostics import DiagnosticReport, ComponentReport
    from kdesk.diagnostics import Issue, Severity, Category

    # Build report
    components = {}
    for issue in issues:
        comp_key = f"{issue.component}:{issue.file}"
        if comp_key not in components:
            comp_type = "config"
            if "agent" in issue.component.lower() or "agent" in issue.file.lower():
                comp_type = "agent"
            elif "skill" in issue.component.lower() or "skill" in issue.file.lower():
                comp_type = "skill"
            elif "workflow" in issue.component.lower() or "workflow" in issue.file.lower():
                comp_type = "workflow"
            elif "command" in issue.component.lower() or "command" in issue.file.lower():
                comp_type = "command"
            components[comp_key] = ComponentReport(
                name=Path(issue.component).name if issue.component else "unknown",
                type=comp_type,
                file=issue.file,
                platform=issue.platform,
            )
        components[comp_key].issues.append(issue)

    component_list = list(components.values())
    issues_list = issues

    # Calculate score
    def calc_score(issues):
        if not issues:
            return 100
        critical = sum(1 for i in issues if i.severity == i.severity.CRITICAL)
        errors = sum(1 for i in issues if i.severity == i.severity.ERROR)
        warnings = sum(1 for i in issues if i.severity == i.severity.WARNING)
        penalty = min(critical * 20, 80) + min(errors * 10, 60) + min(warnings * 2, 40)
        return max(0, 100 - penalty)

    score = calc_score(issues_list)
    report = DiagnosticReport(
        project_root=str(Path.cwd()),
        platform=args.platform,
        score=score,
        max_score=100,
        components=component_list,
        issues=issues_list,
        scan_metadata={},
    )

    if args.json:
        output = {"report": report.to_dict()}
        print(json.dumps(output, indent=2, default=str))

    # Exit with non-zero if score below threshold
    threshold = args.threshold
    if score < threshold:
        print(f"Health score {score}% below threshold {threshold}%", file=sys.stderr)
        return 1
    return 0
    """Apply fixes for a previously diagnosed project."""
    if doctor is None:
        base = Path(args.project_root).resolve() if args.project_root else Path.cwd()
        registry = Path(args.root).resolve() if args.root else default_repo_root()

        adapters = AdapterRegistry(registry)
        doctor = Doctor(adapters, base=Path(args.base).resolve() if args.base else Path.cwd(), registry_root=registry)

    # First diagnose
    project_root = Path(args.project_root).resolve() if args.project_root else Path.cwd()
    scan_result = doctor.scan_project(project_root)
    issues = doctor.analyze_compatibility(scan_result, args.platform)

    # Apply fixes
    fix_report = doctor.apply_fixes(issues, args.platform, dry_run=args.dry_run, project_root=project_root)

    if args.json:
        print(json.dumps(fix_report.to_dict(), indent=2, default=str))
    else:
        print(doctor.format_fix_report(fix_report))

    if fix_report.failed > 0:
        return 1
    return 0


def _cmd_doctor_scan(args, doctor=None) -> int:
    """Scan a project for AI configuration."""
    if doctor is None:
        registry = Path(args.root).resolve() if args.root else default_repo_root()
        adapters = AdapterRegistry(registry)
        doctor = Doctor(adapters, base=Path(args.base).resolve() if args.base else Path.cwd(), registry_root=Path(args.root).resolve() if args.root else default_repo_root())

    project_root = Path(args.project_root).resolve() if args.project_root else Path.cwd()
    scan_result = doctor.scan_project(project_root)

    if args.json:
        print(json.dumps(scan_result.to_dict(), indent=2, default=str))
    else:
        print(f"Project: {scan_result.project_root}")
        print(f"Detected Platform: {scan_result.platform or 'unknown'}")
        print(f"Agents: {len(scan_result.agents)}")
        print(f"Skills: {len(scan_result.skills)}")
        print(f"Commands: {len(scan_result.commands)}")
        print(f"Workflows: {len(scan_result.workflows)}")
        print(f"Config Files: {len(scan_result.configuration)}")
        if scan_result.errors:
            print(f"Errors: {len(scan_result.errors)}")
        if scan_result.warnings:
            print(f"Warnings: {len(scan_result.warnings)}")
        print(f"Metadata: {scan_result.metadata}")

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


def _cmd_policy(args) -> int:
    catalog = _catalog(args)
    engine = PolicyEngineV2()
    
    # Load custom policy file if provided
    if args.policy_file:
        policy_file = Path(args.policy_file)
        if policy_file.exists():
            import yaml
            with open(policy_file, 'r') as f:
                if policy_file.suffix in ['.yaml', '.yml']:
                    custom_rules = yaml.safe_load(f)
                else:
                    import json
                    custom_rules = json.load(f)
                # Add custom rules to engine
                for rule_data in custom_rules.get("rules", []):
                    from kdesk.policy import PolicyRuleV2, Severity
                    rule = PolicyRuleV2(
                        id=rule_data["id"],
                        name=rule_data["name"],
                        description=rule_data.get("description", ""),
                        severity=Severity(rule_data.get("severity", "warning")),
                        condition=rule_data.get("condition", ""),
                        message=rule_data.get("message", ""),
                        fix_hint=rule_data.get("fix_hint", "")
                    )
                    engine.rules.append(rule)
    
    result = engine.evaluate(catalog)
    
    if args.format == "json":
        print(json.dumps({
            "violations": result["violations"],
            "passed": result["passed"],
            "total_rules": result["total_rules"]
        }, indent=2, default=str))
    else:
        if result["violations"]:
            for v in result["violations"]:
                print(f"[{v['severity'].upper()}] {v['rule_id']}: {v['message']} (target: {v['target']})")
            print(f"\nPassed: {result['passed']}/{result['total_rules']} rules")
            print(f"Violations: {len(result['violations'])}")
        else:
            print(f"All {result['total_rules']} policy rules passed!")
    
    return 3 if result["violations"] else 0


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


def _cmd_skill_publish(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    catalog = Catalog.from_repo(root)
    skill = catalog.get_skill(args.skill_id)
    if not skill:
        print(f"ERROR: Skill '{args.skill_id}' not found in catalog", file=sys.stderr)
        return 1
    mp = Marketplace(root)
    try:
        result = mp.publish(skill.source_path, force=args.force)
        print(json.dumps(result, indent=2, default=str))
        return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def _cmd_skill_install(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    mp = Marketplace(root)
    entry = mp.resolve(args.skill_spec)
    if entry is None:
        print(f"NOT FOUND: {args.skill_spec} (no version matches)", file=sys.stderr)
        return 1
    print(json.dumps({"status": "resolved", "name": entry.name, "version": entry.version,
                       "checksum": entry.checksum, "dependencies": entry.dependencies}, indent=2))
    return 0


def _cmd_skill_search(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    mp = Marketplace(root)
    results = mp.search(args.query, limit=args.limit)
    if not results:
        print("No results found.")
        return 0
    for e in results:
        print(f"  {e.name}@{e.version}  [{e.category}]  {e.description[:60]}")
    return 0


def _cmd_skill_list(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    mp = Marketplace(root)
    entries = mp.list_all()
    stats = mp.stats()
    print(f"Registry: {mp.registry_path} ({stats['unique_skills']} skills, {stats['total_versions']} versions)")
    for e in entries:
        print(f"  {e.name}@{e.version}  [{e.category}]")
    return 0


def _cmd_skill(args) -> int:
    if args.skill_command == "publish":
        return _cmd_skill_publish(args)
    elif args.skill_command == "install":
        return _cmd_skill_install(args)
    elif args.skill_command == "search":
        return _cmd_skill_search(args)
    elif args.skill_command == "list":
        return _cmd_skill_list(args)
    else:
        print("Usage: kdesk skill {publish|install|search|list} ...")
        return 2


def _cmd_delegate(args) -> int:
    catalog = _catalog(args)
    resolver = SubAgentResolver(catalog)
    plan = resolver.resolve(args.agent, input_data={})
    if plan is None:
        agent = catalog.get_agent(args.agent)
        if not agent:
            print(f"ERROR: Agent '{args.agent}' not found", file=sys.stderr)
            return 1
        print(f"Agent '{args.agent}' has no sub_agents declared.")
        return 0
    data = plan.summary()
    print(json.dumps(data, indent=2, default=str))
    return 0 if plan.all_succeeded else 3


def _cmd_version_resolve(args) -> int:
    catalog = _catalog(args)
    all_names = list(catalog.agents.keys()) + list(catalog.skills.keys())
    available = build_available_versions({n: True for n in all_names})
    resolver = VersionResolver()
    result = resolver.resolve(args.spec, available)
    if result is None:
        print(f"NO MATCH: {args.spec}", file=sys.stderr)
        return 1
    # Check for breaking change if we have a current version
    spec_parts = result.split("@")
    if len(spec_parts) == 2:
        check = resolver.check_breaking_change("1.0.0", spec_parts[1])
        print(json.dumps({"resolved": result, **({"breaking_change_check": check})}, indent=2))
    else:
        print(result)
    return 0


def _cmd_telemetry(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    stats = telemetry_summary(root)
    print(json.dumps(stats, indent=2))
    return 0


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
    st.add_argument("--fast", action="store_true", help="skip slow platform output file count")

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

    d = sub.add_parser("doctor", parents=[root_parent], help="verify installations + project diagnostics")
    d.add_argument("--platform", default=None, help="target platform (e.g., claude_code, opencode, codex_cli)")
    d.add_argument("--base", default=None, help="base directory for install check")
    d.add_argument("--format", choices=["json", "table"], default="json")
    d.add_argument("--mode", choices=["check", "diagnose", "fix", "scan"], default="check",
                   help="doctor mode: check (install verification), diagnose (full pipeline), fix (apply fixes), scan (scan project)")
    d.add_argument("--project-root", default=None, help="project directory to scan")
    d.add_argument("--fix", action="store_true", help="automatically fix fixable issues (diagnose mode)")
    d.add_argument("--dry-run", action="store_true", help="preview fixes without applying")
    d.add_argument("--json", action="store_true", help="output JSON")
    d.add_argument("--verbose", action="store_true", help="show detailed issue explanations")
    # CI mode
    d.add_argument("--ci", action="store_true", help="CI mode: exit with non-zero code if health below threshold")
    d.add_argument("--threshold", type=int, default=90, help="CI health threshold (0-100), exit non-zero if below")

    s = sub.add_parser("security", parents=[root_parent], help="secret scan")
    s.add_argument("--json", action="store_true")

    pv = sub.add_parser("provenance", parents=[root_parent], help="JSON->YAML traceability")
    pv.add_argument("--wiring", action="store_true", help="verify wiring evidence instead")

    q = sub.add_parser("quality", parents=[root_parent], help="content quality report")
    q.add_argument("--format", choices=["json", "table"], default="json")

    l = sub.add_parser("license", parents=[root_parent], help="license audit")
    l.add_argument("--format", choices=["json", "table"], default="json")

    pl = sub.add_parser("policy", parents=[root_parent], help="policy-as-code engine")
    pl.add_argument("--format", choices=["json", "table"], default="json")
    pl.add_argument("--policy-file", default=None, help="custom policy file (JSON/YAML)")

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

    # Skill marketplace commands
    sk = sub.add_parser("skill", parents=[root_parent],
                        help="skill marketplace (publish, install, search, list)")
    sk_sub = sk.add_subparsers(dest="skill_command")

    sk_pub = sk_sub.add_parser("publish", help="publish a skill to the local registry")
    sk_pub.add_argument("skill_id", help="skill ID to publish")
    sk_pub.add_argument("--force", action="store_true", help="overwrite existing version")

    sk_inst = sk_sub.add_parser("install", help="resolve a skill spec (name@semver)")
    sk_inst.add_argument("skill_spec", help="skill@version or skill_id")

    sk_search = sk_sub.add_parser("search", help="search the registry")
    sk_search.add_argument("query", nargs="?", default="", help="search query")
    sk_search.add_argument("--limit", type=int, default=20)

    sk_list = sk_sub.add_parser("list", help="list available skills")

    dg = sub.add_parser("delegate", parents=[root_parent],
                        help="resolve sub-agent delegation for an agent")
    dg.add_argument("agent", help="agent name with sub_agents")

    vr = sub.add_parser("resolve-version", parents=[root_parent],
                        help="resolve a name@semver spec against the catalog")
    vr.add_argument("spec", help="e.g. my-agent@^2.0 or terraform-infrastructure")

    tl = sub.add_parser("telemetry", parents=[root_parent],
                        help="show anonymous usage stats")

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
        "policy": _cmd_policy,
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
        "skill": _cmd_skill,
        "delegate": _cmd_delegate,
        "resolve-version": _cmd_version_resolve,
        "telemetry": _cmd_telemetry,
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