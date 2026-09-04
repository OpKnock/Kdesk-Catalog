"""Regression tests for bugs found during the full-CLI audit pass.

- wiring text mode crashed: len() on bool `verified`
- partial semver constraints (^1.0, ~1.2, >=1) never matched
- diagnose report header showed detected platform, not requested target
- compatibility._analyze_agent raised UnboundLocalError when content
  lacked a platforms.<platform> section
"""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kdesk.cli import main as cli_main
from kdesk.versioning import (
    VersionResolver,
    build_available_versions,
    parse_constraint,
)


class TestPartialSemverConstraints(unittest.TestCase):
    def test_partial_versions_default_to_zero(self):
        self.assertEqual(parse_constraint("^2").base, (2, 0, 0))
        self.assertEqual(parse_constraint("^1.0").base, (1, 0, 0))
        self.assertEqual(parse_constraint("~1.2").base, (1, 2, 0))
        self.assertEqual(parse_constraint(">=1").base, (1, 0, 0))

    def test_partial_caret_satisfies(self):
        c = parse_constraint("^1.0")
        self.assertTrue(c.satisfies("1.0.0"))
        self.assertTrue(c.satisfies("1.9.3"))
        self.assertFalse(c.satisfies("2.0.0"))

    def test_resolver_with_partial_constraint(self):
        available = build_available_versions({"my-agent": True})
        r = VersionResolver()
        self.assertEqual(r.resolve("my-agent@^1.0", available), "my-agent@1.0.0")
        self.assertIsNone(r.resolve("my-agent@^2.0", available))

    def test_garbage_constraint_matches_nothing(self):
        c = parse_constraint("bogus!!")
        self.assertFalse(c.satisfies("1.0.0"))


class TestWiringTextMode(unittest.TestCase):
    def test_wiring_text_mode_exits_zero(self):
        code = cli_main(["wiring", "--root", str(ROOT)])
        self.assertEqual(code, 0)


class TestCompatibilityNoPlatformSection(unittest.TestCase):
    def _engine(self):
        from kdesk.compatibility import (
            CompatibilityEngine,
            get_platform_profile,
        )
        eng = CompatibilityEngine.__new__(CompatibilityEngine)
        eng.platform = "cursor"
        eng.profile = get_platform_profile("cursor")
        return eng

    def test_agent_without_platforms_section(self):
        eng = self._engine()
        scanned = SimpleNamespace(
            rel_path="agents/test-agent.md",
            path=Path("agents/test-agent.md"),
            parse_error=None,
            content={
                "name": "test-agent",
                "description": "x",
                "tools": ["Read"],
            },
        )
        issues = eng._analyze_agent(scanned)  # must not raise UnboundLocalError
        self.assertIsInstance(issues, list)

    def test_agent_with_other_platform_section(self):
        eng = self._engine()
        scanned = SimpleNamespace(
            rel_path="agents/test-agent.md",
            path=Path("agents/test-agent.md"),
            parse_error=None,
            content={
                "name": "test-agent",
                "description": "x",
                "platforms": {"claude_code": {"tools": ["Bash"]}},
            },
        )
        issues = eng._analyze_agent(scanned)
        self.assertIsInstance(issues, list)


class TestDiagnoseUsesRequestedPlatform(unittest.TestCase):
    def test_report_platform_matches_request(self):
        import tempfile
        from kdesk.adapters import AdapterRegistry
        from kdesk.doctor import Doctor

        with tempfile.TemporaryDirectory() as tmp:
            registry = AdapterRegistry(ROOT)
            doctor = Doctor(registry, base=Path(tmp), registry_root=ROOT)
            result = doctor.diagnose(
                platform="cursor",
                project_root=Path(tmp),
                fix=False,
                dry_run=True,
            )
            self.assertEqual(result["report"].platform, "cursor")


if __name__ == "__main__":
    unittest.main()
