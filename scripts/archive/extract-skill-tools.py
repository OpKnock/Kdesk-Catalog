#!/usr/bin/env python3
"""extract-skill-tools.py - derive `prerequisites` for skills that declare none.

Content-derived and invariant: the tools a skill really uses are the command
binaries in its own `commands` (first word per line, labels and noise excluded,
identical to wire-skills' agent tokenizer). Files that already declare `tools`
or `prerequisites` are never touched, so the script is idempotent and safe to
re-run after curation.

Usage:
  python scripts/extract-skill-tools.py            # preview (no writes)
  python scripts/extract-skill-tools.py --apply    # write prerequisites: [...] into skills
"""
import argparse
import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"

spec = importlib.util.spec_from_file_location("wire_skills", ROOT / "scripts" / "wire-skills.py")
wire_skills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wire_skills)
agent_command_tokens = wire_skills.agent_command_tokens  # reuse wire's tokenizer


def is_skill(rel: str) -> bool:
    return "/skill/" in rel or rel.endswith("-skill.yaml")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    updated = skipped = empty = 0
    samples = []
    for f in sorted(UA.rglob("*.yaml")):
        rel = str(f.relative_to(UA)).replace("\\", "/")
        if not is_skill(rel):
            continue
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or not doc.get("name"):
            continue
        if doc.get("tools") or doc.get("prerequisites"):
            skipped += 1
            continue
        tokens = sorted(agent_command_tokens(doc))
        if not tokens:
            empty += 1
            continue
        updated += 1
        if not args.apply:
            if len(samples) < 12:
                samples.append((doc["name"], tokens[:6]))
            continue
        blob = f.read_text(encoding="utf-8")
        ins = "\n".join(f"- {t}" for t in tokens)
        if "capabilities:\n" in blob:
            blob = blob.replace("capabilities:\n", "prerequisites:\n" + ins + "\n\ncapabilities:\n", 1)
        else:
            blob = blob.rstrip() + "\nprerequisites:\n" + ins + "\n"
        f.write_text(blob, encoding="utf-8")

    print(f"skills skipped (already declare tools/prerequisites): {skipped}")
    print(f"skills with no command evidence (stay unwired): {empty}")
    print(f"skills to update: {updated}")
    for name, toks in samples:
        print(f"  {name:<34} -> {toks}")
    if args.apply:
        print("applied.")


if __name__ == "__main__":
    main()