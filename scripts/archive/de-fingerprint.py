#!/usr/bin/env python3
"""de-fingerprint.py - one content-consistency pass over the curated corpus.

Closes the residual generator fingerprints AFTER L1 file renames, all content-derived:

  1. Description serials: drop generator `vN` serials (`agent v2`, `auth v5`, ...)
     from descriptions of files whose role word precedes the serial (agent|auth|
     deploy|sdk|server|client|workflow). Real tool versions (Artillery v2, OpenAPI v2,
     FCM v1, KV v2, HTTP v2, grpc-gateway v2) never match a role word and are untouched.
  2. Keyword quarantine: keyword sets shared verbatim by <= SHARED_MAX files are
     family-sized copy-paste sets; tokens not evidenced ANYWHERE in the file's own
     content (name, display_name, description, capability descriptions + commands,
     knowledge titles, instructions) are dropped per file. Multi-word keywords are
     normalized ('screen reader' == 'screen-reader'). Category labels shared by many
     files (['api'], ['ml','agent']) are never a leak and are untouched.
  3. System prompt sync: files whose `generic.system_prompt` says
     "You are an expert in <old>" while the file name changed get the new name —
     the L1 rename updated names but not this template slot.
  4. Husk cleanup: delete empty directories left behind by renames (git tracks no
     empty dirs; these are disk-only residue).

Idempotent: only files that still carry a fingerprint are touched.

Usage:
  python scripts/de-fingerprint.py           # preview (no writes)
  python scripts/de-fingerprint.py --apply   # apply all four fixes
"""
import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"

ROLE_WORD_RE = re.compile(r"\b(agent|auth|deploy|sdk|server|client|workflow) +v[0-9]+\b")
SERIAL_RE = re.compile(r"\b(v[0-9]+)[\s:.]*")
EXPERT_RE = re.compile(r"^(You are an expert in )([^.]*?)(\. .*)?$", re.DOTALL)
SHARED_MAX = 10  # sets shared by >10 files are category labels, not leaks


def de_serial(desc: str):
    if not ROLE_WORD_RE.search(desc):
        return None
    out = re.sub(r"\s{2,}", " ", SERIAL_RE.sub("", desc)).strip()
    return out if out != desc else None


def content_blob(doc: dict) -> str:
    texts = [
        str(doc.get("name") or ""),
        str(doc.get("display_name") or ""),
        str(doc.get("description") or ""),
        str(doc.get("instructions") or ""),
    ]
    for cap in (doc.get("capabilities") or []):
        texts.append(str(cap.get("description") or ""))
        texts.extend(str(c) for c in (cap.get("commands") or []))
    texts.extend(str(k.get("title") or "") for k in (doc.get("knowledge") or []))
    return re.sub(r"[^a-z0-9]+", "-", " ".join(texts).lower())


def quarantine_keywords(doc: dict, kws: list, set_count: int):
    if set_count > SHARED_MAX:
        return None
    blob = content_blob(doc)
    keep = [k for k in kws if re.sub(r"[^a-z0-9]+", "-", str(k).lower()).strip("-") in blob]
    if len(keep) == len(kws):
        return None
    if not keep:
        keep = re.findall(r"[a-z][a-z0-9-]*", str(doc.get("name") or "").lower())[:2]
    return keep


def sync_expert(sp: str, name: str):
    m = EXPERT_RE.match(sp)
    if not m or m.group(2).strip().lower() == str(name).strip().lower():
        return None
    tail = m.group(3) or ""
    return f"You are an expert in {name}." + (tail if tail else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    docs = {}
    for f in UA.rglob("*.yaml"):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            docs[f] = d
    kwset_count = {}
    for d in docs.values():
        key = tuple(d.get("keywords") or d.get("tags") or [])
        if key:
            kwset_count[key] = kwset_count.get(key, 0) + 1

    n_desc = n_kw = n_prompt = 0
    samples = []
    for f, doc in sorted(docs.items()):
        fixes = []
        d = doc.get("description")
        if isinstance(d, str) and (new := de_serial(d)):
            fixes.append(("desc", f"description: {d!r} -> {new!r}"[:110]))
            doc["description"] = new
        kws = doc.get("keywords") or doc.get("tags") or []
        key = tuple(str(k) for k in kws)
        if kws and (keep := quarantine_keywords(doc, kws, kwset_count.get(key, 0))):
            fixes.append(("keywords", f"{kws} -> {keep}"[:100]))
            if "keywords" in doc:
                doc["keywords"][:] = keep
            else:
                doc["tags"][:] = keep
        sp = ((doc.get("platforms") or {}).get("generic") or {}).get("system_prompt")
        name = doc.get("name")
        if isinstance(sp, str) and (new := sync_expert(sp, name)):
            fixes.append(("prompt", f"expert-in {name}"[:60]))
            doc["platforms"]["generic"]["system_prompt"] = new
        if not fixes:
            continue
        for kind, msg in fixes[:3]:
            samples.append((kind, f.name, msg))
            if kind == "desc":
                n_desc += 1
            elif kind == "keywords":
                n_kw += 1
            else:
                n_prompt += 1
        if args.apply:
            f.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")

    husks = [d for d in UA.rglob("*") if d.is_dir() and not any(d.rglob("*"))]
    for d in husks:
        if args.apply:
            d.rmdir()

    print(f"description serials fixed: {n_desc} | keyword sets quarantined: {n_kw} | prompts synced: {n_prompt}")
    print(f"empty husk dirs removed: {len(husks)}")
    if not args.apply:
        for kind, fname, msg in samples[:14]:
            print(f"  [{kind}] {fname}: {msg}")


if __name__ == "__main__":
    main()