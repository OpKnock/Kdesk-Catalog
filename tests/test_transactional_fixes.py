"""Test transactional Doctor fixes with rollback."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kdesk.fixer import FixEngine


class TestTransactionalFixes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="kdesk_txn_")
        self.root = Path(self.tmp)
        self.test_file = self.root / "test-agent.yaml"
        self.original_content = 'name: test\nversion: 1.0.0\n'.encode()
        self.test_file.write_bytes(self.original_content)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_snapshot_captures_files(self):
        engine = FixEngine(project_root=self.root, platform="test")
        issues = [type("I", (), {"file": "test-agent.yaml", "fixable": True, "id": "t1"})()]
        snap = engine._snapshot(self.root, issues)
        self.assertIn(self.test_file, snap)
        self.assertEqual(snap[self.test_file], self.original_content)

    def test_rollback_restores_content(self):
        engine = FixEngine(project_root=self.root, platform="test")
        snapshot = {self.test_file: self.original_content}

        # Simulate a bad fix that corrupted the file
        self.test_file.write_bytes(b"corrupted")

        # Rollback
        engine._rollback(snapshot)

        # File restored
        self.assertEqual(self.test_file.read_bytes(), self.original_content)

    def test_rollback_removes_new_files(self):
        """If fix created a new file (not in snapshot), rollback removes it."""
        engine = FixEngine(project_root=self.root, platform="test")
        new_file = self.root / "new-file.yaml"
        new_file.write_text("new content")

        # Snapshot is empty (file didn't exist before)
        snapshot = {}

        # Add to rollback: empty content means delete
        snapshot[new_file] = b""
        engine._rollback(snapshot)

        self.assertFalse(new_file.exists())

    @patch.object(FixEngine, "_apply_fix")
    def test_transaction_rolls_back_on_error(self, mock_apply):
        """When _apply_fix raises, all changes are rolled back."""
        mock_apply.side_effect = RuntimeError("something broke badly")

        engine = FixEngine(project_root=self.root, platform="test")
        issues = [type("I", (), {
            "file": "test-agent.yaml", "fixable": True,
            "id": "t1", "suggested_fix": "fix it",
            "severity": type("S", (), {"value": "error"})(),
            "description": "desc",
            "platform": "test",
        })()]

        with self.assertRaises(RuntimeError):
            engine.apply_fixes(issues, catalog=None, platform="test", registry_root=self.root)

        # File must be unchanged after rollback
        self.assertEqual(self.test_file.read_bytes(), self.original_content)


if __name__ == "__main__":
    unittest.main()
