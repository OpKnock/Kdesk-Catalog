"""Phase L: verification gate tests."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kdesk.verify import run_verify  # noqa: E402


class VerifyGateTests(unittest.TestCase):
    """The verify gate must pass on the real repo and fail cleanly on a broken one."""

    @classmethod
    def setUpClass(cls):
        cls.repo = Path(os.environ.get("KDESK_REPO", REPO))

    def test_fast_verify_passes(self):
        summary = run_verify(self.repo, fast=True)
        self.assertEqual(summary["status"], "PASS")
        self.assertEqual(summary.get("tool"), "kdesk")
        self.assertIn("checks", summary)
        self.assertIn("results", summary)
        self.assertEqual(summary["checks"].get("FAIL", 0), 0)
        names = [r["name"] for r in summary["results"]]
        self.assertEqual(len(names), len(set(names)))

    def test_fast_verify_skips_slow_checks(self):
        summary = run_verify(self.repo, fast=True)
        skipped = [r["name"] for r in summary["results"]
                   if r["status"] == "SKIP"]
        self.assertIn("schema", skipped)
        self.assertIn("provenance", skipped)
        self.assertIn("freshness", skipped)

    def test_skip_flag_removes_check(self):
        summary = run_verify(self.repo, fast=True, skip=["quality"])
        for result in summary["results"]:
            if result["name"] == "quality":
                self.assertEqual(result["status"], "SKIP")
                self.assertIn("excluded", result["detail"])
                break
        else:
            self.fail("quality check missing from results")

    def test_every_result_has_status(self):
        summary = run_verify(self.repo, fast=True)
        for result in summary["results"]:
            self.assertIn(result["status"], ("PASS", "FAIL", "SKIP"))

    def test_empty_repo_fails_cleanly(self):
        with tempfile.TemporaryDirectory(prefix="kdesk-empty-") as tmp:
            summary = run_verify(Path(tmp), fast=True)
            self.assertEqual(summary["status"], "FAIL")
            names = {r["name"]: r["status"] for r in summary["results"]}
            self.assertEqual(names.get("catalog_load"), "FAIL")

    def test_cli_verify_json_roundtrip(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.repo)
        proc = subprocess.run(
            [sys.executable, "-m", "kdesk.cli", "verify", "--fast", "--json"],
            capture_output=True, text=True, cwd=str(self.repo),
            env=env, encoding="utf-8", errors="replace", timeout=600)
        self.assertEqual(proc.returncode, 0, proc.stderr[:500])
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "PASS")

    def test_cli_verify_exit_codes(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.repo)
        with tempfile.TemporaryDirectory(prefix="kdesk-broken-") as tmp:
            proc = subprocess.run(
                [sys.executable, "-m", "kdesk.cli", "verify", "--fast",
                 "--root", tmp],
                capture_output=True, text=True, cwd=str(self.repo),
                env=env, encoding="utf-8", errors="replace", timeout=600)
            self.assertEqual(proc.returncode, 3)


if __name__ == "__main__":
    unittest.main()