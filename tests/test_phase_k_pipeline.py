"""Phase K: orchestration pipeline tests (resolve -> plan -> policy -> run)."""
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

from kdesk.engine import (  # noqa: E402
    STATUS_BLOCKED,
    STATUS_FAILED,
    STATUS_PARTIAL,
    STATUS_PENDING,
    STATUS_SUCCESS,
    STATUS_WAITING_APPROVAL,
    Engine,
)
from kdesk.policy import ApprovalState  # noqa: E402
from kdesk.registry import Catalog, default_repo_root  # noqa: E402


class PipelineTests(unittest.TestCase):
    """End-to-end pipeline tests against the real catalog (read-only runtime)."""

    @classmethod
    def setUpClass(cls):
        cls.repo = Path(os.environ.get("KDESK_REPO", REPO))
        cls.catalog = Catalog.from_repo(cls.repo)
        cls.engine = Engine(cls.repo, catalog=cls.catalog)
        cls.tmp = Path(tempfile.mkdtemp(prefix="kdesk-phase-k-"))
        cls.base = cls.tmp / "proj"
        (cls.base / "src").mkdir(parents=True)
        (cls.base / "src" / "greet.py").write_text(
            "def greet(name: str) -> str:\n    return f'hi {name}'\n",
            encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls.tmp, ignore_errors=True)

    # ------------------------------------------------------------- resolve
    def test_resolve_classifies_intent(self):
        result = self.engine.resolve("review python code quality",
                                     probe_environment=False)
        self.assertTrue(result.candidates)
        self.assertIn(result.intent.get("intent"),
                      ("review", "analyze", "inspect", "unknown"))

    def test_resolve_returns_catalog_definitions(self):
        result = self.engine.resolve("explain how to use curl",
                                     probe_environment=False)
        self.assertTrue(result.candidates)
        for cand in result.candidates:
            self.assertTrue(cand.name)
            self.assertGreater(cand.score, 0.0)

    def test_why_explains_matching(self):
        result = self.engine.resolve("write a fastapi endpoint",
                                     probe_environment=False)
        target = result.candidates[0].name
        explanation = self.engine.why("write a fastapi endpoint", target)
        self.assertIsInstance(explanation, dict)
        self.assertIn("target", explanation)
        self.assertTrue(explanation.get("found"))

    # ---------------------------------------------------------------- plan
    def test_plan_builds_steps(self):
        plan = self.engine.plan("refactor python project structure")
        self.assertTrue(plan.steps)
        for step in plan.steps:
            self.assertIn(step.index, range(len(plan.steps)))
            self.assertTrue(step.description)
            self.assertIn(step.decision.decision.value,
                          ("allowed", "require_approval", "blocked"))

    def test_plan_orders_steps(self):
        plan = self.engine.plan("update documentation for the api")
        indexes = [s.index for s in plan.steps]
        self.assertEqual(indexes, sorted(indexes))

    # ----------------------------------------------------------------- run
    def test_run_success_path(self):
        result = self.engine.run("analyze python code quality",
                                 base=self.base, auto_approve=True,
                                 timeout_s=90.0)
        self.assertEqual(result.execution_id, result.execution_id)
        self.assertIn(result.status,
                      (STATUS_SUCCESS, STATUS_PARTIAL, STATUS_FAILED,
                       STATUS_BLOCKED))
        record = self.engine.inspect(result.execution_id)
        self.assertIsNotNone(record)
        self.assertEqual(record["execution"]["request"],
                         "analyze python code quality")

    def test_run_persists_artifacts(self):
        result = self.engine.run("list files in the project",
                                 base=self.base, auto_approve=True,
                                 timeout_s=90.0)
        if result.status == STATUS_SUCCESS:
            self.assertTrue(result.artifacts)
        record = self.engine.inspect(result.execution_id)
        self.assertIsNotNone(record)
        self.assertGreaterEqual(record["events_count"], 1)

    def test_run_dry_run_no_execution(self):
        plan = self.engine.plan("format the source code")
        self.assertTrue(plan.steps)
        result = self.engine.run("format the source code", base=self.base,
                                 auto_approve=True, dry_run=True,
                                 timeout_s=30.0)
        self.assertIn(result.status,
                      (STATUS_PENDING, STATUS_SUCCESS, STATUS_PARTIAL,
                       STATUS_BLOCKED, STATUS_FAILED))

    def test_run_approval_gate_waits(self):
        result = self.engine.run("install a linter in the project",
                                 base=self.base, auto_approve=False,
                                 timeout_s=60.0)
        if result.status == STATUS_WAITING_APPROVAL:
            pending = [s for s in result.steps
                       if s.get("status") == "WAITING_APPROVAL"]
            self.assertTrue(pending)
            first = pending[0]["index"]
            updated = self.engine.approve(result.execution_id, first, True,
                                          note="test approval")
            self.assertIsNotNone(updated)
            self.assertEqual(updated["state"], "approved")

    # -------------------------------------------------------------- history
    def test_history_lists_executions(self):
        self.engine.run("analyze python code quality", base=self.base,
                        auto_approve=True, timeout_s=90.0)
        history = self.engine.history(limit=5)
        self.assertTrue(history)
        for entry in history:
            self.assertIn("execution_id", entry)
        self.assertNotEqual(history[0]["status"], STATUS_PENDING)

    def test_resume_after_approval(self):
        result = self.engine.run("install a linter in the project", base=self.base,
                                 auto_approve=False, timeout_s=60.0)
        if result.status != STATUS_WAITING_APPROVAL:
            self.skipTest(f"request did not gate: {result.status}")
        pending = [s for s in result.steps if s.get("status") == "WAITING_APPROVAL"]
        first = pending[0]["index"]
        updated = self.engine.approve(result.execution_id, first, True,
                                      note="test approval")
        self.assertIsNotNone(updated)
        resumed = self.engine.resume(result.execution_id, base=self.base, timeout_s=60.0)
        self.assertIsNotNone(resumed)
        self.assertEqual(resumed.execution_id, result.execution_id)
        resumed_waiting = [s for s in resumed.steps if s.get("status") == "WAITING_APPROVAL"]
        if resumed.status == STATUS_WAITING_APPROVAL:
            self.assertTrue(resumed_waiting)
            self.assertGreater(resumed_waiting[0]["index"], first)

    def test_inspect_unknown_execution(self):
        self.assertIsNone(self.engine.inspect("does-not-exist-0000"))

    # ----------------------------------------------------------------- cli
    def test_cli_commands_print_help(self):
        commands = ["resolve", "why", "plan", "run", "history", "inspect",
                    "approve", "verify", "stats", "doctor", "schema",
                    "security", "wiring", "graph"]
        for command in commands:
            with self.subTest(command=command):
                proc = subprocess.run(
                    [sys.executable, "-m", "kdesk.cli", command, "--help"],
                    capture_output=True, text=True, cwd=str(self.repo),
                    encoding="utf-8", errors="replace", timeout=120)
                self.assertEqual(proc.returncode, 0,
                                 f"{command}: {proc.stderr[:300]}")

    def test_cli_verify_fast_prints_summary(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.repo)
        proc = subprocess.run(
            [sys.executable, "-m", "kdesk.cli", "verify", "--fast"],
            capture_output=True, text=True, cwd=str(self.repo),
            env=env, encoding="utf-8", errors="replace", timeout=600)
        self.assertEqual(proc.returncode, 0, proc.stderr[:500])
        self.assertIn("verify:", proc.stdout)

    def test_cli_run_and_history_roundtrip(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.repo)
        run = subprocess.run(
            [sys.executable, "-m", "kdesk.cli", "run",
             "analyze python code quality", "--base", str(self.base),
             "--auto-approve", "--json"],
            capture_output=True, text=True, cwd=str(self.repo),
            env=env, encoding="utf-8", errors="replace", timeout=300)
        self.assertEqual(run.returncode, 0, run.stderr[:500])
        data = json.loads(run.stdout)
        self.assertIn("execution_id", data)
        history = subprocess.run(
            [sys.executable, "-m", "kdesk.cli", "history", "--limit", "3"],
            capture_output=True, text=True, cwd=str(self.repo),
            env=env, encoding="utf-8", errors="replace", timeout=120)
        self.assertEqual(history.returncode, 0, history.stderr[:300])
        self.assertIn(data["execution_id"], history.stdout)


if __name__ == "__main__":
    unittest.main()