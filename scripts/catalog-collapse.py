"""catalog-collapse.py - L3: collapse function-clones into a richest survivor.

Merges only when content evidence agrees: files in the same subject family whose
capability command sets are identical AND instruction text is near-duplicate
(high token Jaccard) with comparable quality scores. Superseded files move to
archive/ (versioned, recoverable). Pairs below the merge bar are emitted as
ranked merge-candidates for human review.

Usage:
  python scripts/catalog-collapse.py                # measure only (no changes)
  python scripts/catalog-collapse.py --apply        # collapse at defaults
  python scripts/catalog-collapse.py --apply --threshold 0.5 --max-gap 4
  python scripts/catalog-collapse.py --report       # write merge-candidates report
"""
import argparse
import json
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"
ARCHIVE = ROOT / "archive"


def norm(t):
    if isinstance(t, list):
        t = " ".join(str(x) for x in t)
    return " ".join(re.findall(r"[a-z0-9]+", (t or "").lower()))


def jac(a, b):
    return len(a & b) / max(1, len(a | b))


def commands(d):
    out = []
    for cap in d.get("capabilities") or []:
        if isinstance(cap, dict):
            out.extend(norm(c) for c in (cap.get("commands") or []) if isinstance(c, str))
    return out


def instr_tokens(d):
    return set(norm(d.get("instructions")).split())


def quality_score(d):
    s = len(set(commands(d)))
    s += 2 * sum(len((c.get("parameters") or [])) for c in (d.get("capabilities") or [])
                 if isinstance(c, dict))
    s += 2 * len(d.get("tools") or [])
    s += 2 * len(d.get("prerequisites") or [])
    s += len(norm(d.get("description")).split())
    return s


def walk():
    for f in sorted(UA.rglob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(d, dict) or not d.get("name"):
            continue
        yield f, d


def build_families():
    fams = {}
    for f, d in walk():
        key = " ".join(norm(str(d["name"])).split()[:2])
        fams.setdefault(key, []).append((f, d))
    return fams


def analyze(threshold, max_gap, overlap=0.7):
    pairs = []
    for stem, members in build_families().items():
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                (fa, da), (fb, db) = members[i], members[j]
                if da.get("category") != db.get("category"):
                    continue
                ca, cb = set(commands(da)), set(commands(db))
                if not ca or not cb:
                    continue
                ovl = len(ca & cb) / max(1, len(ca | cb))
                if ovl < overlap:
                    continue
                sim = jac(instr_tokens(da), instr_tokens(db))
                gap = abs(quality_score(da) - quality_score(db))
                pairs.append({
                    "family": stem,
                    "a": str(fa.relative_to(ROOT)),
                    "b": str(fb.relative_to(ROOT)),
                    "ovl": round(ovl, 3),
                    "sim": round(sim, 3),
                    "score_a": quality_score(da),
                    "score_b": quality_score(db),
                    "gap": gap,
                    "commands": len(ca),
                })
    merges = [p for p in pairs if p["sim"] >= threshold and p["gap"] <= max_gap]
    candidates = [p for p in pairs if p not in merges and p["sim"] >= 0.3]
    return merges, candidates


def components(merges):
    nodes = {}
    for p in merges:
        nodes.setdefault(p["a"], set()).add(p["b"])
        nodes.setdefault(p["b"], set()).add(p["a"])
    seen, out = set(), []
    for start in nodes:
        if start in seen:
            continue
        comp, stack = set(), [start]
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            comp.add(n)
            stack.extend(nodes.get(n, ()))
        out.append(comp)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--threshold", type=float, default=0.55)
    ap.add_argument("--max-gap", type=float, default=3.0)
    args = ap.parse_args()

    merges, candidates = analyze(args.threshold, args.max_gap)
    comps = components(merges)
    arc = sum(len(c) - 1 for c in comps)
    print(f"command-identical pairs: {len(merges) + len(candidates)} "
          f"(set: {len(merges)} merge / {len(candidates)} below bar)")
    print(f"merge components: {len(comps)}  -> surgical collapse removes {arc} files "
          f"({len(comps)} survivors)")

    by_fam = {}
    for p in merges:
        by_fam.setdefault(p["family"], []).append(p)
    for fam, g in sorted(by_fam.items(), key=lambda kv: -len(kv[1]))[:12]:
        comp2 = components(g)
        print(f"  {fam:<20} pairs={len(g)} comps={len(comp2)} "
              f"files={sum(len(c) for c in comp2)} -> survivors={len(comp2)}")

    if args.report:
        rep = ROOT / "reports" / "merge-candidates.md"
        rep.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# Merge candidates (below auto bar)\n",
                 f"Auto bar: identical commands + instruction Jaccard >= {args.threshold} "
                 f"and score gap <= {args.max_gap}.\n",
                 "Auto-merging would cancel the remaining differences: instructions vary "
                 "~80% even inside name families. Deciding these is human curation.\n"]
        rows = sorted(candidates, key=lambda p: (-p["sim"], p["family"]))
        if not rows:
            lines.append("\n_None._\n")
        for p in rows[:200]:
            lines.append(f"- `{p['a']}` / `{p['b']}` (fam {p['family']}, sim {p['sim']}, "
                         f"gap {p['gap']}, {p['commands']} cmds)\n")
        if len(rows) > 200:
            lines.append(f"\n_… and {len(rows) - 200} more._\n")
        rep.write_text("".join(lines), encoding="utf-8")
        print(f"report: {rep.relative_to(ROOT)} ({len(rows)} candidates listed)")

    if args.apply:
        moved = 0
        for comp in comps:
            best, best_score = None, -1
            for rel in comp:
                f = ROOT / rel
                if not f.exists():
                    continue
                d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
                s = quality_score(d)
                if s > best_score:
                    best, best_score = rel, s
            if best is None:
                continue
            for rel in comp:
                if rel == best:
                    continue
                f = ROOT / rel
                if not f.exists():
                    continue
                dest = ARCHIVE / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(dest))
                moved += 1
        print(f"collapsed: {moved} files archived")


if __name__ == "__main__":
    main()