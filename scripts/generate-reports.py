#!/usr/bin/env python3
"""
Generate the seven spec section 97 reports:
  reports/provenance-report.json
  reports/license-report.json
  reports/quality-report.json
  reports/duplicate-report.json
  reports/security-report.json
  reports/platform-adapter-report.json
  reports/catalog-stats.json
All data comes from the kdesk package modules so reports always match the
verified pipeline. Zero-file false-success guards: every scan reports the
number of files/definitions it examined and refuses to claim a pass on 0.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kdesk.adapters import AdapterRegistry
from kdesk.duplicates import DuplicateDetector, DuplicatePolicy
from kdesk.license import LicenseAudit, LicensePolicy
from kdesk.provenance import Provenance, verify_wiring
from kdesk.quality import QualityReport
from kdesk.registry import Catalog
from kdesk.security import scan_repo
from kdesk.stats import StatsError, compute as compute_stats

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"


def write_report(name: str, data: dict) -> None:
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / name).write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"  wrote {name}", flush=True)


def guard_zero(scanned: int, label: str) -> None:
    if scanned == 0:
        print(f"FATAL: {label} scanned 0 files - refusing to write report")
        sys.exit(1)


def main() -> int:
    root = ROOT
    catalog = Catalog.from_repo(root)
    total_defs = len(catalog.agents) + len(catalog.skills)

    # 1. provenance report
    prov = Provenance(root).verify()
    guard_zero(prov["files_scanned"], "provenance")
    wiring = verify_wiring(root)
    write_report("provenance-report.json", {
        "schema": "provenance-report-v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "json_files": prov["json_files"],
        "yaml_files": prov["yaml_files"],
        "files_scanned": prov["files_scanned"],
        "verified": prov["verified"],
        "problems": prov["problems"],
        "wiring": wiring,
    })

    # 2. license report (policy-classified)
    lic = LicenseAudit(catalog).audit(policy=LicensePolicy.load(REPORTS / "license-policy.json"))
    guard_zero(lic["files_scanned"], "license")
    write_report("license-report.json", {
        "schema": "license-report-v2",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **lic,
    })

    # 3. quality report
    qual = QualityReport(catalog).score()
    guard_zero(qual["files_scanned"], "quality")
    write_report("quality-report.json", {
        "schema": "quality-report-v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **qual,
    })

    # 4. duplicate report (policy-classified)
    dup = DuplicateDetector(catalog).detect(
        policy=DuplicatePolicy.load(REPORTS / "duplicate-classifications.json")
    )
    guard_zero(dup["definitions_scanned"], "duplicates")
    write_report("duplicate-report.json", {
        "schema": "duplicate-report-v2",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **dup,
    })

    # 5. security report (severity + auditable exceptions)
    sec = scan_repo(root, REPORTS / "security-exceptions.json")
    guard_zero(sec["definitions_scanned"], "security")
    write_report("security-report.json", {
        "schema": "security-report-v2",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **sec,
    })

    # 6. platform adapter report
    adapters = AdapterRegistry(root).summary()
    guard_zero(adapters["platforms"], "platform-adapters")
    write_report("platform-adapter-report.json", {
        "schema": "platform-adapter-report-v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **adapters,
    })

    # 7. catalog stats: single authoritative source is kdesk.stats
    try:
        stats = compute_stats(root)
    except StatsError as exc:
        print(f"FATAL: {exc}")
        return 1
    guard_zero(stats["files_scanned"], "catalog-stats")
    write_report("catalog-stats.json", stats)

    print(f"reports written: provenance/license/quality/duplicates/security/adapters/catalog-stats", flush=True)
    print(f"  definitions scanned: {total_defs}; platforms: {adapters['platforms']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())