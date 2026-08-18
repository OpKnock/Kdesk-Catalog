"""Marketplace manifest tests.

Assert that per-platform marketplaces (marketplaces/*.marketplace.json):
- exist for every active platform in tools.json (format != "none")
- carry the manifest shape (version/name/label/format/description/entries)
- list the full catalog (agents + skills per platform, derived from the
  committed, freshness-gated reports/catalog-stats.json)
- entries are sorted by id and carry required fields
- category accents/icons resolve from divisions.json
- the marketplace report exists and is non-empty
"""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MARKETPLACES_DIR = ROOT / "marketplaces"
REPORT_PATH = ROOT / "reports" / "marketplace-report.md"

with open(ROOT / "reports" / "catalog-stats.json", "r", encoding="utf-8") as f:
    STATS = json.load(f)
AGENT_COUNT = STATS["agents"]
SKILL_COUNT = STATS["skills"]
ENTRY_COUNT = AGENT_COUNT + SKILL_COUNT

REQUIRED_ENTRY_FIELDS = ("id", "name", "label", "description", "category")

with open(ROOT / "tools.json", "r", encoding="utf-8") as f:
    TOOLS = json.load(f)["tools"]
ACTIVE_PLATFORMS = sorted(
    k for k, v in TOOLS.items() if v.get("format") != "none"
)

with open(ROOT / "divisions.json", "r", encoding="utf-8") as f:
    DIVISIONS = json.load(f)["divisions"]


def load_marketplace(name):
    path = MARKETPLACES_DIR / f"{name}.marketplace.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class TestMarketplaceManifests(unittest.TestCase):
    def test_manifest_per_active_platform(self):
        files = {p.stem[: -len(".marketplace")] for p in MARKETPLACES_DIR.glob("*.marketplace.json")}
        self.assertEqual(files, set(ACTIVE_PLATFORMS))

    def test_manifest_shape(self):
        for name in ACTIVE_PLATFORMS:
            manifest = load_marketplace(name)
            self.assertEqual(manifest["version"], "1.0.0", name)
            self.assertEqual(manifest["name"], name)
            self.assertTrue(manifest["label"], name)
            self.assertTrue(manifest["format"], name)
            self.assertTrue(manifest["description"], name)
            self.assertIsInstance(manifest["entries"], list)

    def test_entries_cover_full_catalog(self):
        for name in ACTIVE_PLATFORMS:
            manifest = load_marketplace(name)
            self.assertEqual(len(manifest["entries"]), ENTRY_COUNT, name)

    def test_entries_sorted_by_id(self):
        for name in ACTIVE_PLATFORMS:
            manifest = load_marketplace(name)
            ids = [entry["id"] for entry in manifest["entries"]]
            self.assertEqual(ids, sorted(ids), name)
            self.assertEqual(len(ids), len(set(ids)), name)

    def test_entry_required_fields(self):
        for name in ACTIVE_PLATFORMS:
            manifest = load_marketplace(name)
            for entry in manifest["entries"]:
                for field in REQUIRED_ENTRY_FIELDS:
                    self.assertIn(field, entry, f"{name}/{entry['id']} missing {field}")
                    self.assertTrue(entry[field], f"{name}/{entry['id']} empty {field}")

    def test_entry_accent_icon_resolve_from_divisions(self):
        for name in ACTIVE_PLATFORMS:
            manifest = load_marketplace(name)
            for entry in manifest["entries"]:
                self.assertIn(entry["category"], DIVISIONS, f"{name}/{entry['id']}")
                self.assertIn("accent", entry, f"{name}/{entry['id']}")
                self.assertIn("icon", entry, f"{name}/{entry['id']}")

    def test_report_exists(self):
        self.assertTrue(REPORT_PATH.exists())
        text = REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Marketplace Report", text)
        self.assertIn(str(ENTRY_COUNT), text)


if __name__ == "__main__":
    unittest.main()