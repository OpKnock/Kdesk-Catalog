#!/usr/bin/env python3
"""Generate per-platform marketplace manifests from JSON definitions.

Every agent and skill definition converts to every platform (the converter
does not filter on `platforms`; that map holds per-platform config such as
tools and model). Each platform marketplace therefore lists the full catalog.
Entries are enriched with category accent/icon from divisions.json and
optional color/emoji from the definition. Output is deterministic: platforms
sorted, entries sorted by id, no timestamps. Workflows are platform-neutral
and are not listed.

Usage:
  python scripts/generate-marketplaces.py            # write marketplaces/ + report
  python scripts/generate-marketplaces.py --validate # check on-disk manifests
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACES = ROOT / "marketplaces"
REPORT = ROOT / "reports" / "marketplace-report.md"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def divisions_index():
    return load_json(ROOT / "divisions.json")["divisions"]


def tool_index():
    return load_json(ROOT / "tools.json")["tools"]


def iter_defs(kind):
    tree = ROOT / kind / "json"
    for p in sorted(tree.rglob("*.json")):
        doc = load_json(p)
        if not isinstance(doc, dict) or not doc.get("name"):
            continue
        rel = p.relative_to(tree).as_posix()
        doc["_category"] = rel.split("/")[0]
        yield doc


def build_entry(doc, divisions):
    accent = divisions.get(doc["_category"], {}).get("accent")
    icon = divisions.get(doc["_category"], {}).get("icon")
    entry = {
        "id": doc["name"],
        "name": doc["name"],
        "label": doc.get("display_name") or doc["name"],
        "description": (doc.get("description") or doc.get("display_name") or doc["name"]).strip(),
        "category": doc["_category"],
    }
    if accent:
        entry["accent"] = accent
    if icon:
        entry["icon"] = icon
    if doc.get("color"):
        entry["color"] = doc["color"]
    if doc.get("emoji"):
        entry["emoji"] = doc["emoji"]
    return entry


def build_marketplace(tool_key, tool, divisions):
    platforms = {"agents": 0, "skills": 0}
    entries = []
    for doc in iter_defs("agents"):
        entries.append(build_entry(doc, divisions))
        platforms["agents"] += 1
    for doc in iter_defs("skills"):
        entries.append(build_entry(doc, divisions))
        platforms["skills"] += 1
    entries.sort(key=lambda e: e["id"])
    return {
        "version": "1.0.0",
        "name": tool_key,
        "label": tool.get("label"),
        "format": tool.get("format"),
        "description": f"{tool.get('label')} agents and skills marketplace.",
        "entries": entries,
    }, platforms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true", help="check on-disk manifests")
    args = ap.parse_args()

    tools = tool_index()
    divisions = divisions_index()
    active = {k: v for k, v in sorted(tools.items()) if v.get("format") != "none"}

    errors = []
    totals = {"agents": 0, "skills": 0, "entries": 0}

    if args.validate:
        for key, tool in active.items():
            expected, counts = build_marketplace(key, tool, divisions)
            totals["agents"] += counts["agents"]
            totals["skills"] += counts["skills"]
            totals["entries"] += len(expected["entries"])
            path = MARKETPLACES / f"{key}.marketplace.json"
            want = json.dumps(expected, indent=2, ensure_ascii=False) + "\n"
            if not path.exists():
                errors.append(f"[missing] {path}")
                continue
            got = path.read_text(encoding="utf-8")
            if got != want:
                errors.append(f"[dirty] {path} differs from generated content")
        if errors:
            for line in errors:
                print(line, file=sys.stderr)
            print(f"[FAIL] {len(errors)} marketplace manifest(s) invalid", file=sys.stderr)
            sys.exit(2)
        print(f"[OK] {len(active)} marketplace manifests consistent ({totals['entries']} entries)")
        return

    MARKETPLACES.mkdir(exist_ok=True)
    rows = []
    for key, tool in active.items():
        manifest, counts = build_marketplace(key, tool, divisions)
        totals["agents"] += counts["agents"]
        totals["skills"] += counts["skills"]
        totals["entries"] += len(manifest["entries"])
        path = MARKETPLACES / f"{key}.marketplace.json"
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            f.write("\n")
        rows.append((key, tool.get("label"), counts["agents"], counts["skills"], len(manifest["entries"])))

    lines = [
        "# Marketplace Report",
        "",
        "Per-platform marketplaces generated from `agents/` and `skills/` JSON",
        "definitions. Each entry supports the platform via its `platforms` map.",
        "Workflows are platform-neutral and are not listed in marketplaces.",
        "",
        "| Platform | Label | Agents | Skills | Entries |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for key, label, agents, skills, entries in rows:
        lines.append(f"| {key} | {label} | {agents} | {skills} | {entries} |")
    lines.append(
        f"| **Total** | **{len(rows)} platforms** | **{totals['agents']}** | "
        f"**{totals['skills']}** | **{totals['entries']}** |"
    )
    lines += [
        "",
        f"Distinct divisions covered: {len(divisions)}.",
        "",
        f"Validate with: `python scripts/generate-marketplaces.py --validate`.",
        "",
    ]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"[OK] Wrote {len(rows)} marketplace manifests to {MARKETPLACES}")
    print(f"[OK] Wrote report to {REPORT}")


if __name__ == "__main__":
    main()