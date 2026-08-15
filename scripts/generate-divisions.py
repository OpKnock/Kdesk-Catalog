#!/usr/bin/env python3
"""Generate divisions.json from the universal-agents/ top-level category dirs.

Output is deterministic: categories sorted by name, order assigned 1..N.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"
OUT = ROOT / "divisions.json"

ACRONYMS = {
    "ai", "api", "ci", "ddos", "finops", "grpc", "idempotency", "iot",
    "kv", "ml", "oauth2", "sla", "slo", "sre", "waf",
}

ACCENTS = [
    "#0EA5E9", "#10B981", "#F59E0B", "#EF4444", "#14B8A6", "#8B5CF6",
    "#EC4899", "#F97316", "#06B6D4", "#6366F1", "#84CC16", "#A855F7",
]

ICONS = [
    "code-xml", "sparkles", "rocket", "bot", "pen-tool", "puzzle",
    "layers", "gauge", "zap", "cloud", "database", "shield",
]


def humanize(name):
    parts = name.split("-")
    words = []
    for part in parts:
        if part in ACRONYMS:
            words.append(part.upper())
        elif part == "and":
            words.append("and")
        else:
            words.append(part.capitalize())
    return " ".join(words)


def main():
    categories = sorted(p.name for p in UA.iterdir() if p.is_dir())
    divisions = {}
    for i, name in enumerate(categories, start=1):
        label = humanize(name)
        divisions[name] = {
            "name": name,
            "label": label,
            "accent": ACCENTS[(i - 1) % len(ACCENTS)],
            "icon": ICONS[(i - 1) % len(ICONS)],
            "order": i,
            "description": f"{label} agents, skills, and workflows.",
        }
    manifest = {"version": "1.0.0", "divisions": divisions}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"[OK] Wrote {len(divisions)} divisions to {OUT}")


if __name__ == "__main__":
    main()