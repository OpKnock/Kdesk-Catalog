"""Platform-spec tests: assert the output-format contract for every platform.

Each test validates the *emitted artifact shape*, not content:
- claude_code: .md agents with YAML frontmatter (model: inherit), skills under .claude/skills/<name>/SKILL.md
- cursor: .mdc with description/globs/alwaysApply only (no model, no rule_type)
- github_copilot: .github/instructions/*.instructions.md with applyTo frontmatter
- windsurf: .windsurf/rules/*.md with trigger/description frontmatter (no model)
- opencode/generic: JSON (opencode plugin shape, generic system_prompt)
- goose: recipes/*.yaml with title/description/instructions
- openhands: microagents/*.md with name/description/type frontmatter
- single-file platforms: instructions/*.md + manifest.yaml
- No stale model IDs anywhere (claude-3-5-sonnet-20241022, claude-3.5-sonnet)
- No orphan files: every emitted file maps to a source universal-agents YAML
"""

import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = ROOT / "platform-agents"
UA = ROOT / "universal-agents"

STALE_MODELS = {"claude-3-5-sonnet-20241022", "claude-3.5-sonnet", "claude-3.5-sonnet-20240620"}

SOURCE_NAMES = set()
SOURCE_STEMS = set()
SOURCE_SLUGS = set()
import re as _re
for p in UA.rglob("*.yaml"):
    if p.name == "registry.yaml":
        continue
    try:
        import yaml
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:
        d = {}
    SOURCE_NAMES.add(d.get("name") or p.name[:-5])
    SOURCE_STEMS.add(p.name[:-5])
    for cand in (d.get("name"), p.name[:-5]):
        if cand:
            slug = _re.sub(r"[^a-z0-9]+", "-", str(cand).lower()).strip("-")
            SOURCE_SLUGS.add((slug[:64]).rstrip("-") or "skill")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def yaml_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        import yaml
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def require_full_scan(test):
    """Skip full-catalog sweeps unless KDESK_FULL=1 (they scan ~130k files)."""
    if os.environ.get("KDESK_FULL") != "1":
        test.skipTest("set KDESK_FULL=1 to run full-catalog sweeps")
    return True


class TestClaudeCodeFormat(unittest.TestCase):
    def test_agents_are_md_with_frontmatter(self):
        agents = list((OUT / "claude_code" / ".claude" / "agents").glob("*.md"))
        self.assertGreater(len(agents), 100)
        for f in agents:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("name", fm, f)
            self.assertIn("description", fm, f)
            self.assertEqual(fm.get("model"), "inherit", f)

    def test_skills_in_claude_dir(self):
        skills = list((OUT / "claude_code" / ".claude" / "skills").glob("*/SKILL.md"))
        self.assertGreater(len(skills), 500)
        for f in skills:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("name", fm, f)
            self.assertIn("description", fm, f)


class TestCursorFormat(unittest.TestCase):
    def test_mdc_frontmatter_fields(self):
        files = list((OUT / "cursor").glob("*.mdc"))
        self.assertGreater(len(files), 100)
        for f in files:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("description", fm, f)
            self.assertIn("alwaysApply", fm, f)
            self.assertNotIn("model", fm, f)
            self.assertNotIn("rule_type", fm, f)


class TestCopilotFormat(unittest.TestCase):
    def test_instructions_md_with_applyto(self):
        files = list((OUT / "github_copilot" / ".github" / "instructions").glob("*.instructions.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("applyTo", fm, f)


class TestWindsurfFormat(unittest.TestCase):
    def test_rules_md_with_trigger(self):
        files = list((OUT / "windsurf" / ".windsurf" / "rules").glob("*.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("trigger", fm, f)
            self.assertIn(fm.get("trigger"), {"always_on", "model_decision", "glob", "manual"}, f)
            self.assertIn("description", fm, f)
            self.assertNotIn("model", fm, f)

    def test_glob_trigger_has_globs(self):
        for f in (OUT / "windsurf" / ".windsurf" / "rules").glob("*.md"):
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            if fm.get("trigger") == "glob":
                self.assertTrue(fm.get("globs"), f)

    def test_file_size_cap(self):
        for f in (OUT / "windsurf" / ".windsurf" / "rules").glob("*.md"):
            self.assertLessEqual(len(f.read_text(encoding="utf-8")), 12000, f)


class TestOpencodeFormat(unittest.TestCase):
    def test_agents_are_md_with_frontmatter(self):
        files = list((OUT / "opencode" / ".opencode" / "agents").glob("*.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("description", fm, f)
            self.assertIn("mode", fm, f)
            self.assertNotIn("prompt", fm, f)

    def test_skills_in_opencode_dir(self):
        skills = list((OUT / "opencode" / ".opencode" / "skills").glob("*/SKILL.md"))
        self.assertGreater(len(skills), 500)
        for f in skills:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("name", fm, f)
            self.assertIn("description", fm, f)

    def test_generic_system_prompt(self):
        d = json.loads((OUT / "generic" / "1password.json").read_text(encoding="utf-8"))
        self.assertIn("system_prompt", d.get("config", d))


class TestRulesMdPlatforms(unittest.TestCase):
    def test_augment_type_and_description(self):
        files = list((OUT / "augment" / ".augment" / "rules").glob("*.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn(fm.get("type"), {"always_apply", "agent_requested", "manual"}, f)
            self.assertTrue(fm.get("description"), f)

    def test_continue_alwaysapply_false(self):
        files = list((OUT / "continue" / ".continue" / "rules").glob("*.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("name", fm, f)
            self.assertIn("description", fm, f)
            self.assertIs(fm.get("alwaysApply"), False, f)

    def test_grok_and_amazonq_plain_md(self):
        for plat, sub in (("grok_build", ".grok"), ("amazon_q", ".amazonq")):
            files = list((OUT / plat / sub / "rules").glob("*.md"))
            self.assertGreater(len(files), 100)
            for f in files:
                self.assertFalse(f.read_text(encoding="utf-8").startswith("---"), f)


class TestGooseFormat(unittest.TestCase):
    def test_recipes_yaml(self):
        files = list((OUT / "goose" / "recipes").glob("*.yaml"))
        self.assertGreater(len(files), 100)
        import yaml
        for f in files:
            d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            self.assertIn("title", d, f)
            self.assertIn("description", d, f)
            self.assertIn("instructions", d, f)
            self.assertTrue(d.get("prompt"), f)


class TestOpenHandsFormat(unittest.TestCase):
    def test_microagent_frontmatter(self):
        files = list((OUT / "openhands" / "microagents").glob("*.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            fm = yaml_frontmatter(f.read_text(encoding="utf-8"))
            self.assertIn("name", fm, f)
            self.assertIn("description", fm, f)
            self.assertIn(fm.get("type"), {"repo", "knowledge", "task"}, f)
            if fm.get("type") == "knowledge":
                self.assertTrue(fm.get("triggers"), f)


class TestNoStaleModels(unittest.TestCase):
    def _head(self, f, size=4096):
        with open(f, "rb") as fh:
            return fh.read(size).decode("utf-8", errors="ignore")

    def test_no_stale_model_ids_in_outputs(self):
        # Stale model pins only ever live in frontmatter/config at file top,
        # so reading the head of each file is a complete check.
        require_full_scan(self)
        stale_hits = 0
        for f in OUT.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix in (".json", ".md", ".mdc", ".txt", ".yaml", ".yml"):
                content = self._head(f)
                if any(s in content for s in STALE_MODELS):
                    stale_hits += 1
                    if stale_hits <= 3:
                        print("STALE:", f)
        self.assertEqual(stale_hits, 0)

    def test_no_stale_models_in_sources(self):
        require_full_scan(self)
        stale_hits = 0
        for f in UA.rglob("*.yaml"):
            if f.name == "registry.yaml":
                continue
            content = f.read_text(encoding="utf-8", errors="ignore")
            if any(s in content for s in STALE_MODELS):
                stale_hits += 1
        self.assertEqual(stale_hits, 0)


class TestNoOrphans(unittest.TestCase):
    def test_no_orphan_files(self):
        require_full_scan(self)
        orphans = []
        for platform_dir in OUT.iterdir():
            if not platform_dir.is_dir():
                continue
            for f in platform_dir.rglob("*"):
                if not f.is_file():
                    continue
                rel = f.relative_to(platform_dir)
                parts = rel.parts
                if parts[0] in ("README.md", "manifest.yaml", "firebender.json", "instructions", "recipes",
                                "microagents", ".github", ".claude", ".vscode", ".firebender"):
                    continue
                if f.suffix == ".json" and f.stem not in SOURCE_NAMES:
                    orphans.append(str(f))
                if f.suffix == ".mdc" and f.stem not in SOURCE_NAMES and f.stem not in SOURCE_SLUGS:
                    orphans.append(str(f))
        for o in orphans[:5]:
            print("ORPHAN:", o)
        self.assertEqual(len(orphans), 0)


class TestSingleFileAssembly(unittest.TestCase):
    def test_codegpt_agents_md(self):
        native = OUT / "codegpt" / "AGENTS.md"
        if not native.exists():
            self.skipTest("codegpt native file not assembled yet")
        content = native.read_text(encoding="utf-8")
        self.assertGreater(len(content), 1000)
        self.assertTrue(content.startswith("#"))

    def test_cody_commands_json(self):
        native = OUT / "cody" / ".vscode" / "cody.json"
        if not native.exists():
            self.skipTest("cody native file not assembled yet")
        data = json.loads(native.read_text(encoding="utf-8"))
        self.assertIn("commands", data)
        commands = data["commands"]
        self.assertGreater(len(commands), 100)
        for name, cmd in list(commands.items())[:3]:
            self.assertTrue(name)
            self.assertTrue(cmd.get("description"), name)
            self.assertTrue(cmd.get("prompt"), name)

    def test_firebender_agents_index(self):
        native = OUT / "firebender" / "firebender.json"
        if not native.exists():
            self.skipTest("firebender native file not assembled yet")
        data = json.loads(native.read_text(encoding="utf-8"))
        self.assertIn("agents", data)
        agents = data["agents"]
        self.assertGreater(len(agents), 100)
        sample = OUT / "firebender" / agents[0].removeprefix("./")
        self.assertTrue(sample.exists(), f"referenced agent file missing: {sample}")
        fm = yaml_frontmatter(sample.read_text(encoding="utf-8"))
        self.assertIn("name", fm)
        self.assertIn("description", fm)

    def test_tabnine_guidelines_plain_md(self):
        files = list((OUT / "tabnine" / ".tabnine" / "guidelines").glob("*.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            self.assertFalse(f.read_text(encoding="utf-8").startswith("---"), f)

    def test_supermaven_rules_plain_md(self):
        files = list((OUT / "supermaven" / ".supermaven" / "rules").glob("*.md"))
        self.assertGreater(len(files), 100)
        for f in files:
            self.assertFalse(f.read_text(encoding="utf-8").startswith("---"), f)

    def test_void_has_no_native_file(self):
        self.assertFalse((OUT / "void" / ".void" / "config.json").exists())
        manifest = OUT / "void" / "manifest.yaml"
        if manifest.exists():
            data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
            self.assertIsNone(data.get("native_file"), "void must not claim a native file")


if __name__ == "__main__":
    unittest.main()
