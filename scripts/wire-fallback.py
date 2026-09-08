#!/usr/bin/env python3
"""Extend skills/wiring.json with fallback tier for unwired agents.

Tool-evidence links (from wire-skills.py) are kept intact. For each unwired
agent, find top skills by secondary evidence, in order:
  1. same category + subcategory
  2. shared tags (>=2) or keywords
  3. capability-name token overlap with skill name/tags
  4. same category (last resort)

Links are marked {"fallback": true} with evidence strings like
"category:api", "tags:rest,openapi", "capability:endpoint-design".
Scores are small (0.01-0.09) so tool-evidence always ranks above fallback.

Usage: python scripts/wire-fallback.py [--max-links 3]
"""
import argparse
import json
import re
from pathlib import Path

import yaml


def tokens(s: str) -> set:
    return set(t for t in re.split(r"[^a-z0-9]+", str(s).lower()) if len(t) >= 3)


def load_docs(src: Path):
    agents, skills = {}, {}
    for f in sorted(src.rglob("*.yaml")):
        if f.name == "registry.yaml":
            continue
        rel = str(f.relative_to(src)).replace("\\", "/")
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        name = data.get("name")
        if not name:
            continue
        if "/skill/" in rel or rel.endswith("-skill.yaml"):
            skills[name] = data
        else:
            agents[name] = data
    return agents, skills


def fallback_links(agent_doc: dict, skills: dict, max_links: int = 3):
    acat = str(agent_doc.get("category", ""))
    asub = str(agent_doc.get("subcategory") or "")
    atags = set(str(t).lower() for t in (agent_doc.get("tags") or []))
    akeys = set(str(k).lower() for k in (agent_doc.get("keywords") or []))
    acaps = set()
    for cap in agent_doc.get("capabilities") or []:
        if isinstance(cap, dict) and cap.get("name"):
            acaps |= tokens(cap["name"])
            acaps |= tokens(cap.get("description", ""))
    scored = []
    for sname, sdoc in skills.items():
        scat = str(sdoc.get("category", ""))
        ssub = str(sdoc.get("subcategory") or "")
        stags = set(str(t).lower() for t in (sdoc.get("tags") or []))
        skeys = set(str(k).lower() for k in (sdoc.get("keywords") or []))
        ev, score = [], 0.0
        if acat and acat == scat:
            ev.append(f"category:{acat}")
            score += 0.03
            if asub and asub == ssub:
                ev.append(f"subcategory:{asub}")
                score += 0.02
        shared_tags = (atags | akeys) & (stags | skeys)
        if len(shared_tags) >= 2:
            ev.append("tags:" + ",".join(sorted(shared_tags)[:3]))
            score += 0.02 + 0.005 * len(shared_tags)
        cap_overlap = acaps & (tokens(sname) | stags | skeys)
        if cap_overlap:
            ev.append("capability:" + ",".join(sorted(cap_overlap)[:3]))
            score += 0.02
        # same skill-family name prefix (e.g. api-rest-agent <-> api-rest)
        anorm = re.sub(r"[^a-z0-9]+", "-", agent_doc.get("name", "").lower()).strip("-")
        snorm = re.sub(r"[^a-z0-9]+", "-", sname.lower()).strip("-")
        if snorm and (anorm.startswith(snorm) or snorm in anorm):
            ev.append(f"name-match:{snorm}")
            score += 0.03
        if ev and score > 0:
            scored.append((score, sname, ev))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [{"skill": s, "evidence": ev, "score": round(sc, 4), "fallback": True}
            for sc, s, ev in scored[:max_links]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents", default="universal-agents")
    ap.add_argument("--wiring", default="skills/wiring.json")
    ap.add_argument("--max-links", type=int, default=3)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    src = root / args.agents
    wpath = root / args.wiring
    manifest = json.loads(wpath.read_text(encoding="utf-8"))
    wiring = manifest.get("wiring", {})
    agents, skills = load_docs(src)
    added_agents, added_links = 0, 0
    for aname in sorted(agents):
        if aname in wiring and wiring[aname]:
            continue
        links = fallback_links(agents[aname], skills, args.max_links)
        if links:
            wiring[aname] = links
            added_agents += 1
            added_links += len(links)
    manifest["wiring"] = wiring
    stats = manifest.get("stats", {})
    stats["fallback_agents"] = added_agents
    stats["fallback_links"] = added_links
    stats["agents_wired"] = len(wiring)
    stats["total_links"] = sum(len(v) for v in wiring.values())
    stats["unwired_agents"] = len(agents) - len(wiring)
    stats["skills_used"] = len({l["skill"] for links in wiring.values() for l in links})
    manifest["stats"] = stats
    manifest["rule"] = manifest.get("rule", "") + " | fallback tier: category/subcategory/tags/capability-name overlap, marked fallback:true, score<0.1, tool-evidence always ranks first."
    wpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"fallback: +{added_agents} agents, +{added_links} links")
    print(f"wired {stats['agents_wired']}/{len(agents)}, unwired {stats['unwired_agents']}, skills_used {stats['skills_used']}")


if __name__ == "__main__":
    main()
