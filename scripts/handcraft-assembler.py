#!/usr/bin/env python3
"""
Hand-crafted content assembler.
Reads content JSON files (one per skill) and merges them into the
corresponding universal YAML files, preserving platform sections.
"""
import os
import sys
import json
import yaml
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parents[1] / "universal-agents"
CONTENT_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__import__("tempfile").gettempdir()) / "skill-content")

def load_content_files():
    content = {}
    for f in CONTENT_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            content.update(data)
        except Exception as e:
            print(f"[ERR] content file {f}: {e}")
    return content

def main():
    content = load_content_files()
    print(f"Loaded {len(content)} content entries")

    updated = 0
    errors = 0
    for rel_path, entry in content.items():
        target = AGENTS_DIR / rel_path
        if not target.exists():
            print(f"[ERR] target missing: {target}")
            errors += 1
            continue
        try:
            with open(target, "r", encoding="utf-8") as f:
                doc = yaml.safe_load(f)

            # Replace hand-crafted fields, preserve everything else
            for key in ("description", "capabilities", "knowledge", "instructions", "examples"):
                if key in entry and entry[key] is not None:
                    doc[key] = entry[key]
            doc["version"] = "2.0.0"

            with open(target, "w", encoding="utf-8") as f:
                yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            updated += 1
        except Exception as e:
            print(f"[ERR] {rel_path}: {e}")
            errors += 1

    print(f"Updated {updated} files, {errors} errors")

if __name__ == "__main__":
    main()
