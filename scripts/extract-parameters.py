#!/usr/bin/env python3
"""extract-parameters.py - promote real CLI flags from commands into capability parameters.

Content-derived and invariant: a flag is promoted only when it is demonstrably
used by the capability's own commands (evidence = distinct commands containing
the flag) and the capability currently declares an empty `parameters` list.

Evidence rules (no invention):
  - long flags `--name`:  >= 2 distinct commands
  - short flags `-x` (single letter): >= 4 distinct commands
  - universal noise excluded: --help, --version
  - the generator artifact command (`python identity.py ... --agent <id>`) is
    skipped entirely; --agent is therefore never extracted
  - type inferred from the token following the flag on its first occurrence:
    none/next-flag -> boolean; all digits -> number; else string
  - description is factual: "CLI flag --<name> observed in capability commands"

Files whose existing parameters are non-empty are never touched (idempotent).
Top-level `parameters: []` (whole-skill) declarations are not modified; only
per-capability `parameters: []` entries are filled, and only when they exactly
outnumber capabilities (safety check: 1:1 lines, otherwise the file is skipped).

Usage:
  python scripts/extract-parameters.py            # preview (no writes)
  python scripts/extract-parameters.py --apply    # fill capability parameters
"""
import argparse
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"

LONG_RE = re.compile(r"--([a-z][a-z0-9-]*)")
SHORT_RE = re.compile(r"-\s*([a-z])\b")
NOISE = {"help", "version", "agent"}
CAP_PARAMS_LINE = re.compile(r"^\s+parameters: \[\]\s*$")


def flag_evidence(cmds):
    """Return {flag: count} across distinct commands, artifact lines excluded."""
    long_count = Counter()
    short_count = Counter()
    for cmd in cmds:
        if not isinstance(cmd, str) or not cmd.strip():
            continue
        if "identity.py" in cmd:
            continue
        for m in LONG_RE.finditer(cmd):
            f = "--" + m.group(1)
            if m.group(1) not in NOISE:
                long_count[f] += 1
        for m in SHORT_RE.finditer(cmd):
            f = "-" + m.group(1)
            if m.group(1) not in NOISE:
                short_count[f] += 1
    return long_count, short_count


def infer_type(cmd, flag):
    tokens = cmd.split()
    for i, t in enumerate(tokens):
        if t.startswith(flag):
            nxt = tokens[i + 1] if i + 1 < len(tokens) else None
            if nxt is None or nxt.startswith("-"):
                return "boolean"
            if nxt.isdigit():
                return "number"
            return "string"
    return "string"


def build_parameters(cmds):
    long_count, short_count = flag_evidence(cmds)
    keep = {}
    for f, c in long_count.items():
        if c >= 2:
            keep[f] = c
    for f, c in short_count.items():
        if c >= 4:
            keep[f] = c
    if not keep:
        return None
    params = []
    for f, c in sorted(keep.items()):
        name = f.lstrip("-")
        t = "string"
        for cmd in cmds:
            if isinstance(cmd, str) and f in cmd:
                t = infer_type(cmd, f)
                break
        params.append({
            "name": name,
            "type": t,
            "description": f"CLI flag --{name} observed in capability commands",
        })
    return params


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    updated = skipped = unchanged = 0
    samples = []
    for f in sorted(UA.rglob("*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or not doc.get("capabilities"):
            continue
        caps = doc["capabilities"]
        plan = []
        for cap in caps:
            if cap.get("parameters") or not cap.get("commands"):
                continue
            params = build_parameters(cap.get("commands") or [])
            if params:
                plan.append((cap, params))
        if not plan:
            unchanged += 1
            continue
        lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
        empty_lines = [i for i, ln in enumerate(lines) if CAP_PARAMS_LINE.match(ln)]
        if len(empty_lines) != len(caps):
            skipped += 1
            print(f"  SKIP {f.name}: {len(empty_lines)} parameters:[] lines vs {len(caps)} capabilities")
            continue
        if not args.apply:
            for cap, params in plan[:4]:
                if len(samples) < 10:
                    samples.append((f.name, cap.get("name"), [p["name"] for p in params[:6]]))
            updated += 1
            continue
        by_cap = {id(cap): params for cap, params in plan}
        for idx, cap in enumerate(caps):
            params = by_cap.get(id(cap))
            if not params:
                continue
            block = "".join(
                f'  parameters:\n'
                + "".join(
                    f'  - name: "{p["name"]}"\n'
                    f'    type: {p["type"]}\n'
                    f'    description: {p["description"]}\n'
                    for p in params
                )
            )
            lines[empty_lines[idx]] = block
        f.write_text("".join(lines), encoding="utf-8")
        updated += 1

    print(f"files with empty parameter lists (no evidence): {unchanged}")
    print(f"files skipped (parameters:[] count mismatch): {skipped}")
    print(f"files to update: {updated}")
    for name, cap, flags in samples:
        print(f"  {name:<40} {cap!r:>25} -> {flags}")
    if args.apply:
        print("applied.")


if __name__ == "__main__":
    main()