"""divisions.json manifest tests.

Assert that the divisions manifest (repo-root divisions.json) matches the
on-disk catalog layout:
- keys == universal-agents/ top-level category dirs
- every entry carries the full descriptor shape (name/label/accent/icon/order)
- orders are unique 1..N
- agents/, skills/, workflows/ JSON category trees are consistent (check-catalog)
- regenerating divisions.json is byte-identical (no drift)
"""

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIVISIONS_PATH = ROOT / "divisions.json"
UA = ROOT / "universal-agents"

REQUIRED_FIELDS = ("name", "label", "accent", "icon", "order", "description")


def load_divisions():
    with open(DIVISIONS_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return manifest


MANIFEST = load_divisions()
DIVISIONS = MANIFEST["divisions"]

UA_DIRS = {p.name for p in UA.iterdir() if p.is_dir()}


class TestDivisionsManifestKeys(unittest.TestCase):
    def test_manifest_has_version(self):
        self.assertIn("version", MANIFEST)

    def test_keys_match_universal_agents_dirs(self):
        self.assertEqual(set(DIVISIONS), UA_DIRS)

    def test_no_extra_or_missing_dirs(self):
        self.assertEqual(UA_DIRS - set(DIVISIONS), set())
        self.assertEqual(set(DIVISIONS) - UA_DIRS, set())


class TestDivisionsEntryShape(unittest.TestCase):
    def test_required_fields_present(self):
        for key, entry in DIVISIONS.items():
            for field in REQUIRED_FIELDS:
                self.assertIn(field, entry, f"{key} missing {field}")

    def test_name_matches_key(self):
        for key, entry in DIVISIONS.items():
            self.assertEqual(entry["name"], key)

    def test_accent_is_hex_color(self):
        for key, entry in DIVISIONS.items():
            accent = entry["accent"]
            self.assertRegex(accent, r"^#[0-9A-F]{6}$", key)

    def test_icon_is_non_empty(self):
        for key, entry in DIVISIONS.items():
            self.assertTrue(entry["icon"], key)

    def test_label_and_description_non_empty(self):
        for key, entry in DIVISIONS.items():
            self.assertTrue(entry["label"], key)
            self.assertTrue(entry["description"], key)

    def test_description_mentions_label(self):
        for key, entry in DIVISIONS.items():
            self.assertIn(entry["label"], entry["description"], key)

    def test_orders_unique_1_to_n(self):
        orders = [entry["order"] for entry in DIVISIONS.values()]
        self.assertEqual(sorted(orders), list(range(1, len(DIVISIONS) + 1)))


class TestCatalogConsistency(unittest.TestCase):
    def test_check_catalog_passes(self):
        result = subprocess.run(
            [os.sys.executable, str(ROOT / "scripts" / "check-catalog.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TestDivisionsRegeneration(unittest.TestCase):
    def test_regeneration_is_byte_identical(self):
        before = (DIVISIONS_PATH).read_bytes()
        result = subprocess.run(
            [os.sys.executable, str(ROOT / "scripts" / "generate-divisions.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = (DIVISIONS_PATH).read_bytes()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()