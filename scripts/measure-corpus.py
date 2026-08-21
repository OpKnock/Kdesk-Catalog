#!/usr/bin/env python3
"""measure-corpus.py - quantify template fingerprints to curate.

Reads reports/curation-status.json and produces, for every template-tier file,
the exact fields that need fixing, plus aggregates:
  - unique knowledge titles/sources pointing at kdesk/agents
  - unique placeholder commands (with <>/example.com/TODO)
  - identity.py command occurrences
  - registry.example.com occurrences
  - generic descriptions

Output: reports/curation-plan.json (machine-readable) + console summary.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

PLACEHOLDER_RE = re.compile(r"<[^>]*>|example\.com|TODO", re.IGNORECASE)
REGISTRY_RE = re.compile(r"registry\.example\.com", re.IGNORECASE)
IDENTITY_RE = re.compile(r"identity\.py", re.IGNORECASE)


def main():
    status = json.loads((ROOT / "reports" / "curation-status.json").read_text(encoding="utf-8"))
    files = status["files"]

    plan = {}
    kdesk_sources = collections.Counter()
    kdesk_titles = collections.Counter()
    placeholder_cmds = collections.Counter()
    identity_cmds = collections.Counter()
    registry_cmds = collections.Counter()
    generic_descs = collections.Counter()
    name_desc_pairs = collections.Counter()
    unparseable = []

    n_templ = 0
    for rel, meta in files.items():
        if meta["tier"] != "template":
            continue
        n_templ += 1
        path = UA / rel
        if not path.exists():
            continue
        txt = path.read_text(encoding="utf-8")
        try:
            doc = yaml.safe_load(txt) or {}
        except yaml.YAMLError:
            unparseable.append(rel)
            plan[rel] = {"name": None, "fingerprints": meta["fingerprints"], "fixes": ["unparseable"]}
            continue

        entry = {"name": doc.get("name"), "fingerprints": meta["fingerprints"], "fixes": []}

        if "kdesk_agents_link" in meta["fingerprints"]:
            for k in doc.get("knowledge") or []:
                src = str(k.get("source") or "")
                if "kdesk/agents" in src:
                    kdesk_sources[src] += 1
                    kdesk_titles[str(k.get("title") or "?")] += 1
                    entry["fixes"].append("knowledge")
        if "placeholder_command" in meta["fingerprints"]:
            for cap in doc.get("capabilities") or []:
                if not isinstance(cap, dict):
                    continue
                for cmd in cap.get("commands") or []:
                    if PLACEHOLDER_RE.search(str(cmd)):
                        placeholder_cmds[str(cmd)] += 1
                        entry["fixes"].append("command")
        if "identity_py" in meta["fingerprints"]:
            for cap in doc.get("capabilities") or []:
                if not isinstance(cap, dict):
                    continue
                for cmd in cap.get("commands") or []:
                    if IDENTITY_RE.search(str(cmd)):
                        identity_cmds[str(cmd)] += 1
                        entry["fixes"].append("identity")
        if "registry_example" in meta["fingerprints"]:
            for cap in doc.get("capabilities") or []:
                if not isinstance(cap, dict):
                    continue
                for cmd in cap.get("commands") or []:
                    if REGISTRY_RE.search(str(cmd)):
                        registry_cmds[str(cmd)] += 1
                        entry["fixes"].append("registry")
        if "generic_description" in meta["fingerprints"]:
            name = str(doc.get("name") or "")
            desc = str(doc.get("description") or "")
            generic_descs[desc] += 1
            name_desc_pairs[(name, desc[:80])] += 1
            entry["fixes"].append("description")

        plan[rel] = entry

    out = {
        "template_files": n_templ,
        "unparseable": unparseable,
        "kdesk_sources": dict(kdesk_sources.most_common()),
        "kdesk_titles": dict(kdesk_titles.most_common()),
        "placeholder_commands": dict(placeholder_cmds.most_common(300)),
        "identity_commands": dict(identity_cmds.most_common(100)),
        "registry_commands": dict(registry_cmds.most_common(100)),
        "generic_descriptions": dict(generic_descs.most_common(200)),
        "files": plan,
    }
    (ROOT / "reports" / "curation-plan.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8"
    )

    print(f"template files: {n_templ}")
    print(f"unparseable yaml files: {len(unparseable)}")
    if unparseable:
        for f in unparseable[:20]:
            print(f"  !! {f}")
    print(f"unique kdesk/agents sources: {len(kdesk_sources)}")
    print(f"unique kdesk/agents titles: {len(kdesk_titles)}")
    print(f"unique placeholder commands: {len(placeholder_cmds)}")
    print(f"unique identity.py commands: {len(identity_cmds)}")
    print(f"unique registry.example.com commands: {len(registry_cmds)}")
    print(f"unique generic descriptions: {len(generic_descs)}")
    print("\n--- top kdesk titles ---")
    for t, n in kdesk_titles.most_common(40):
        print(f"  {n:4d}  {t[:90]}")
    print("\n--- top placeholder commands ---")
    for c, n in placeholder_cmds.most_common(30):
        print(f"  {n:4d}  {c[:100]}")
    print("\n--- top identity.py commands ---")
    for c, n in identity_cmds.most_common(15):
        print(f"  {n:4d}  {c[:100]}")
    print("\n--- top registry commands ---")
    for c, n in registry_cmds.most_common(15):
        print(f"  {n:4d}  {c[:100]}")


if __name__ == "__main__":
    main()