"""Phase A tests: authoritative stats, report freshness, verify-all zero-file guard."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from kdesk.registry import Catalog  # noqa: E402
from kdesk.stats import StatsError, compute, format_table, write_baseline  # noqa: E402


class TestAuthoritativeStats(unittest.TestCase):
    def setUp(self):
        self.catalog = Catalog.from_repo(ROOT)
        self.stats = compute(ROOT)

    def test_counts_match_catalog(self):
        self.assertEqual(self.stats["agents"], len(self.catalog.agents))
        self.assertEqual(self.stats["skills"], len(self.catalog.skills))
        self.assertEqual(self.stats["definitions_total"], self.stats["agents"] + self.stats["skills"])

    def test_yaml_json_counts_are_consistent(self):
        self.assertEqual(self.stats["yaml_files"], self.stats["yaml_definitions"])
        self.assertGreater(self.stats["yaml_files"], 0)
        self.assertGreater(self.stats["json_files"], 0)
        self.assertEqual(self.stats["total_files"], self.stats["yaml_files"] + self.stats["json_files"])

    def test_workflows_present(self):
        self.assertGreater(self.stats["workflows"], 0)

    def test_platform_outputs(self):
        self.assertGreater(self.stats["platforms"], 0)
        self.assertGreater(self.stats["platform_output_files"], 0)

    def test_no_load_errors(self):
        self.assertEqual(self.stats["load_errors"], 0)

    def test_wiring_section(self):
        w = self.stats["wiring"]
        self.assertGreater(w["agents_wired"], 0)
        self.assertGreater(w["links"], 0)

    def test_checksums_section(self):
        c = self.stats["checksums"]
        self.assertEqual(c["definition_count"], self.stats["yaml_files"])
        self.assertTrue(c["content_hash"])

    def test_zero_file_scan_raises(self):
        from pathlib import Path
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            fake = Path(td) / "universal-agents"
            fake.mkdir()
            with self.assertRaises(StatsError):
                compute(Path(td))

    def test_format_table_contains_counts(self):
        text = format_table(self.stats)
        self.assertIn(f"Agents:    {self.stats['agents']}", text)
        self.assertIn(f"Skills:    {self.stats['skills']}", text)
        self.assertIn(f"Workflows: {self.stats['workflows']}", text)


class TestReportFreshness(unittest.TestCase):
    def test_catalog_stats_report_matches_live_state(self):
        report_path = ROOT / "reports" / "catalog-stats.json"
        self.assertTrue(report_path.is_file(), "catalog-stats.json must exist")
        committed = json.loads(report_path.read_text(encoding="utf-8"))
        live = compute(ROOT)
        for key in ("agents", "skills", "definitions_total", "workflows", "yaml_files",
                    "json_files", "platforms", "platform_output_files", "load_errors"):
            self.assertEqual(committed.get(key), live.get(key), f"stale report key: {key}")
        for key in ("agents_wired", "links", "unwired_agents"):
            self.assertEqual(committed.get("wiring", {}).get(key), live.get("wiring", {}).get(key))

    def test_baseline_report_matches_live_state(self):
        baseline = ROOT / "reports" / "baseline-stats.json"
        self.assertTrue(baseline.is_file(), "baseline-stats.json must exist")
        committed = json.loads(baseline.read_text(encoding="utf-8"))
        live = compute(ROOT)
        for key in ("agents", "skills", "definitions_total", "workflows", "yaml_files",
                    "json_files", "platforms", "platform_output_files", "load_errors"):
            self.assertEqual(committed.get(key), live.get(key), f"stale baseline key: {key}")

    def test_freshness_script_exits_zero_when_fresh(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check-report-freshness.py")],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_freshness_script_fails_on_stale_report(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fake_root = Path(td)
            (fake_root / "reports").mkdir()
            (fake_root / "reports" / "catalog-stats.json").write_text(
                json.dumps({"agents": -1, "wiring": {}}), encoding="utf-8"
            )
            # script derives root from its own location; point it at a fake copy
            # instead, verify the diff logic directly via module import
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "freshness", ROOT / "scripts" / "check-report-freshness.py"
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            committed = json.loads((fake_root / "reports" / "catalog-stats.json").read_text(encoding="utf-8"))
            live = compute(ROOT)
            diffs = mod._differences(committed, live, mod.COMPARE_KEYS)
            self.assertTrue(diffs)


class TestVerifyAllZeroGuard(unittest.TestCase):
    def test_verify_all_succeeds_on_real_repo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "verify-all.py")],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("TOTAL YAML FILES:", result.stdout)

    def test_verify_all_fails_on_zero_files(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fake = Path(td) / "universal-agents"
            fake.mkdir()
            shim = Path(td) / "shim_verify_zero.py"
            shim.write_text(
                "import sys\n"
                "import pathlib\n"
                "import importlib.util\n"
                "spec = importlib.util.spec_from_file_location(%r, %r)\n"
                "verify_all = importlib.util.module_from_spec(spec)\n"
                "spec.loader.exec_module(verify_all)\n"
                "verify_all.AGENTS_DIR = pathlib.Path(%r)\n"
                "sys.exit(verify_all.main())\n" % (
                    "verify_all", str(ROOT / "scripts" / "verify-all.py"), str(fake)
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(shim)], cwd=ROOT, capture_output=True, text=True
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("0 definitions scanned", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()