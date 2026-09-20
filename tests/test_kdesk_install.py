"""Phase 8: installer filters (--scope / --tool) and CLI wiring.

Covers:
- scope=agents / scope=skills restrict installed files by kind
- scope on a flat-layout platform (cursor) is rejected
- tool=NAME restricts installs to definitions invoking that tool
- unknown scope / tool are usage errors (exit 2 from the CLI)
- dry-run writes nothing and records no manifest
- default kwargs preserve the original install contract
"""

import json
import tempfile
import unittest
from pathlib import Path

from kdesk.adapters import AdapterRegistry
from kdesk.cli import main as cli_main
from kdesk.installer import InstallError, Installer

ROOT = Path(__file__).resolve().parents[1]


def _build_index():
    index = {}
    for base in (ROOT / "agents" / "json", ROOT / "skills" / "json"):
        for path in base.rglob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            tools = data.get("tools")
            if isinstance(tools, list):
                index[path.stem] = set(tools)
    return index


DEF_INDEX = _build_index()


class InstallScopeTests(unittest.TestCase):
    def setUp(self):
        self.registry = AdapterRegistry(ROOT)
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _installed_files(self):
        root = self.base / ".claude"
        return [p for p in root.rglob("*") if p.is_file()]

    def test_scope_agents_installs_only_agents(self):
        installer = Installer(self.registry, home_dir=self.base)
        result = installer.install("claude_code", base=self.base, scope="agents")
        files = self._installed_files()
        self.assertTrue(files)
        for path in files:
            self.assertIn("agents", path.parts)
        self.assertNotIn("skills", [p.parts for p in files])
        self.assertEqual(sum(r["files"] for r in result["results"]), len(files))

    def test_scope_skills_installs_only_skills(self):
        installer = Installer(self.registry, home_dir=self.base)
        result = installer.install("claude_code", base=self.base, scope="skills")
        files = self._installed_files()
        self.assertTrue(files)
        for path in files:
            self.assertIn("skills", path.parts)
        self.assertEqual(sum(r["files"] for r in result["results"]), len(files))

    def test_scope_on_flat_platform_rejected(self):
        installer = Installer(self.registry)
        with self.assertRaises(InstallError):
            installer.install("cursor", base=self.base, scope="agents")


class InstallToolFilterTests(unittest.TestCase):
    def setUp(self):
        self.registry = AdapterRegistry(ROOT)
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.index = DEF_INDEX

    def tearDown(self):
        self.tmp.cleanup()

    def test_tool_filter_installs_only_invoking_definitions(self):
        installer = Installer(self.registry, home_dir=self.base)
        result = installer.install("claude_code", base=self.base, tool="python")
        self.assertTrue(self.index, "def index should not be empty")
        matching = {stem for stem, tools in self.index.items()
                    if "python" in tools}
        self.assertTrue(matching)
        installed = [p for p in (self.base / ".claude").rglob("*")
                     if p.is_file()]
        self.assertTrue(installed)
        for path in installed:
            self.assertIn(path.stem, matching)
        with open(ROOT / "reports" / "catalog-stats.json", "r", encoding="utf-8") as f:
            total_agents = json.load(f)["agents"]
        self.assertLess(len(installed), total_agents)

    def test_unknown_tool_rejected(self):
        installer = Installer(self.registry)
        with self.assertRaises(InstallError):
            installer.install("claude_code", base=self.base, tool="not-a-tool")

    def test_unknown_scope_rejected(self):
        installer = Installer(self.registry)
        with self.assertRaises(InstallError):
            installer.install("claude_code", base=self.base, scope="bogus")


class InstallDryRunTests(unittest.TestCase):
    def setUp(self):
        self.registry = AdapterRegistry(ROOT)
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_dry_run_writes_nothing(self):
        installer = Installer(self.registry, dry_run=True, home_dir=self.base)
        result = installer.install("claude_code", base=self.base)
        self.assertEqual(result["results"][0]["status"], "DRY-RUN")
        self.assertTrue(result["results"][0]["copied"] > 0)
        self.assertFalse((self.base / ".claude").exists())
        self.assertFalse((self.base / ".kdesk" / "manifest.json").exists())

    def test_default_kwargs_preserve_contract(self):
        installer = Installer(self.registry, home_dir=self.base)
        result = installer.install("claude_code", base=self.base)
        self.assertEqual(result["results"][0]["status"], "OK")
        self.assertTrue((self.base / ".claude" / "agents").is_dir())


class InstallCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_cli_scope_flag(self):
        code = cli_main(["install", "claude_code", "--scope", "agents",
                         "--dry-run", "--base", str(self.base),
                         "--home", str(self.base)])
        self.assertEqual(code, 0)
        self.assertFalse((self.base / ".claude").exists())

    def test_cli_unknown_tool_exit_2(self):
        code = cli_main(["install", "claude_code", "--tool", "not-a-tool",
                         "--dry-run", "--base", str(self.base),
                         "--home", str(self.base)])
        self.assertEqual(code, 2)

    def test_cli_unknown_scope_exit_2(self):
        code = cli_main(["install", "claude_code", "--scope", "bogus",
                         "--dry-run", "--base", str(self.base),
                         "--home", str(self.base)])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()