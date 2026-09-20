#!/usr/bin/env python3
"""
Full verification of universal agents directory.

1. Discover repository root dynamically (no hard-coded paths).
2. Locate universal-agents safely; refuse to proceed if missing.
3. All YAML files parse (single doc).
4. Zero template shells remain (every file has real commands).
5. Unique content check (no duplicate command sets).
6. All required fields present.
7. FATAL + non-zero exit on zero-file scans - verification NEVER succeeds
   on zero work.
"""
import os
import sys
import yaml
import re
import json
from pathlib import Path
from collections import Counter

# ------------------------------------------------------------------ root
def find_root() -> Path:
    """Discover the repository root from this file's location."""
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "universal-agents").is_dir():
        return candidate
    # walk upward for a tree containing universal-agents
    for parent in Path(__file__).resolve().parents:
        if (parent / "universal-agents").is_dir():
            return parent
    raise SystemExit("FATAL: could not locate universal-agents directory from %s" % __file__)


ROOT = find_root()
AGENTS_DIR = ROOT / "universal-agents"


def classify(path, content):
    m = re.search(r"^type:\s*(agent|skill)", content, re.M)
    if m:
        return m.group(1)
    if path.name.endswith("-skill.yaml"):
        return "skill"
    return "agent"


def check_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    errors = []
    try:
        doc = yaml.safe_load(content)
    except Exception as e:
        return ["YAML PARSE ERROR: %s" % e]

    if not isinstance(doc, dict):
        return ["NOT A DICT"]

    for field in ["name", "description", "version"]:
        if field not in doc:
            errors.append("missing field: %s" % field)

    # Hand-crafted check: real commands
    caps = doc.get("capabilities", [])
    has_commands = False
    cmd_count = 0
    for cap in caps:
        cmds = cap.get("commands", []) if isinstance(cap, dict) else []
        if cmds:
            has_commands = True
            cmd_count += len(cmds)

    if not has_commands:
        errors.append("NO REAL COMMANDS (template shell)")

    # Instructions length
    instructions = doc.get("instructions", "")
    if len(str(instructions)) < 200:
        errors.append("instructions too short (%d chars)" % len(str(instructions)))

    # Examples present
    if not doc.get("examples") and not any(
        (c.get("examples") if isinstance(c, dict) else None) for c in caps
    ):
        errors.append("no examples")

    return errors


def main():
    if not AGENTS_DIR.is_dir():
        print("FATAL: universal-agents directory not found: %s" % AGENTS_DIR)
        return 2

    total = 0
    agents = 0
    skills = 0
    error_files = []
    cmd_sets = Counter()

    for path in sorted(AGENTS_DIR.rglob("*.yaml")):
        if path.name == "registry.yaml":
            continue
        total += 1
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        t = classify(path, content)
        if t == "agent":
            agents += 1
        else:
            skills += 1

        errs = check_file(path)
        if errs:
            error_files.append((str(path.relative_to(AGENTS_DIR)), errs))

        # collect command sets for uniqueness check
        try:
            doc = yaml.safe_load(content)
            for cap in doc.get("capabilities", []):
                if isinstance(cap, dict):
                    cmds = tuple(cap.get("commands", []))
                    if cmds:
                        cmd_sets[cmds] += 1
        except Exception:
            pass

    if total == 0:
        print("FATAL:")
        print("0 definitions scanned.")
        print("Verification aborted.")
        return 2

    print("=" * 50)
    print("TOTAL YAML FILES: %d (agents=%d, skills=%d)" % (total, agents, skills))
    print("FILES WITH ERRORS: %d" % len(error_files))
    for path, errs in error_files[:20]:
        print("  [ERR] %s" % path)
        for e in errs[:3]:
            print("        - %s" % e)
    if len(error_files) > 20:
        print("  ... and %d more" % (len(error_files) - 20))

    dups = {k: v for k, v in cmd_sets.items() if v > 1}
    print("DUPLICATE COMMAND SETS: %d" % len(dups))
    for k, v in list(dups.items())[:5]:
        print("  [DUP x%d] %s" % (v, k[0][:60] if k else "empty"))

    return 0 if not error_files else 1


if __name__ == "__main__":
    sys.exit(main())