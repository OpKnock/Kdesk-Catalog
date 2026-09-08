#!/usr/bin/env python3
"""Generate bundles/ from universal-agents divisions.

Each top-level universal-agents/<division>/ dir becomes bundles/<division>.json:
  {id, name, label, description, agents[], skills[], workflows[], counts}

Workflows are matched by workflow.agent in the division's agents.
Writes bundles/registry.json index too.
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
UA = ROOT / "universal-agents"
WF = ROOT / "workflows"
OUT = ROOT / "bundles"


def main():
    divisions = json.loads((ROOT / "divisions.json").read_text(encoding="utf-8")).get("divisions", {})
    OUT.mkdir(parents=True, exist_ok=True)
    # index agents/skills per division dir
    per_div = {}
    for f in sorted(UA.rglob("*.yaml")):
        if f.name == "registry.yaml":
            continue
        rel = f.relative_to(UA).as_posix()
        div = rel.split("/")[0]
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        name = doc.get("name") or f.stem
        is_skill = "/skill/" in rel or rel.endswith("-skill.yaml")
        entry = per_div.setdefault(div, {"agents": [], "skills": []})
        (entry["skills"] if is_skill else entry["agents"]).append(name)
    # workflows per agent
    wf_by_agent = {}
    for f in sorted(WF.rglob("*.workflow.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("agent"):
            wf_by_agent.setdefault(d["agent"], []).append(d.get("id", f.stem))
    index = []
    for div in sorted(per_div):
        agents = sorted(set(per_div[div]["agents"]))
        skills = sorted(set(per_div[div]["skills"]))
        wfs = sorted({wid for a in agents for wid in wf_by_agent.get(a, [])})
        meta = divisions.get(div, {})
        bundle = {
            "id": div,
            "name": div,
            "label": meta.get("label", div),
            "description": meta.get("description", f"{meta.get('label', div)} agents, skills, and workflows."),
            "agents": agents,
            "skills": skills,
            "workflows": wfs,
            "counts": {"agents": len(agents), "skills": len(skills), "workflows": len(wfs)},
        }
        (OUT / f"{div}.json").write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
        index.append({"id": div, **bundle["counts"]})
    (OUT / "registry.json").write_text(json.dumps({
        "version": "1.0.0",
        "bundles": len(index),
        "agents": sum(i["agents"] for i in index),
        "skills": sum(i["skills"] for i in index),
        "index": index,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"bundles: {len(index)} divisions, agents {sum(i['agents'] for i in index)}, skills {sum(i['skills'] for i in index)}")


if __name__ == "__main__":
    main()
