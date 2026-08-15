import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c = load_module("universal_converter", "universal-converter.py")


class TestParsePlatforms(unittest.TestCase):
    def test_comma_separated(self):
        self.assertEqual(c.parse_platforms(["claude_code,cursor,opencode"]),
                         ["claude_code", "cursor", "opencode"])

    def test_space_separated(self):
        self.assertEqual(c.parse_platforms(["claude_code", "cursor", "opencode"]),
                         ["claude_code", "cursor", "opencode"])

    def test_mixed_separators(self):
        self.assertEqual(c.parse_platforms(["claude_code,cursor", "opencode", "generic"]),
                         ["claude_code", "cursor", "opencode", "generic"])

    def test_all_expands(self):
        self.assertEqual(c.parse_platforms(["all"]), list(c.ALL_PLATFORMS))
        self.assertEqual(c.parse_platforms(["claude_code,all"]), list(c.ALL_PLATFORMS))

    def test_single_platform(self):
        self.assertEqual(c.parse_platforms(["cursor"]), ["cursor"])

    def test_unknown_platform_raises(self):
        with self.assertRaises(ValueError):
            c.parse_platforms(["bad_platform"])
        with self.assertRaises(ValueError):
            c.parse_platforms(["claude_code,bad_platform"])

    def test_whitespace_stripped(self):
        self.assertEqual(c.parse_platforms([" claude_code , cursor "]),
                         ["claude_code", "cursor"])


if __name__ == "__main__":
    unittest.main()
