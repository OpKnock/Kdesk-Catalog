#!/usr/bin/env python3
"""CI staleness gate: every committed report must match current repository state.

Compares the committed reports/*.json against freshly computed values from the
kdesk package modules (using the same committed policy/exception files), so CI
fails when any generated report is stale. Exits non-zero on any mismatch.

Usage: python scripts/check-report-freshness.py [--root PATH]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from kdesk.adapters import AdapterRegistry
from kdesk.duplicates import DuplicateDetector, DuplicatePolicy
from kdesk.license import LicenseAudit, LicensePolicy
from kdesk.provenance import Provenance
from kdesk.quality import QualityReport
from kdesk.registry import Catalog
from kdesk.security import scan_repo
from kdesk.stats import StatsError, compute as compute_stats

# Stats keys that must match between committed report and live state.
COMPARE_KEYS = [
    "total_files",
    "agents",
    "skills",
    "definitions_total",
    "workflows",
    "platforms",
    "platform_output_files",
    "yaml_definitions",
    "json_definitions",
    "yaml_files",
    "json_files",
    "load_errors",
]

WIRING_KEYS = ["agents_wired", "links", "unwired_agents", "skills_used", "manual_links"]

LICENSE_KEYS = [
    "definitions",
    "license_counts",
    "valid_count",
    "inherited_count",
    "third_party_count",
    "unspecified_count",
    "missing_count",
    "unapproved_count",
    "unknown_count",
    "unresolved_count",
    "policy_applied",
]

DUPLICATE_KEYS = [
    "family_count",
    "definitions_scanned",
    "classified_count",
    "unresolved_count",
    "policy_applied",
]

SECURITY_KEYS = [
    "count",
    "definitions_scanned",
    "severity_counts",
    "excepted_count",
    "blocking_count",
    "exceptions_applied",
]

PROVENANCE_KEYS = ["json_files", "yaml_files", "files_scanned", "verified"]

QUALITY_KEYS = ["definitions", "files_scanned", "low_score_count"]

ADAPTER_KEYS = ["platforms", "support_counts"]


def _subset(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    return {k: data.get(k) for k in keys}


def _differences(committed: Dict[str, Any], live: Dict[str, Any], keys: List[str]) -> List[str]:
    diffs: List[str] = []
    for key in keys:
        if committed.get(key) != live.get(key):
            diffs.append(f"{key}: report={committed.get(key)} live={live.get(key)}")
    return diffs


def _live_values(root: Path, reports: Path) -> Dict[str, Dict[str, Any]]:
    catalog = Catalog.from_repo(root)
    stats = compute_stats(root)
    adapters = AdapterRegistry(root).summary()
    live = {
        "catalog-stats.json": stats,
        "license-report.json": LicenseAudit(catalog).audit(
            policy=LicensePolicy.load(reports / "license-policy.json")
        ),
        "duplicate-report.json": DuplicateDetector(catalog).detect(
            policy=DuplicatePolicy.load(reports / "duplicate-classifications.json")
        ),
        "security-report.json": scan_repo(root, reports / "security-exceptions.json"),
        "provenance-report.json": Provenance(root).verify(),
        "quality-report.json": QualityReport(catalog).score(),
        "platform-adapter-report.json": adapters,
    }
    return live


def _check(name: str, committed: Dict[str, Any], live: Dict[str, Any]) -> List[str]:
    if name == "catalog-stats.json":
        diffs = _differences(committed, live, COMPARE_KEYS)
        cw = committed.get("wiring", {})
        lw = live.get("wiring", {})
        for key in WIRING_KEYS:
            if cw.get(key) != lw.get(key):
                diffs.append(f"wiring.{key}: report={cw.get(key)} live={lw.get(key)}")
        return diffs
    spec = {
        "license-report.json": LICENSE_KEYS,
        "duplicate-report.json": DUPLICATE_KEYS,
        "security-report.json": SECURITY_KEYS,
        "provenance-report.json": PROVENANCE_KEYS,
        "quality-report.json": QUALITY_KEYS,
        "platform-adapter-report.json": ADAPTER_KEYS,
    }.get(name)
    if spec is None:
        return []
    return _differences(committed, live, spec)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] != "--root" else ROOT
    if len(sys.argv) > 2 and sys.argv[1] == "--root":
        root = Path(sys.argv[2])
    reports = root / "reports"
    if not reports.is_dir():
        print("FATAL: reports/ directory not found")
        return 1

    try:
        live = _live_values(root, reports)
    except StatsError as exc:
        print(f"FATAL: {exc}")
        return 1

    names = [
        "catalog-stats.json",
        "license-report.json",
        "duplicate-report.json",
        "security-report.json",
        "provenance-report.json",
        "quality-report.json",
        "platform-adapter-report.json",
    ]
    failed = False
    for name in names:
        path = reports / name
        if not path.is_file():
            print(f"WARN: {name} missing (not committed yet)")
            continue
        try:
            committed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"FATAL: {name} unreadable: {exc}")
            failed = True
            continue
        diffs = _check(name, committed, live[name])
        if diffs:
            failed = True
            print(f"STALE: {name}")
            for d in diffs:
                print(f"  {d}")
        else:
            print(f"OK: {name} matches current repository state")

    # baseline-stats.json is a stats snapshot only.
    path = reports / "baseline-stats.json"
    if path.is_file():
        try:
            committed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"FATAL: {path.name} unreadable: {exc}")
            failed = True
        else:
            diffs = _differences(committed, live["catalog-stats.json"], COMPARE_KEYS)
            if diffs:
                failed = True
                print(f"STALE: {path.name}")
                for d in diffs:
                    print(f"  {d}")
            else:
                print(f"OK: {path.name} matches current repository state")

    if failed:
        print("FATAL: generated reports are stale - regenerate with scripts/generate-reports.py")
        return 1
    print("all committed reports are fresh")
    return 0


if __name__ == "__main__":
    sys.exit(main())