#!/usr/bin/env python3
"""Kdesk-Catalog: curation tier classifier.

Scans every universal-agents YAML definition and classifies it into one of
three tiers using template fingerprints:

  curated  - no template fingerprints found; content is genuine expert
             material (real commands, real knowledge links, unique text)
  template - one or more template fingerprints detected (see FINGERPRINTS)
  unknown  - file could not be parsed as YAML

Outputs:
  reports/curation-status.json  - machine-readable per-file tier data
  reports/CURATION-STATUS.md    - human-readable summary (trust layer)

Usage:
  python scripts/curate-tier.py [--source universal-agents] [--quiet]
"""

import argparse
import collections
import glob
import json
import os
import sys
from datetime import date

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML is required: pip install PyYAML", file=sys.stderr)
    sys.exit(2)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SOURCE = os.path.join(REPO, "universal-agents")

FINGERPRINTS = {
    "kdesk_agents_link": {
        "test": lambda txt, doc: "kdesk/agents" in txt,
        "label": "fake knowledge link (kdesk/agents -> 404)",
    },
    "identity_py": {
        "test": lambda txt, doc: "identity.py" in txt,
        "label": "fake identity.py command",
    },
    "registry_example": {
        "test": lambda txt, doc: "registry.example.com" in txt,
        "label": "placeholder registry.example.com",
    },
    "frozen_timestamp": {
        "test": lambda txt, doc: "created_at: '2024-01-01" in txt
        or "created_at: 2024-01-01" in txt,
        "label": "frozen 2024-01-01 created_at",
    },
    "template_author": {
        "test": lambda txt, doc: doc.get("author") == "Kdesk-Catalog",
        "label": "template author Kdesk-Catalog",
    },
    "generic_description": {
        "test": lambda txt, doc: bool(
            doc.get("name")
            and doc.get("name").replace("-", " ").lower()
            in str(doc.get("description", "")).lower()
            and " for " in str(doc.get("description", ""))
        ),
        "label": "description repeats the name (auto-generated)",
    },
    "placeholder_command": {
        "test": lambda txt, doc: any(
            "<" in str(cmd) or "example.com" in str(cmd) or "TODO" in str(cmd).upper()
            for cap in (doc.get("capabilities") or [])
            if isinstance(cap, dict)
            for cmd in (cap.get("commands") or [])
        ),
        "label": "placeholder command (<>/example.com/TODO)",
    },
}


def classify(txt, doc):
    """Return (tier, [fingerprint keys]) for one parsed YAML document."""
    found = []
    for key, fp in FINGERPRINTS.items():
        try:
            if fp["test"](txt, doc):
                found.append(key)
        except Exception:
            continue
    if found:
        return "template", found
    return "curated", []


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=DEFAULT_SOURCE, help="source YAML dir")
    ap.add_argument("--quiet", action="store_true", help="no per-file output")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.source, "**", "*.yaml"), recursive=True))
    if not files:
        print("no YAML files found under %s" % args.source, file=sys.stderr)
        sys.exit(1)

    per_file = {}
    tier_counts = collections.Counter()
    fp_counts = collections.Counter()
    per_category = collections.defaultdict(collections.Counter)

    for f in files:
        rel = os.path.relpath(f, args.source).replace("\\", "/")
        try:
            txt = open(f, encoding="utf-8").read()
            doc = yaml.safe_load(txt) or {}
        except Exception as exc:
            per_file[rel] = {"tier": "unknown", "fingerprints": [], "error": str(exc)}
            tier_counts["unknown"] += 1
            per_category[doc.get("category", "?") if isinstance(doc, dict) else "?"]["unknown"] += 1
            continue
        if not isinstance(doc, dict):
            per_file[rel] = {"tier": "unknown", "fingerprints": [], "error": "not a mapping"}
            tier_counts["unknown"] += 1
            per_category["?"]["unknown"] += 1
            continue
        tier, found = classify(txt, doc)
        per_file[rel] = {
            "tier": tier,
            "fingerprints": found,
            "name": doc.get("name"),
            "category": doc.get("category"),
            "type": doc.get("type") or ("skill" if "/skill/" in "/" + rel else "agent"),
        }
        tier_counts[tier] += 1
        per_category[doc.get("category", "?")][tier] += 1
        for k in found:
            fp_counts[k] += 1
        if not args.quiet:
            print("%-8s %s%s" % (tier, rel, (" [%s]" % ",".join(found)) if found else ""))

    status = {
        "generated": date.today().isoformat(),
        "tiers": dict(tier_counts),
        "fingerprints": dict(fp_counts),
        "categories": {k: dict(v) for k, v in sorted(per_category.items())},
        "files": per_file,
    }

    out_dir = os.path.join(REPO, "reports")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "curation-status.json"), "w", encoding="utf-8") as fh:
        json.dump(status, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    total = sum(tier_counts.values())
    curated = tier_counts["curated"]
    template = tier_counts["template"]
    pct = (100.0 * curated / total) if total else 0.0

    lines = [
        "# Curation Status",
        "",
        "Machine-readable report: `reports/curation-status.json` "
        "(regenerate with `python scripts/curate-tier.py`).",
        "",
        "| Tier | Count | Share |",
        "|---|---|---|",
        "| curated | %d | %.1f%% |" % (curated, pct),
        "| template | %d | %.1f%% |" % (template, (100.0 * template / total) if total else 0.0),
        "| unknown | %d | %.1f%% |" % (tier_counts["unknown"], (100.0 * tier_counts["unknown"] / total) if total else 0.0),
        "| **total** | **%d** | **100%%** |" % total,
        "",
        "## Template fingerprints found",
        "",
        "| Fingerprint | Files |",
        "|---|---|",
    ]
    for k, n in fp_counts.most_common():
        lines.append("| %s (%s) | %d |" % (FINGERPRINTS[k]["label"], k, n))
    lines += ["", "## Worst categories (most template-tier files)", ""]
    lines.append("| Category | curated | template |")
    lines.append("|---|---|---|")
    for cat, counts in sorted(per_category.items(), key=lambda kv: -kv[1]["template"]):
        if counts["template"] > 0:
            lines.append("| %s | %d | %d |" % (cat, counts["curated"], counts["template"]))

    with open(os.path.join(out_dir, "CURATION-STATUS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    if not args.quiet:
        print("\ncurated=%d template=%d unknown=%d" % (curated, template, tier_counts["unknown"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())