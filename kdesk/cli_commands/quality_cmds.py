"""Quality/doctor commands: doctor modes, security, audits, policy, verify."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from kdesk.adapters import AdapterRegistry
from kdesk.doctor import Doctor
from kdesk.duplicates import DuplicateDetector, DuplicatePolicy
from kdesk.license import LicenseAudit, LicensePolicy
from kdesk.policy import PolicyEngineV2
from kdesk.provenance import Provenance, verify_wiring
from kdesk.quality import QualityReport
from kdesk.registry import default_repo_root
from kdesk.security import scan_repo
from kdesk.verify import run_verify
from kdesk import __version__

from kdesk.cli_commands.helpers import _catalog, _out, _subprocess_ok


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


def _cmd_doctor_fix(args, doctor=None) -> int:
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
                    import json as _json
                    custom_rules = _json.load(f)
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
