#!/usr/bin/env python3
"""
Canonical release verification for Kdesk-Catalog.

Runs all release gates and outputs a clear PASS/FAIL verdict.
"""
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent


def _get_platform_output_count() -> int:
    """Read platform output count from the authoritative report."""
    report_path = ROOT / "reports" / "catalog-stats.json"
    if not report_path.exists():
        raise RuntimeError("catalog-stats.json not found - run generate-reports.py first")
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("platform_output_files", 0)


GATES: List[Tuple[str, List[str]]] = [
    # Generation first (fresh checkout has no agents/json, workflows/, etc.)
    ("Generate JSON from YAML", ["python", "scripts/yaml-to-json.py"]),
    ("Generate platform outputs", ["python", "scripts/universal-converter.py", "--platforms", "all", "--quiet"]),

    # Catalog integrity (fast)
    ("Schema validation", ["python", "scripts/schema-check.py"]),
    ("Duplicate ID validation", ["python", "scripts/check-catalog.py"]),
    ("Provenance validation", ["python", "-m", "kdesk.cli", "provenance", "--root", "."]),
    ("Catalog integrity (stats + zero-file guard)", ["python", "scripts/verify-all.py"]),

    # Generation
    ("Marketplace generation & validation", ["python", "scripts/generate-marketplaces.py", "--validate"]),
    ("Platform generation (converter validate)", ["python", "scripts/universal-converter.py", "--platforms", "all", "--validate"]),

    # Wiring
    ("Wiring integrity", ["python", "scripts/wire-skills.py"]),
    ("Graph validation", ["python", "-m", "kdesk.cli", "graph", "--root", "."]),

    # Reports (fast - uses cached stats; skip on fresh checkout where JSONs are gitignored)
    ("Report freshness", ["python", "scripts/check-report-freshness.py", "--fast", "--root", "."]),

    # Security
    ("Security validation (no hardcoded secrets)", ["python", "-m", "kdesk.cli", "security", "--json", "--root", "."]),
    ("Stale model IDs (gate)", ["python", "scripts/fix-stale-model-ids.py", "--dry-run"]),
    ("Duplicate scan", ["python", "-m", "kdesk.cli", "duplicates", "--root", "."]),
    ("License gate", ["python", "-m", "kdesk.cli", "license", "--root", "."]),

    # Tests
    ("Unit tests (quick)", ["python", "-m", "unittest", "-v",
     "tests.test_divisions",
     "tests.test_tools_manifest",
     "tests.test_converter_cli",
     "tests.test_wire_skills",
     "tests.test_marketplaces",
     "tests.test_kdesk_install",
     "tests.test_agent_framework",
     "tests.test_yaml_to_json"]),

    # Packaging
    ("Package build (sdist + wheel)", ["python", "-m", "build"]),

    # Clean install + CLI smoke test
    ("Clean install + CLI smoke test", ["python", "scripts/release-smoke-test.py"]),

    # No uncommitted source changes (exclude regenerated output dirs)
    ("No uncommitted source changes", ["git", "diff", "--exit-code", "--", ".",
     ":(exclude)reports/*",
     ":(exclude)platform-agents/*",
     ":(exclude)agents/*",
     ":(exclude)skills/json",
     ":(exclude)skills/yaml",
     ":(exclude)workflows/*"]),
]


def run_gate(name: str, cmd: List[str], timeout: int = 300) -> Tuple[str, str]:
    """Run a single gate and return (status, output)."""
    print(f"\n{'='*60}")
    print(f"GATE: {name}")
    print(f"CMD: {' '.join(cmd)}")
    print(f"{'='*60}")
    start = time.time()
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        elapsed = time.time() - start
        if result.returncode == 0:
            print(f"STATUS: PASS ({elapsed:.1f}s)")
            if result.stdout.strip():
                print(result.stdout[:500])
            return "PASS", result.stdout
        else:
            print(f"STATUS: FAIL (exit code {result.returncode}) ({elapsed:.1f}s)")
            if result.stdout.strip():
                print(f"STDOUT:\n{result.stdout[:1000]}")
            if result.stderr.strip():
                print(f"STDERR:\n{result.stderr[:1000]}")
            return "FAIL", result.stderr or result.stdout
    except subprocess.TimeoutExpired:
        print(f"STATUS: FAIL (timeout after {timeout}s)")
        return "FAIL", "timeout"
    except Exception as e:
        print(f"STATUS: FAIL (exception: {e})")
        return "FAIL", str(e)


def main() -> int:
    print("Kdesk-Catalog Release Verification")
    print("=" * 60)
    print(f"Repository: {ROOT}")
    print(f"Running {len(GATES)} release gates...")

    results: List[Tuple[str, str, str]] = []  # (name, status, output)

    for name, cmd in GATES:
        # Use longer timeout for slow gates
        if name in ("Package build (sdist + wheel)", "Clean install + CLI smoke test", "Unit tests (quick)", "Report freshness"):
            timeout = 600
        else:
            timeout = 300
        status, output = run_gate(name, cmd, timeout=timeout)
        results.append((name, status, output))

    # Summary
    print("\n" + "=" * 60)
    print("RELEASE GATE SUMMARY")
    print("=" * 60)
    all_pass = True
    for name, status, _ in results:
        status_str = "PASS" if status == "PASS" else "FAIL"
        print(f"  [{status_str}] {name}")
        if status != "PASS":
            all_pass = False

    print("=" * 60)
    if all_pass:
        print("RELEASE_READY")
        print("All release gates passed.")
        return 0
    else:
        print("NOT_RELEASE_READY")
        print("One or more release gates failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())