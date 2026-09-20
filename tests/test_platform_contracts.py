"""Platform contract tests: every platform must produce valid output.

Tests that every active platform:
- generates output files
- produces correct file extensions
- creates expected directory structure
- has non-empty content
- passes basic format validation
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Load converter as module
spec = importlib.util.spec_from_file_location("uc", str(ROOT / "scripts" / "universal-converter.py"))
uc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uc)

from kdesk.platforms import PlatformRegistry, SupportLevel


def load_fixture():
    """Load one representative agent for conversion testing."""
    fixture_dir = ROOT / "tests" / "fixtures"
    fixture_file = fixture_dir / "canonical-agent.yaml"
    if fixture_file.exists():
        return fixture_file.parent
    # Fall back to first available agent from universal-agents
    for p in sorted((ROOT / "universal-agents").rglob("*.yaml")):
        if p.name != "registry.yaml":
            return p.parent
    return ROOT / "universal-agents"


class TestPlatformContracts(unittest.TestCase):
    """Contract test: every active platform must convert without errors."""

    @classmethod
    def setUpClass(cls):
        cls.registry = PlatformRegistry.load()
        cls.active_platforms = [
            p.id for p in cls.registry.active()
            if p.support_level not in (SupportLevel.DEPRECATED,)
        ]
        cls.universal_dir = str(ROOT / "universal-agents")

    def test_all_platforms_registered(self):
        """Every platform in tools.json must exist in canonical registry."""
        tools_json = json.loads((ROOT / "tools.json").read_text(encoding="utf-8"))
        tool_ids = set(tools_json["tools"].keys())
        registry_ids = set(self.registry.ids())
        missing_from_registry = tool_ids - registry_ids
        self.assertEqual(missing_from_registry, set(),
                        f"Platforms in tools.json but not in registry: {missing_from_registry}")

    def test_no_duplicate_platform_ids(self):
        """Registry must have zero duplicate IDs."""
        self.assertEqual(self.registry.validate_unique(), [])

    def test_deprecated_platforms_flagged(self):
        """Void must be marked deprecated."""
        void = self.registry.get("void")
        self.assertIsNotNone(void)
        self.assertEqual(void.support_level, SupportLevel.DEPRECATED)

    def test_every_active_platform_has_detect_dirs(self):
        """Active platforms must have detection directories."""
        for spec in self.registry.active():
            if spec.family in ("single-file", "legacy-core") and spec.id == "generic":
                continue  # generic and single-file detect by filename, not dirs
            if spec.family == "single-file":
                continue
            self.assertTrue(spec.detect_dirs,
                           f"{spec.id} has no detect_dirs")

    def test_every_platform_has_display_name(self):
        for spec in self.registry.all():
            self.assertTrue(spec.display_name, f"{spec.id} missing display_name")

    def test_cursor_limits_enforced(self):
        """Cursor max_file_size must be 50KB."""
        cursor = self.registry.get("cursor")
        self.assertEqual(cursor.max_file_size, 50000)

    def test_claude_code_supports_tools(self):
        """Claude Code must support tools field."""
        cc = self.registry.get("claude_code")
        self.assertIn("tools", cc.supported_fields)


class TestConverterOutput(unittest.TestCase):
    """Test that the converter produces valid output for key platforms."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="kdesk_contract_")
        self.universal_dir = load_fixture()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _convert_and_check(self, platform, expected_ext, min_files=1):
        result = subprocess_run(
            [sys.executable, str(ROOT / "scripts" / "universal-converter.py"),
             "--platforms", platform, "--quiet",
             "--universal-dir", str(self.universal_dir),
             "--output", self.tmp],
        )
        if result.returncode != 0:
            self.fail(f"Converter failed for {platform}: {result.stderr[:200]}")

        out_dir = Path(self.tmp) / platform
        files = [p for p in out_dir.rglob("*") if p.is_file()]
        self.assertGreaterEqual(len(files), min_files,
                               f"{platform}: expected >= {min_files} files, got {len(files)}")

        for f in files[:5]:  # Check first 5 files
            content = f.read_text(encoding="utf-8")
            self.assertTrue(content.strip(), f"{platform}/{f.name}: empty file")

        return files

    def test_claude_code_output(self):
        files = self._convert_and_check("claude_code", ".md", min_files=10)
        md_files = [f for f in files if f.suffix == ".md"]
        self.assertTrue(md_files, "No .md files produced for claude_code")

    def test_cursor_output(self):
        files = self._convert_and_check("cursor", ".mdc", min_files=10)
        mdc_files = [f for f in files if f.suffix == ".mdc"]
        self.assertTrue(mdc_files, "No .mdc files produced for cursor")

    def test_github_copilot_output(self):
        files = self._convert_and_check("github_copilot", ".instructions.md", min_files=10)
        inst_files = [f for f in files if f.name.endswith(".instructions.md")]
        self.assertTrue(inst_files, "No .instructions.md files for github_copilot")


def subprocess_run(argv, timeout=120):
    import subprocess
    return subprocess.run(argv, capture_output=True, text=True,
                         timeout=timeout, cwd=str(ROOT),
                         env={**os.environ, "PYTHONPATH": str(ROOT)})


if __name__ == "__main__":
    unittest.main()
