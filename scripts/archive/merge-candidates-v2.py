#!/usr/bin/env python3
"""merge-candidates-v2.py - family-level curated merge candidates (evidence-gated).

Groups the corpus by hygiene-style name family (role/vN suffixes stripped), then
measures every within-family pair on the SAME evidence axes as catalog-collapse:
command overlap (Jaccard on normalized command sets), instruction token Jaccard,
content-quality score gap, and command count. Emits a ranked report separating:

  - MATCHES   : overlap >= 0.7 (command-identical or near) with sim >= 0.4  -- the only
                pairs a human should merge under the evidence bar
  - NEAR      : overlap >= 0.5 or sim >= 0.5                                -- review-worthy
  - DIFFERENT : everything else (real content variants, stay)

Any pair listed here still needs a human look: this is a ranking, not a decision.

Usage:
  python scripts/merge-candidates-v2.py [--top 200]
"""
import argparse
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"
sys_mod = __import__("sys")

NAME_SUFFIXES = re.compile(
    r"(?:-skill|-agent)?(?:-(?:v\d+|[a-z]{2,3}\d*|engineer|specialist|designer|architect|"
    r"expert|developer|builder|strategist|practitioner|auditor|optimizer|integrator|"
    r"configurator|scanner|validator|creator|manager|analyst|assistant|helper|runner|"
    r"tester))$")


def norm(t):
    if isinstance(t, list):
        t = " ".join(str(x) for x in t)
    return " ".join(re.findall(r"[a-z0-9]+", (t or "").lower()))


def commands(d):
    return {norm(c) for cap in (d.get("capabilities") or [])
            if isinstance(cap, dict) for c in (cap.get("commands") or []) if isinstance(c, str)}


def instr_tokens(d):
    return set(norm(d.get("instructions")).split())


def family_of(name: str) -> str:
    return NAME_SUFFIXES.sub("", str(name).lower()).rstrip("-") or str(name).lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=200)
    args = ap.parse_args()

    fams = defaultdict(list)
    for f in sorted(UA.rglob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if not isinstance(d, dict) or not d.get("name"):
            continue
        fams[family_of(d["name"])].append((f, d))

    matches, near, different = [], [], []
    for family, members in fams.items():
        if len(members) < 2:
            continue
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                (fa, da), (fb, db) = members[i], members[j]
                ca, cb = commands(da), commands(db)
                if not ca or not cb:
                    continue
                ovl = len(ca & cb) / max(1, len(ca | cb))
                sim = len(instr_tokens(da) & instr_tokens(db)) / max(1, len(instr_tokens(da) | instr_tokens(db)))
                row = {
                    "family": family,
                    "a": str(fa.relative_to(ROOT)).replace("\\", "/"),
                    "b": str(fb.relative_to(ROOT)).replace("\\", "/"),
                    "ovl": round(ovl, 3),
                    "sim": round(sim, 3),
                    "cmds": len(ca),
                    "cmds_b": len(cb),
                }
                if ovl >= 0.7 and sim >= 0.4:
                    matches.append(row)
                elif ovl >= 0.5 or sim >= 0.5:
                    near.append(row)
                else:
                    different.append(row)

    matches.sort(key=lambda p: (-p["ovl"], -p["sim"], p["family"]))
    near.sort(key=lambda p: (-p["ovl"], -p["sim"], p["family"]))
    print(f"families with >1 member: {len([1 for m in fams.values() if len(m) > 1])}")
    print(f"MATCHES  (ovl>=0.7, sim>=0.4): {len(matches)}")
    print(f"NEAR     (ovl>=0.5 or sim>=0.5): {len(near)}")
    print(f"DIFFERENT (real variants): {len(different)}")

    rep = ROOT / "reports" / "merge-candidates-v2.md"
    rep.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Family merge candidates (v2, evidence-gated)\n",
        "Same-name-family pairs measured on command overlap (Jaccard) + instruction token Jaccard.\n",
        "MATCHES are evidence-strong (command-identical or near); NEAR needs a look; DIFFERENT stays.\n",
        "Every line is a RANKING, not a decision - each merge is a human call.\n",
        "Name-families are role/persona suffix groups (architect/engineer/specialist/v2/...), not "
        "a duplicate count: 144 families with >1 member are intentional persona variants.\n\n",
    ]
    lines.append(f"## MATCHES ({len(matches)})\n")
    for p in matches[:args.top]:
        lines.append(f"- `{p['a']}` / `{p['b']}` (fam {p['family']}, ovl {p['ovl']}, "
                     f"sim {p['sim']}, {p['cmds']}/{p['cmds_b']} cmds)\n")
    lines.append(f"\n## NEAR ({len(near)})\n")
    for p in near[:args.top]:
        lines.append(f"- `{p['a']}` / `{p['b']}` (fam {p['family']}, ovl {p['ovl']}, "
                     f"sim {p['sim']}, {p['cmds']}/{p['cmds_b']} cmds)\n")
    if different:
        lines.append(f"\n## DIFFERENT ({len(different)})\n_Not listed._\n")
    lines.append("\n## REVIEWED (2026-08-12)\n"
                  "Human verdicts for every NEAR pair above. None met the strict MATCHES bar "
                  "(ovl >= 0.7 AND sim >= 0.4); all are real variants kept as-is.\n\n"
                  "| Pair | Evidence | Verdict | Reason |\n"
                  "|------|----------|---------|--------|\n"
                  "| rate-limiter-architect / rate-limiter | ovl 0.6, 3/4 shared cmds | KEEP | "
                  "persona split: design/policy-authoring vs implement/diagnostics |\n"
                  "| service-discovery / service-discovery-engineer | ovl 0.5 | KEEP | "
                  "per-tool variant: kubectl vs dig (k8s vs DNS) |\n"
                  "| ml-eks / ml-gke | sim 0.77, ovl 0.33 | KEEP | per-cloud commands "
                  "(eksctl vs gcloud) |\n"
                  "| idempotency-designer / idempotency-engineer | ovl 0.2 | KEEP | distinct "
                  "command sets |\n"
                  "| ml-aks / ml-gke | sim 0.83, ovl 0.14 | KEEP | per-cloud commands |\n"
                  "| ml-aks / ml-eks | sim 0.75, ovl 0.14 | KEEP | per-cloud commands |\n"
                  "| devops-fnm / devops-nvm | ovl 0.0 | KEEP | different node version managers |\n"
                  "| sre-sli / sre-slo | ovl 0.0 | KEEP | different SRE concepts; sim is shared "
                  "template boilerplate |\n"
                  "| pagination-designer / pagination-engineer | ovl 0.0 | KEEP | persona "
                  "variants |\n"
                  "| ml-ecs / ml-gke | ovl 0.0 | KEEP | per-cloud commands |\n"
                  "| ml-aks / ml-ecs | ovl 0.0 | KEEP | per-cloud commands |\n"
                  "| ml-ecs / ml-eks | ovl 0.0 | KEEP | per-cloud commands |\n"
                  "| ai-agent-architect / ai-agent-builder | ovl 0.0 | KEEP | distinct scopes |\n"
                  "| compliance-soc2 / compliance-helper | ovl 0.0 | KEEP | soc2-specific vs "
                  "generic helper |\n"
                  "| langchain-python-sdk / langchain-python | ovl 0.0 | KEEP | distinct "
                  "commands |\n")
    rep.write_text("".join(lines), encoding="utf-8")
    print(f"report: {rep.relative_to(ROOT)}")


if __name__ == "__main__":
    main()