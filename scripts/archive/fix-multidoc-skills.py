#!/usr/bin/env python3
"""
Fix multi-document skill YAMLs (frontmatter + markdown body).
Merges into a single-doc YAML with instructions = markdown body,
and adds standard platform sections so the converter can process them.
"""
import os
import sys
import yaml
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parents[1] / "universal-agents"

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Split frontmatter and body
    parts = raw.split("\n---\n", 1)
    if len(parts) != 2:
        return "skip", "no separator"
    front, body = parts

    try:
        doc = yaml.safe_load(front)
    except Exception as e:
        return "error", str(e)

    if not isinstance(doc, dict):
        return "error", "frontmatter not a dict"

    doc["type"] = "skill"
    doc["instructions"] = body.strip()
    doc["examples"] = doc.get("examples", [])

    # Ensure display_name
    if "display_name" not in doc:
        doc["display_name"] = doc.get("name", "skill")

    # Standard platform sections (converter needs these)
    name = doc.get("name", "skill")
    doc["platforms"] = {
        "claude_code": {
            "tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"],
            "model": "claude-3-5-sonnet-20241022"
        },
        "cursor": {"rule_type": "auto", "model": "gpt-4"},
        "github_copilot": {"prompt_file": f"{name}.md", "extension": "github.copilot"},
        "windsurf": {"model": "claude-3.5-sonnet", "tools": ["bash", "read", "write", "edit"]},
        "opencode": {"plugin": f"opencode-{name}"},
        "generic": {
            "system_prompt": f"You are an expert in {name}.",
            "available_tools": ["bash", "read", "write", "edit", "glob", "grep"]
        }
    }

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return "ok", ""

def main():
    fixed, skipped, errors = 0, 0, 0
    for root, dirs, files in os.walk(AGENTS_DIR):
        for fn in files:
            if not fn.endswith(".yaml") or fn == "registry.yaml":
                continue
            path = os.path.join(root, fn)
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            if "\n---\n" not in raw:
                continue
            status, msg = fix_file(path)
            if status == "ok":
                fixed += 1
            elif status == "error":
                errors += 1
                print(f"[ERR] {os.path.relpath(path, AGENTS_DIR)}: {msg}")
            else:
                skipped += 1
    print(f"Fixed: {fixed}, skipped: {skipped}, errors: {errors}")

if __name__ == "__main__":
    main()
