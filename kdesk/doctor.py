"""kdesk doctor: developer-facing compatibility, diagnosis, repair, and validation system.

Core pipeline:
  PROJECT -> SCAN -> ANALYZE -> DETECT -> COMPATIBILITY -> FIX -> VALIDATE -> REPORT

Preserves existing install verification behavior while adding:
- Project scanner for AI development configuration
- Compatibility engine with severity scoring
- Automatic fix engine with validation
- Diagnostic reports (human + JSON)
- CI mode with exit codes
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.adapters import AdapterRegistry
from kdesk.capabilities import CapabilityIndex
from kdesk.registry import Catalog, default_repo_root
from kdesk.scanner import ProjectScanner, ProjectScanResult, scan_project
from kdesk.compatibility import CompatibilityEngine, analyze_compatibility
from kdesk.diagnostics import (
    DiagnosticReport, Issue, Severity, Category, FixReport, FixResult,
    ComponentReport, ComponentReport as ComponentReportType
)
from kdesk.fixer import FixEngine, apply_fixes
from kdesk.registry import Catalog
from kdesk.contracts import Contract, derive_contract


class Doctor:
    """Extended Doctor: install verification + project diagnostics + repair."""

    def __init__(
        self,
        adapters: AdapterRegistry,
        base: Optional[Path] = None,
        registry_root: Optional[Path] = None,
    ):
        self.adapters = adapters
        self.base = Path(base) if base else Path.cwd()
        self.registry_root = Path(registry_root).resolve() if registry_root else default_repo_root()
        self.catalog = Catalog.from_repo(self.registry_root)
        self.scanner = ProjectScanner(self.base, self.registry_root)

    # ------------------------------------------------------------------------
    # EXISTING: Install verification (preserved)
    # ------------------------------------------------------------------------
    def check(self, platform: str) -> Dict[str, Any]:
        adapter = self.adapters.get(platform)
        if adapter is None:
            return {"platform": platform, "status": "UNKNOWN", "scanned_files": 0, "note": "no adapter"}
        if not adapter.exists():
            return {"platform": platform, "status": "NOT_GENERATED", "scanned_files": 0, "note": "platform-agents/<name> missing; run converter"}
        generated = adapter.items_emitted()
        if generated == 0:
            return {"platform": platform, "status": "EMPTY", "scanned_files": 0, "note": "generated dir has no item files"}
        installed = self._find_installed(adapter)
        scanned = sum(1 for p in installed.rglob("*") if p.is_file()) if installed else 0
        if not installed:
            return {
                "platform": platform,
                "status": "MISSING",
                "scanned_files": scanned,
                "expected": generated,
                "installed": 0,
            }
        return {
            "platform": platform,
            "status": "OK",
            "scanned_files": scanned,
            "expected": generated,
            "installed": scanned,
            "install_target": str(installed),
        }

    def _find_installed(self, adapter) -> Optional[Path]:
        name = adapter.name
        home_candidates = {
            "claude_code": [Path.home() / ".claude"],
            "goose": [Path.home() / ".config" / "goose" / "recipes"],
            "opencode": [Path.home() / ".config" / "opencode" / "plugin"],
        }
        project_candidates = {
            "claude_code": [self.base / ".claude"],
            "cursor": [self.base / ".cursor" / "rules"],
            "github_copilot": [self.base / ".github" / "instructions"],
            "windsurf": [self.base / ".windsurf" / "rules"],
            "opencode": [self.base / ".opencode"],
            "codex_cli": [self.base / ".agents" / "skills"],
            "gemini_cli": [self.base / ".gemini" / "skills"],
            "antigravity": [self.base / ".agent" / "skills"],
            "devin": [self.base / ".devin" / "skills"],
            "zed": [self.base / ".agents" / "skills"],
            "cline": [self.base / ".clinerules" / "skills"],
            "roo_code": [self.base / ".roo" / "skills"],
            "kilo_code": [self.base / ".kilocode" / "skills"],
            "trae": [self.base / ".trae" / "skills"],
            "qwen_code": [self.base / ".qwen" / "skills"],
            "kiro": [self.base / ".kiro" / "skills"],
            "junie": [self.base / ".junie" / "skills"],
            "zencoder": [self.base / ".agents" / "skills"],
            "amp": [self.base / ".agents" / "skills"],
            "factory_droid": [self.base / ".factory" / "skills"],
            "crush": [self.base / ".crush" / "skills"],
            "mcpjam": [self.base / ".mcpjam" / "skills"],
            "mux": [self.base / ".mux" / "skills"],
            "pi": [self.base / ".pi" / "skills"],
            "qoder": [self.base / ".qoder" / "skills"],
            "codebuddy": [self.base / ".codebuddy" / "skills"],
            "commandcode": [self.base / ".commandcode" / "skills"],
            "neovate": [self.base / ".neovate" / "skills"],
            "grok_build": [self.base / ".grok" / "rules"],
            "amazon_q": [self.base / ".amazonq" / "rules"],
            "augment": [self.base / ".augment" / "rules"],
            "firebase_studio": [self.base / ".idx" / "rules"],
            "continue": [self.base / ".continue" / "rules"],
            "tabnine": [self.base / ".tabnine" / "guidelines"],
            "supermaven": [self.base / ".supermaven" / "rules"],
            "openhands": [self.base / ".openhands" / "microagents"],
            "google_jules": [self.base / "AGENTS.md"],
            "warp": [self.base / "WARP.md"],
            "codegpt": [self.base / "AGENTS.md"],
            "cody": [self.base / ".vscode"],
            "firebender": [self.base / ".firebender"],
        }
        for cand in home_candidates.get(name, []) + project_candidates.get(name, []):
            if cand.exists():
                return cand if cand.is_dir() or cand.is_file() else None
        return None

    def check_all(self) -> List[Dict[str, Any]]:
        return [self.check(a.name) for a in self.adapters.all()]

    def summary(self) -> Dict[str, Any]:
        rows = self.check_all()
        from collections import Counter
        by_status = Counter(r["status"] for r in rows)
        total_scanned = sum(r["scanned_files"] for r in rows)
        return {
            "platforms": len(rows),
            "status_counts": dict(by_status),
            "files_scanned": total_scanned,
            "rows": rows,
        }

    # ------------------------------------------------------------------------
    # NEW: Project scanning
    # ------------------------------------------------------------------------
    def scan_project(self, project_root: Optional[Path] = None) -> ProjectScanResult:
        """Scan a project for AI development configuration."""
        root = Path(project_root).resolve() if project_root else self.base
        self.scanner = ProjectScanner(root, self.registry_root)
        return self.scanner.scan()

    # ------------------------------------------------------------------------
    # NEW: Compatibility analysis
    # ------------------------------------------------------------------------
    def analyze_compatibility(
        self,
        scan_result: ProjectScanResult,
        platform: str
    ) -> List[Any]:
        """Analyze scanned project against target platform."""
        engine = CompatibilityEngine(self.catalog, platform, self.registry_root)
        return engine.analyze(scan_result)

    def _build_diagnostic_report(
        self,
        scan_result: ProjectScanResult,
        platform: str,
        issues: List[Any]
    ) -> "DiagnosticReport":
        """Build a structured diagnostic report from scan results and issues."""
        from kdesk.diagnostics import DiagnosticReport, ComponentReport, Issue

        # Group issues by component
        components: Dict[str, ComponentReport] = {}

        for issue in issues:
            comp_key = f"{issue.component}:{issue.file}"
            if comp_key not in components:
                # Determine component type from file path
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

        # Create component list
        component_list = list(components.values())

        # Calculate compatibility score
        score = self._calculate_score(issues)

        report = DiagnosticReport(
            project_root=str(scan_result.project_root),
            platform=platform or scan_result.platform or "unknown",
            score=score,
            max_score=100,
            components=component_list,
            issues=issues,
            scan_metadata=scan_result.metadata,
        )

        return report

    def _calculate_score(self, issues: List[Any]) -> int:
        """Calculate deterministic compatibility score (0-100)."""
        if not issues:
            return 100

        # Count by severity
        critical = sum(1 for i in issues if i.severity == Severity.CRITICAL)
        errors = sum(1 for i in issues if i.severity == Severity.ERROR)
        warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
        infos = sum(1 for i in issues if i.severity == Severity.INFO)

        # Cap penalties: CRITICAL=20 each (max 80), ERROR=10 each (max 60), WARNING=2 each (max 40), INFO=0
        penalty = min(critical * 20, 80) + min(errors * 10, 60) + min(warnings * 2, 40)

        # Base score minus penalties, minimum 0
        score = max(0, 100 - penalty)
        return min(100, score)

    # ------------------------------------------------------------------------
    # NEW: Fix application
    # ------------------------------------------------------------------------
    def apply_fixes(
        self,
        issues: List[Any],
        platform: str,
        dry_run: bool = False,
        project_root: Optional[Path] = None
    ) -> FixReport:
        """Apply fixes for fixable issues."""
        active_root = project_root or self.base
        engine = FixEngine(active_root, platform, dry_run)
        return engine.apply_fixes(issues, self.catalog, platform, self.registry_root, project_root=project_root)

    # ------------------------------------------------------------------------
    # NEW: Full diagnostic pipeline
    # ------------------------------------------------------------------------
    def diagnose(
        self,
        platform: str,
        project_root: Optional[Path] = None,
        fix: bool = False,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Run full diagnostic pipeline: scan -> analyze -> (fix) -> report."""
        # Scan
        scan_result = self.scan_project(project_root)

        # Analyze
        issues = self.analyze_compatibility(scan_result, platform)

        # Build report
        report = self._build_diagnostic_report(scan_result, platform, issues)

        # Apply fixes if requested
        fix_report = None
        if fix and report.fixable_count > 0:
            fix_report = self.apply_fixes(issues, platform, dry_run, project_root=project_root or self.base)
            report.after_fix_score = fix_report.after_score

        return {
            "report": report,
            "fix_report": fix_report,
        }

    # ------------------------------------------------------------------------
    # NEW: Report formatting
    # ------------------------------------------------------------------------
    def format_report(self, report: "DiagnosticReport", verbose: bool = False) -> str:
        """Format diagnostic report for human-readable output."""
        lines = []

        # Header
        lines.append("╭──────────────────── KDESK DOCTOR ────────────────────╮")
        lines.append(f"│ PROJECT: {report.project_root:<43}│")
        lines.append(f"│ TARGET:  {report.platform:<43}│")
        lines.append(f"│ HEALTH:  {'█' * (report.score // 10)}{'░' * (10 - report.score // 10)} {report.score:>3}%{' ' * 34}│")
        lines.append("├──────────────────────────────────────────────────────┤")
        lines.append(f"│ COMPONENTS  Agents: {len([c for c in report.components if c.type == 'agent']):>3}  Skills: {len([c for c in report.components if c.type == 'skill']):>3}  Workflows: {len([c for c in report.components if c.type == 'workflow']):>3}  Other: {len([c for c in report.components if c.type not in ('agent', 'skill', 'workflow')]):>3}  │")
        lines.append("├──────────────────────────────────────────────────────┤")
        lines.append(f"│ ISSUES      ✕ Errors: {report.error_count:>3}  ⚠ Warnings: {report.warning_count:>3}  ℹ Info: {report.info_count:>3}  │")
        lines.append(f"│ FIXABLE     {report.fixable_count:>3} issues can be fixed automatically{' ' * 12}│")
        lines.append("╰──────────────────────────────────────────────────────╯")

        if verbose and report.issues:
            lines.append("")
            lines.append("ISSUE DETAILS:")
            lines.append("─" * 60)
            for issue in report.issues:
                sev_marker = {"CRITICAL": "✕", "ERROR": "✕", "WARNING": "⚠", "INFO": "ℹ"}[issue.severity.value]
                fix_marker = " [FIXABLE]" if issue.fixable else ""
                lines.append(f"  {sev_marker} [{issue.severity.value}] {issue.file}")
                lines.append(f"     {issue.message}")
                lines.append(f"     Reason: {issue.reason}")
                if issue.suggested_fix:
                    lines.append(f"     Fix: {issue.suggested_fix}{fix_marker}")
                lines.append("")

        return "\n".join(lines)

    def format_json(self, report: "DiagnosticReport") -> str:
        """Format report as JSON."""
        return json.dumps(report.to_dict(), indent=2, default=str)

    def format_fix_report(self, fix_report: FixReport) -> str:
        """Format fix report for human output."""
        if not fix_report:
            return "No fixes applied."

        lines = []
        lines.append("╭──────────────────── FIX REPORT ────────────────────╮")
        lines.append(f"│ BEFORE:  {fix_report.before_score:>3}%  →  AFTER:  {fix_report.after_score:>3}%{' ' * 18}│")
        lines.append(f"│ SUCCESSFUL: {fix_report.successful:>3}  FAILED: {fix_report.failed:>3}  VALIDATED: {fix_report.validation_passed:>3}  │")
        lines.append("╰────────────────────────────────────────────────────╯")

        if fix_report.fixes:
            lines.append("")
            for fix in fix_report.fixes:
                status = "✓" if fix.success else "✕"
                lines.append(f"  {status} {fix.issue_id}: {fix.message}")
                if fix.backup_path:
                    lines.append(f"     Backup: {fix.backup_path}")

        if fix_report.manual_actions:
            lines.append("")
            lines.append("MANUAL ACTIONS REQUIRED:")
            for action in fix_report.manual_actions:
                lines.append(f"  - {action}")

        return "\n".join(lines)

    # ------------------------------------------------------------------------
    # EXISTING: Summary
    # ------------------------------------------------------------------------
    def install_summary(self) -> Dict[str, Any]:
        """Original install verification summary."""
        return self.summary()


# ------------------------------------------------------------------------
# Convenience functions
# ------------------------------------------------------------------------
def run_doctor_diagnose(
    platform: str,
    project_root: Optional[Path] = None,
    registry_root: Optional[Path] = None,
    fix: bool = False,
    dry_run: bool = False,
    json_output: bool = False,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Run full diagnostic pipeline."""
    base = project_root or Path.cwd()
    registry = Path(registry_root).resolve() if registry_root else default_repo_root()
    adapters = AdapterRegistry(registry)
    doctor = Doctor(adapters, base=base, registry_root=registry)

    result = doctor.diagnose(platform, project_root, fix, dry_run)

    if json_output:
        output = {"report": result["report"].to_dict()}
        if result["fix_report"]:
            output["fix_report"] = result["fix_report"].to_dict()
        return output

    return result


def run_doctor_install_check(
    platform: Optional[str] = None,
    base: Optional[Path] = None,
    registry_root: Optional[Path] = None,
    format: str = "json"
) -> Any:
    """Original install verification."""
    registry = Path(registry_root).resolve() if registry_root else default_repo_root()
    adapters = AdapterRegistry(registry)
    doctor = Doctor(adapters, base=base or Path.cwd(), registry_root=registry)

    if platform:
        return doctor.check(platform)
    return doctor.summary()