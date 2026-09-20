#!/usr/bin/env python3
"""
Deep audit of Kdesk-Catalog. Runs 10 checks and prints a JSON summary.
1. YAML parse errors
2. Required fields (name, description, version, instructions, capabilities)
3. Short instructions (<200)
4. Zero-command agents (agents MUST have commands in capabilities)
5. Duplicate names
6. Duplicate command sets
7. Command quality: empty strings, pipes to nothing, placeholders
8. Platform JSON parse validity (claude_code, opencode, windsurf, generic)
9. Copilot MD files have content
10. Cursor MDC files have content
11. New platform outputs: file counts per platform, non-empty files,
    SKILL.md frontmatter (name+description), Goose recipe validity
"""
import os
import sys
import json
import yaml
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
UA = ROOT / "universal-agents"
PA = ROOT / "platform-agents"

sys.path.insert(0, str(ROOT / "scripts"))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "universal_converter", ROOT / "scripts" / "universal-converter.py")
uc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uc)

PLACEHOLDER_PATTERNS = ["<your_", "<placeholder", "example.com/your", "TODO:", "coming soon", "lorem ipsum", "{{your", "{{placeholder"]

def scan():
    report = {
        "total_yaml": 0, "agents": 0, "skills": 0,
        "parse_errors": [], "missing_fields": [], "short_instructions": [],
        "zero_cmd_agents": [], "dup_names": [], "dup_cmd_sets": [],
        "bad_commands": [], "platform_json_errors": [], "copilot_empty": [],
        "cursor_empty": [],
    }
    names = Counter()
    cmd_sets = Counter()
    name2file = {}

    for path in sorted(UA.rglob("*.yaml")):
        if path.name == "registry.yaml":
            continue
        report["total_yaml"] += 1
        rel = str(path.relative_to(UA))
        is_skill = "/skill/" in rel.replace("\\", "/") or path.name.endswith("-skill.yaml")
        if is_skill:
            report["skills"] += 1
        else:
            report["agents"] += 1

        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as e:
            report["parse_errors"].append(f"{rel}: {e}")
            continue
        if not isinstance(doc, dict):
            report["parse_errors"].append(f"{rel}: not a dict")
            continue

        for fld in ("name", "description", "version", "instructions", "capabilities"):
            if fld not in doc or doc[fld] in (None, [], ""):
                report["missing_fields"].append(f"{rel}: missing {fld}")

        n = doc.get("name", "")
        names[n] += 1
        name2file.setdefault(n, rel)

        if len(str(doc.get("instructions", ""))) < 200:
            report["short_instructions"].append(f"{rel} ({len(str(doc.get('instructions','')))} chars)")

        caps = doc.get("capabilities") or []
        total_cmds = 0
        for cap in caps:
            if not isinstance(cap, dict):
                report["bad_commands"].append(f"{rel}: capability not dict")
                continue
            cmds = cap.get("commands") or []
            for c in cmds:
                if not isinstance(c, str) or not c.strip():
                    report["bad_commands"].append(f"{rel}: empty command")
                    continue
                low = c.lower()
                if any(p.lower() in low for p in PLACEHOLDER_PATTERNS):
                    report["bad_commands"].append(f"{rel}: placeholder '{c[:60]}'")
                total_cmds += 1
            if cmds:
                cmd_sets[tuple(cmds)] += 1
        if not is_skill and total_cmds == 0:
            report["zero_cmd_agents"].append(rel)

    report["dup_names"] = [f"{n} ({k} files)" for n, k in names.items() if k > 1]
    report["dup_cmd_sets"] = [f"{k}x {list(v)[0][:50]}" for v, k in cmd_sets.items() if k > 1]

    for plat in ("claude_code", "opencode", "windsurf", "generic"):
        pd = PA / plat
        for f in pd.glob("**/*.json"):
            try:
                json.loads(f.read_text(encoding="utf-8"))
            except Exception as e:
                report["platform_json_errors"].append(f"{plat}/{f.name}: {e}")

    for f in (PA / "github_copilot").glob("**/*.md"):
        if not f.read_text(encoding="utf-8").strip():
            report["copilot_empty"].append(f.name)
    for f in (PA / "cursor").glob("**/*.mdc"):
        raw = f.read_text(encoding="utf-8", errors="replace")
        if not raw.strip():
            report["cursor_empty"].append(f.name)
            continue
        if not raw.startswith("---"):
            report["skillmd_missing_frontmatter"].append(f"cursor/{f.name}: no frontmatter")
            continue
        try:
            fm = yaml.safe_load(raw.split("---", 2)[1])
            if not (fm and fm.get("name") and fm.get("description")):
                report["skillmd_missing_frontmatter"].append(f"cursor/{f.name}: bad frontmatter")
        except Exception as e:
            report["skillmd_missing_frontmatter"].append(f"cursor/{f.name}: {e}")

    # 11. New platform outputs
    report["platform_file_counts"] = {}
    report["skillmd_missing_frontmatter"] = []
    report["empty_platform_files"] = []
    report["recipe_parse_errors"] = []

    for plat, skills_dir in uc.NEW_SKILL_PLATFORMS.items():
        sd = PA / plat / skills_dir
        files = list(sd.rglob("SKILL.md"))
        report["platform_file_counts"][plat] = len(files)
        for f in files:
            if f.stat().st_size == 0:
                report["empty_platform_files"].append(f"{plat}/{f.relative_to(PA)}")
                continue
            raw = f.read_text(encoding="utf-8", errors="replace")
            if not raw.startswith("---"):
                report["skillmd_missing_frontmatter"].append(f"{plat}/{f.relative_to(PA)}: no frontmatter")
                continue
            try:
                fm = yaml.safe_load(raw.split("---", 2)[1])
            except Exception as e:
                report["skillmd_missing_frontmatter"].append(f"{plat}/{f.relative_to(PA)}: {e}")
                continue
            if not (fm and fm.get("name") and fm.get("description")):
                report["skillmd_missing_frontmatter"].append(f"{plat}/{f.relative_to(PA)}: missing name/description")
            elif str(fm["name"]) != f.parent.name:
                report["skillmd_missing_frontmatter"].append(
                    f"{plat}/{f.relative_to(PA)}: name '{fm['name']}' != folder '{f.parent.name}'")

    for plat, (rdir, _kind) in uc.NEW_RULES_PLATFORMS.items():
        rd = PA / plat / rdir
        files = [f for f in rd.rglob("*") if f.is_file() and f.suffix in (".md", ".mdc")]
        report["platform_file_counts"][plat] = len(files)
        for f in files:
            if f.stat().st_size == 0:
                report["empty_platform_files"].append(f"{plat}/{f.relative_to(PA)}")
                continue
            raw = f.read_text(encoding="utf-8", errors="replace")
            if raw.startswith("---"):
                try:
                    fm = yaml.safe_load(raw.split("---", 2)[1])
                except Exception as e:
                    report["skillmd_missing_frontmatter"].append(f"{plat}/{f.relative_to(PA)}: {e}")

    for plat, sub in {"goose": "recipes", "aider": "conventions", "openhands": "microagents"}.items():
        pd2 = PA / plat / sub
        files = [f for f in pd2.rglob("*") if f.is_file() and f.suffix in (".md", ".yaml")]
        report["platform_file_counts"][plat] = len(files)
        for f in files:
            if f.stat().st_size == 0:
                report["empty_platform_files"].append(f"{plat}/{f.relative_to(PA)}")
        if plat == "goose":
            for f in pd2.glob("*.yaml"):
                try:
                    d = yaml.safe_load(f.read_text(encoding="utf-8"))
                    if not d or not d.get("title") or not d.get("description") or not d.get("instructions"):
                        report["recipe_parse_errors"].append(f"{plat}/{f.name}: missing title/description/instructions")
                    v = str(d.get("version", ""))
                    parts = v.split(".")
                    if len(parts) != 3 or not all(p.isdigit() for p in parts):
                        report["recipe_parse_errors"].append(f"{plat}/{f.name}: bad semver '{v}'")
                except Exception as e:
                    report["recipe_parse_errors"].append(f"{plat}/{f.name}: {e}")

    for plat in uc.SINGLE_FILE_PLATFORMS:
        pd2 = PA / plat / "instructions"
        files = [f for f in pd2.glob("*.md") if f.is_file()]
        report["platform_file_counts"][plat] = len(files)
        for f in files:
            if f.stat().st_size == 0:
                report["empty_platform_files"].append(f"{plat}/instructions/{f.name}")

    return report

if __name__ == "__main__":
    r = scan()
    print(json.dumps(r, indent=1, ensure_ascii=False))
