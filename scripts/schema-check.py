#!/usr/bin/env python3
"""Validate every universal-agents/ YAML against schemas/universal-agent.schema.json.

Usage: python scripts/schema-check.py [--agents universal-agents] [--schema schemas/universal-agent.schema.json]
Exits 1 when the first N (default 20) violations appear; prints a full count summary.
"""
import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agents", default=str(ROOT / "universal-agents"))
    ap.add_argument("--schema", default=str(ROOT / "schemas" / "universal-agent.schema.json"))
    ap.add_argument("--show", type=int, default=20, help="max violations to print")
    args = ap.parse_args()

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    files = sorted(p for p in Path(args.agents).rglob("*.yaml") if p.name != "registry.yaml")

    total = errors = 0
    shown = 0
    for f in files:
        total += 1
        rel = str(f.relative_to(args.agents)).replace("\\", "/")
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception as e:
            errors += 1
            if shown < args.show:
                print(f"  {rel}: YAML parse error: {e}")
                shown += 1
            continue
        for err in validator.iter_errors(doc):
            errors += 1
            if shown < args.show:
                print(f"  {rel}: {' / '.join(str(p) for p in err.path)}: {err.message}")
                shown += 1

    print(f"schema: {args.schema}")
    print(f"files: {total} | violations: {errors}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()