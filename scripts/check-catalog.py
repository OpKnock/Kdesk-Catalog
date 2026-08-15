#!/usr/bin/env python3
"""Check-catalog: validate divisions.json against the on-disk category trees.

Checks:
1. divisions.json keys == universal-agents/ top-level category dirs.
2. Root agents/, skills/, workflows/ JSON category trees are a subset of the
   division keys (every JSON definition's top-level folder must be a division).
   For agents/ and skills/, each definition must also carry a `category` field
   (a coarse grouping, not necessarily equal to the folder name).
3. Every division entry carries the required descriptor fields.

Exits 1 on any failure, 0 when the catalog is consistent.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIVISIONS_PATH = ROOT / "divisions.json"
UA = ROOT / "universal-agents"

TREES = (
    ("field", ROOT / "agents" / "json"),
    ("field", ROOT / "skills" / "json"),
    ("path", ROOT / "workflows"),
)

REQUIRED_FIELDS = ("name", "label", "accent", "icon", "order", "description")


def load_divisions(path=DIVISIONS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return manifest.get("divisions", {})


def check_divisions_against_dirs(divisions):
    errors = []
    ua_dirs = {p.name for p in UA.iterdir() if p.is_dir()}
    missing = sorted(ua_dirs - set(divisions))
    extra = sorted(set(divisions) - ua_dirs)
    if missing:
        errors.append(f"divisions.json missing universal-agents dirs: {', '.join(missing)}")
    if extra:
        errors.append(f"divisions.json has unknown categories: {', '.join(extra)}")
    return errors


def check_entry_fields(divisions):
    errors = []
    for key, entry in divisions.items():
        if entry.get("name") != key:
            errors.append(f"{key}: name != division key")
        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"{key}: missing field '{field}'")
    return errors


def check_json_trees(divisions, trees):
    errors = []
    files = 0
    categories = {}
    for mode, tree in trees:
        if not tree.is_dir():
            continue
        for p in sorted(tree.rglob("*.json")):
            files += 1
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
            except Exception:
                errors.append(f"{p.relative_to(ROOT)}: unreadable JSON")
                continue
            if mode == "path":
                parts = p.relative_to(tree).parts
                if len(parts) < 2:
                    errors.append(
                        f"{p.relative_to(ROOT)}: category not derivable from path"
                    )
                    continue
                category = parts[0]
            else:
                category = d.get("category")
                if not category:
                    errors.append(
                        f"{p.relative_to(ROOT)}: missing 'category' field"
                    )
                    continue
                parts = p.relative_to(tree).parts
                if len(parts) < 2:
                    errors.append(
                        f"{p.relative_to(ROOT)}: category not derivable from path"
                    )
                    continue
                category = parts[0]
            categories.setdefault(category, 0)
            categories[category] += 1
            if category not in divisions:
                errors.append(
                    f"{p.relative_to(ROOT)}: category '{category}' is not a division"
                )
    print(f"Scanned {files} JSON definitions across {len(categories)} categories")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Check divisions.json consistency")
    parser.add_argument("--divisions", default=str(DIVISIONS_PATH),
                        help="Path to divisions.json")
    args = parser.parse_args()

    divisions = load_divisions(Path(args.divisions))
    errors = []
    errors.extend(check_divisions_against_dirs(divisions))
    errors.extend(check_entry_fields(divisions))
    errors.extend(check_json_trees(divisions, TREES))

    if errors:
        print(f"Check-catalog found {len(errors)} problem(s):")
        for err in errors:
            print(f"  [ERR] {err}")
        sys.exit(1)
    print(f"[OK] divisions.json consistent with {len(divisions)} divisions")
    sys.exit(0)


if __name__ == "__main__":
    main()