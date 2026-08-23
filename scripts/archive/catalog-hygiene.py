#!/usr/bin/env python3
"""Catalog hygiene reports: near-duplicate skills and content-quality gaps.

Subcommands:
  dedup  Group skills by normalized name family (suffixes -v2.., -engineer,
         -specialist, -designer, -skill stripped) and report collisions that are
         likely duplicate entries; sorted by group size.
  gaps   Per-category counts of items lacking parameters / prerequisites /
         examples / knowledge, plus the missing-reference candidates for wiring.

Usage:
  python scripts/catalog-hygiene.py dedup --agents universal-agents [--top 15]
  python scripts/catalog-hygiene.py gaps  --agents universal-agents
"""
import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

NAME_SUFFIXES = re.compile(
    r"(?:-skill|-agent)?(?:-(?:v\d+|[a-z]{2,3}\d*|engineer|specialist|designer|architect|"
    r"expert|developer|builder|strategist|practitioner|auditor|optimizer|integrator|"
    r"configurator|scanner|validator|creator|manager|analyst|assistant|helper|runner|"
    r"tester))$")


def load(agents_dir):
    files = sorted(p for p in Path(agents_dir).rglob("*.yaml") if p.name != "registry.yaml")
    docs = []
    for f in files:
        rel = str(f.relative_to(agents_dir)).replace("\\", "/")
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception as e:
            d = {"_ERROR": str(e)}
        d["_rel"] = rel
        d["_skill"] = "/skill/" in rel or f.name.endswith("-skill.yaml")
        docs.append(d)
    return docs


def do_dedup(args):
    docs = [d for d in load(args.agents) if d["_skill"]]
    fam = defaultdict(list)
    for d in docs:
        name = str(d.get("name", "")).lower()
        core = NAME_SUFFIXES.sub("", name).rstrip("-") or name
        fam[core].append((d.get("name"), d["_rel"]))
    groups = sorted(((core, v) for core, v in fam.items() if len(v) > 1),
                    key=lambda kv: len(kv[1]), reverse=True)
    print(f"skills: {len(docs)} | duplicate-name families: {len(groups)}")
    for core, members in groups[: args.top]:
        print(f"\n  family '{core}' x{len(members)}")
        for name, rel in members:
            print(f"    - {name}  ({rel})")
    return


def do_gaps(args):
    docs = load(args.agents)
    per_cat = defaultdict(lambda: [0, 0, 0, 0, 0])  # total, no-params, no-prereq, no-examples, no-knowledge
    unwired_needs = []
    for d in docs:
        cat = str(d.get("category", "?"))
        row = per_cat[cat]
        row[0] += 1
        nparams = sum(len([p for p in (c.get("parameters") or []) if isinstance(p, dict) and p.get("name")])
                      for c in d.get("capabilities") or [])
        if not nparams:
            row[1] += 1
        if not isinstance(d.get("prerequisites"), list) and not isinstance(d.get("tools"), list):
            row[2] += 1
        if not (d.get("examples") or d.get("examples") == [] and False):
            row[3] += 1
        if not d.get("knowledge"):
            row[4] += 1
        if d["_skill"] and not d.get("tools") and not d.get("prerequisites"):
            unwired_needs.append((d.get("name"), cat, d["_rel"]))
    total = [0, 0, 0, 0, 0]
    print(f"{'category':<14} {'total':>6} {'no-params':>9} {'no-prereq/tools':>15} {'no-examples':>11} {'no-knowledge':>12}")
    for cat, row in sorted(per_cat.items(), key=lambda kv: -kv[1][0]):
        for i in range(5):
            total[i] += row[i]
        print(f"{cat:<14} {row[0]:>6} {row[1]:>9} {row[2]:>15} {row[3]:>11} {row[4]:>12}")
    print(f"{'TOTAL':<14} {total[0]:>6} {total[1]:>9} {total[2]:>15} {total[3]:>11} {total[4]:>12}")
    print(f"\nskills declaring neither tools nor prerequisites (conceptual skills; wireable "
          f"only if a distinct CLI binary exists in their commands): {len(unwired_needs)}")
    for name, cat, rel in unwired_needs[: args.top]:
        print(f"    - {name}  ({cat} / {rel})")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("dedup", do_dedup), ("gaps", do_gaps)):
        p = sub.add_parser(name)
        p.add_argument("--agents", default=str(ROOT / "universal-agents"))
        p.add_argument("--top", type=int, default=15)
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()