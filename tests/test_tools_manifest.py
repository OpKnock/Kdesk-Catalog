"""tools.json manifest tests.

Assert that the tools manifest (repo-root tools.json) matches the converter's
platform registries:
- keys == ALL_PLATFORMS | DEPRECATED_SINGLE_FILE_PLATFORMS (45 platforms incl. void)
- every entry carries the full tool descriptor shape (id/label/kebab/order/...)
- every platform-agents/ directory is covered
- orders are unique 1..45
- the converter's own validator passes on the committed manifest
- regenerating claude_code is byte-identical (no drift)
"""

import importlib.util
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_KEYS = (
    "id", "label", "kebab", "accent", "icon", "order",
    "scope", "detect", "version", "format",
    "installKind", "slugFrom", "slugPrefix", "dest",
)


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c = load_module("universal_converter", "universal-converter.py")

MANIFEST = c.load_tools_manifest()
TOOLS = MANIFEST["tools"]

EXPECTED_KEYS = set(c.ALL_PLATFORMS) | set(c.DEPRECATED_SINGLE_FILE_PLATFORMS)


def snapshot_tree(directory):
    tree = {}
    for p in sorted(Path(directory).rglob("*")):
        if p.is_file():
            tree[str(p.relative_to(Path(directory))).replace(os.sep, "/")] = p.read_bytes()
    return tree


class TestToolsManifestKeys(unittest.TestCase):
    def test_keys_match_converter_platforms(self):
        self.assertEqual(set(TOOLS), EXPECTED_KEYS)

    def test_manifest_has_version(self):
        self.assertIn("version", MANIFEST)

    def test_entry_ids_match_keys(self):
        for key, entry in TOOLS.items():
            self.assertEqual(entry["id"], key)
            self.assertEqual(entry["kebab"], key)


class TestToolsManifestEntryShape(unittest.TestCase):
    def test_required_keys_present(self):
        for key, entry in TOOLS.items():
            for field in REQUIRED_KEYS:
                self.assertIn(field, entry, f"{key} missing {field}")

    def test_scope_has_user_and_project(self):
        for key, entry in TOOLS.items():
            self.assertIn("user", entry["scope"], key)
            self.assertIn("project", entry["scope"], key)

    def test_detect_has_dirs_and_agents_dir(self):
        for key, entry in TOOLS.items():
            self.assertIsInstance(entry["detect"]["dirs"], list, key)
            self.assertIn("agentsDir", entry["detect"], key)

    def test_dest_has_user_and_project(self):
        for key, entry in TOOLS.items():
            self.assertIn("user", entry["dest"], key)
            self.assertIn("project", entry["dest"], key)

    def test_orders_unique_and_sequential(self):
        orders = [entry["order"] for entry in TOOLS.values()]
        self.assertEqual(sorted(orders), list(range(1, len(TOOLS) + 1)))


class TestPlatformDirCoverage(unittest.TestCase):
    def test_every_platform_dir_covered(self):
        platform_dir = ROOT / "platform-agents"
        dirs = {p.name for p in platform_dir.iterdir() if p.is_dir()}
        self.assertEqual(set(TOOLS), dirs)


class TestConverterValidation(unittest.TestCase):
    def test_validate_passes_on_committed_manifest(self):
        self.assertEqual(c.validate_tools_manifest(), [])

    def test_validate_detects_missing_entry(self):
        import copy
        broken = copy.deepcopy(MANIFEST)
        broken["tools"].pop("void")
        errors = c.validate_tools_manifest(broken)
        self.assertTrue(any("void" in e for e in errors))

    def test_validate_detects_unknown_entry(self):
        import copy
        broken = copy.deepcopy(MANIFEST)
        broken["tools"]["not_a_platform"] = {"id": "not_a_platform", "kebab": "not_a_platform"}
        errors = c.validate_tools_manifest(broken)
        self.assertTrue(any("not_a_platform" in e for e in errors))

    def test_manifest_path_points_to_repo_root(self):
        self.assertEqual(c.TOOLS_MANIFEST_PATH, ROOT / "tools.json")


class TestClaudeCodeRegeneration(unittest.TestCase):
    def test_claude_code_regen_is_byte_identical(self):
        platform_dir = ROOT / "platform-agents" / "claude_code"
        before = snapshot_tree(platform_dir)
        proc = subprocess.run(
            [sys.executable, "scripts/universal-converter.py", "--platforms", "claude_code", "--quiet"],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("tools.json validation failed", proc.stdout + proc.stderr)
        after = snapshot_tree(platform_dir)
        self.assertEqual(set(before), set(after))
        for rel in before:
            self.assertEqual(before[rel], after[rel], f"drift in {rel}")


if __name__ == "__main__":
    unittest.main()