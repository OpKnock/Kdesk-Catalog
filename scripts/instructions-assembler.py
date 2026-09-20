#!/usr/bin/env python3
"""
Instructions-only assembler.
Reads short_batch_*.json content files (rel_path -> new instructions string)
and replaces ONLY the `instructions` field in the corresponding universal
YAML files, preserving every other field exactly.
"""
import sys
import json
import yaml
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parents[1] / "universal-agents"
CONTENT_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__import__("tempfile").gettempdir()) / "short-content")

def main():
    content = {}
    for f in sorted(CONTENT_DIR.glob("short_batch_*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            content.update(data)
        except Exception as e:
            print(f"[ERR] content file {f}: {e}")
    print(f"Loaded {len(content)} content entries")

    updated = 0
    errors = 0
    for rel_path, new_instructions in content.items():
        target = AGENTS_DIR / rel_path
        if not target.exists():
            print(f"[ERR] target missing: {target}")
            errors += 1
            continue
        try:
            with open(target, "r", encoding="utf-8") as f:
                doc = yaml.safe_load(f)
            if not isinstance(doc, dict) or "instructions" not in doc:
                print(f"[ERR] no instructions field: {target}")
                errors += 1
                continue
            doc["instructions"] = new_instructions
            with open(target, "w", encoding="utf-8") as f:
                yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            updated += 1
        except Exception as e:
            print(f"[ERR] {rel_path}: {e}")
            errors += 1

    print(f"Updated {updated} files, {errors} errors")

if __name__ == "__main__":
    main()
