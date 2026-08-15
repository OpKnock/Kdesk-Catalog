#!/usr/bin/env python3
"""Compute agent->skill wiring from real tool evidence and write a separate manifest.

Rule (traceable, no invention):
  A skill is linked to an agent when tokens from the skill's declared
  `tools`/`prerequisites` match tool tokens found in the agent's capability
  commands (first word per command) or the agent's declared `tools`.

Writes: <out>/wiring.json  {"version", "rule", "created_at", "stats", "wiring"}
Each wiring entry: {"skill": <id>, "evidence": [tokens...], "score": n}
scores sorted desc, skill name asc. Only evidence-backed links are emitted.

Usage:
  python scripts/wire-skills.py --agents universal-agents --out skills/wiring.json
"""
import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

STOP_WORDS = {"and", "with", "using", "for", "or", "the", "a", "an", "via", "of", "in", "to", "on"}
GENERIC_TOKENS = {"curl"}  # universal fetch primitive: no evidence value
WEAK_TOKENS = {"aws", "gcloud", "az", "awscli", "git", "docker", "kubectl", "helm",
               "npx", "npm", "yarn", "pnpm", "pip", "pip3", "python", "python3",
               "node", "gh", "ssh", "bash", "make", "go", "cd", "ls"}  # provider/generic CLIs: weak evidence alone
MIN_TOKEN_LEN = 2  # short-but-distinct CLIs (op, bw, k6, mb, yq, ng) are real evidence


def is_skill(rel: str) -> bool:
    return "/skill/" in rel or rel.endswith("-skill.yaml")


def normalize_skill_tokens(tool_strs):
    tokens = set()
    for t in tool_strs:
        if not isinstance(t, str):
            continue
        for word in re.split(r"[\s,]+", t):
            word = word.strip(".:()[]'\"").lower()
            if len(word) >= MIN_TOKEN_LEN and word not in STOP_WORDS and word not in GENERIC_TOKENS and not word.isdigit():
                tokens.add(word)
    return tokens


def match(agent_word: str, skill_token: str) -> bool:
    return agent_word == skill_token


def agent_command_tokens(doc: dict) -> set:
    """First word of every capability command, labels excluded, generic CLIs removed."""
    words = set()
    for cap in doc.get("capabilities") or []:
        for cmd in cap.get("commands") or []:
            if isinstance(cmd, str) and cmd.strip():
                word = cmd.strip().split()[0]
                if word.endswith(":"):
                    continue  # block-style YAML label, not a binary
                word = word.strip(":()[]'\"").lower()
                if len(word) >= MIN_TOKEN_LEN and word not in GENERIC_TOKENS and not word.isdigit():
                    words.add(word)
    return words


def compute_wiring(agent_docs: dict, skill_docs: dict, threshold: float = 0.15,
                   max_links: int = 12) -> dict:
    """Compute evidence-backed agent->skill links.

    agent_docs: {name: yaml doc}; skill_docs: {name: yaml doc}.
    Returns {"wiring": {agent: [{"skill","evidence","score"}...]}, "stats": {...}}.
    """
    skill_tokens = {}
    for name, d in skill_docs.items():
        tools = list(d.get("tools") or []) + list(d.get("prerequisites") or [])
        skill_tokens[name] = normalize_skill_tokens(tools)
    tokfreq = Counter(t for toks in skill_tokens.values() for t in toks)
    wiring = {}
    matched_agents = 0
    for name, d in sorted(agent_docs.items()):
        agent_words = agent_command_tokens(d)
        links = {}
        for skill_name, tokens in skill_tokens.items():
            if not tokens:
                continue
            evidence = sorted(agent_words & tokens)
            if not evidence:
                continue
            strong = [t for t in evidence if t not in WEAK_TOKENS]
            score = sum(1.0 / tokfreq[t] for t in strong)
            if score >= threshold or len(evidence) >= 2:
                links[skill_name] = evidence
        if links:
            matched_agents += 1
            wiring[name] = [
                {"skill": s, "evidence": links[s],
                 "score": sum(1.0 / tokfreq[t] for t in links[s] if t not in WEAK_TOKENS)}
                for s in sorted(links,
                                key=lambda k: (-sum(1.0 / tokfreq[t] for t in links[k] if t not in WEAK_TOKENS), k))
            ][: max_links]
    total_links = sum(len(v) for v in wiring.values())
    used_skills = len({l["skill"] for links in wiring.values() for l in links})
    return wiring, {
        "agents": len(agent_docs),
        "skills_with_tool_evidence": len([s for s in skill_tokens.values() if s]),
        "skills_without_evidence": len([s for s in skill_tokens.values() if not s]),
        "agents_wired": matched_agents,
        "skills_used": used_skills,
        "total_links": total_links,
        "unwired_agents": len(agent_docs) - matched_agents,
    }


def load_overrides(path):
    """Committed hand-verified agent->skill links file (YAML):
    agents:
      <agent-id>:
        - <skill-id>
        - <skill-id>
    """
    if not path:
        return {}
    import yaml
    raw = Path(path).read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}
    return {str(aid): [str(s) for s in skills]
            for aid, skills in (data.get("agents") or {}).items() if isinstance(skills, list)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agents", default="universal-agents", help="source YAML dir")
    ap.add_argument("--out", default="skills/wiring.json", help="wiring manifest output")
    ap.add_argument("--overrides", default="skills/wiring-overrides.yaml",
                    help="committed hand-verified links (merged as manual: true)")
    ap.add_argument("--threshold", type=float, default=0.15,
                    help="min rarity-weighted evidence score (1/freq per matched token)")
    ap.add_argument("--max-links", type=int, default=12, help="max links per agent")
    args = ap.parse_args()

    src = Path(args.agents)
    skill_by_rel = {}
    agent_by_rel = {}
    for f in sorted(src.rglob("*.yaml")):
        if f.name == "registry.yaml":
            continue
        rel = str(f.relative_to(src)).replace("\\", "/")
        try:
            doc = f.read_text(encoding="utf-8")
            import yaml
            data = yaml.safe_load(doc) or {}
        except Exception as e:
            print(f"  ERROR reading {rel}: {e}", file=sys.stderr)
            sys.exit(1)
        if is_skill(rel):
            skill_by_rel[rel] = data
        else:
            agent_by_rel[rel] = data

    agent_docs = {d.get("name"): d for d in agent_by_rel.values() if d.get("name")}
    skill_docs = {d.get("name"): d for d in skill_by_rel.values() if d.get("name")}
    wiring, stats_w = compute_wiring(agent_docs, skill_docs,
                                     threshold=args.threshold, max_links=args.max_links)

    overrides = load_overrides(args.overrides)
    if overrides:
        bad_agents = sorted(set(overrides) - set(agent_docs))
        bad_skills = sorted({s for skills in overrides.values() for s in skills} - set(skill_docs))
        if bad_agents or bad_skills:
            print("  ERROR unresolvable wiring overrides:", file=sys.stderr)
            if bad_agents:
                print(f"    agents: {bad_agents}", file=sys.stderr)
            if bad_skills:
                print(f"    skills: {bad_skills}", file=sys.stderr)
            sys.exit(1)
        for aid, skills in overrides.items():
            existing = {l["skill"] for l in wiring.get(aid, [])}
            manual = [{"skill": s, "evidence": [], "score": 0, "manual": True}
                      for s in skills if s not in existing]
            wired = wiring.setdefault(aid, [])
            wired.extend(manual)
            wired.sort(key=lambda l: (not l.get("manual"), -l.get("score", 0), l["skill"]))
        stats_w["manual_links"] = sum(1 for links in wiring.values()
                                      for l in links if l.get("manual"))
        stats_w["agents_wired"] = len(wiring)
        stats_w["total_links"] = sum(len(v) for v in wiring.values())
        stats_w["unwired_agents"] = len(agent_docs) - len(wiring)

    missing_agents = sorted(set(wiring) - set(agent_docs))
    missing_skills = sorted(
        {link["skill"] for links in wiring.values() for link in links} - set(skill_docs)
    )
    total_links = stats_w["total_links"]
    used_skills = stats_w["skills_used"]
    manifest = {
        "version": "1",
        "rule": ("tool-evidence: exact match of agent capability command tokens against "
                 "skill tools/prerequisites tokens; score = sum(1/token-freq) over STRONG "
                 "tokens (non-generic CLIs); link kept iff score >= threshold OR >= 2 distinct "
                 "matching tokens; generic CLIs (curl, aws, gcloud, docker, kubectl, helm, "
                 "python, node, git, npm, npx, go, cd, ls, ...) are weak evidence alone; "
                 "short-but-distinct CLIs (op, bw, k6, mb, yq, ng, jq, >= 2 chars) count as "
                 "evidence; block-style YAML label words (first word ending in ':') excluded; "
                 "skills without tools/prerequisites have no tokens and are reported as "
                 "skills_without_evidence (conceptual skills: not auto-wireable by design); "
                 "no invented links"),
        "created_at": date.today().isoformat(),
        "stats": stats_w,
        "wiring": wiring,
    }
    if missing_agents or missing_skills:
        print("  ERROR unresolvable wiring references:", file=sys.stderr)
        if missing_agents:
            print(f"    agents: {missing_agents}", file=sys.stderr)
        if missing_skills:
            print(f"    skills: {missing_skills}", file=sys.stderr)
        sys.exit(1)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wiring manifest: {out}")
    print(f"  agents: {manifest['stats']['agents']} | skills with evidence: {manifest['stats']['skills_with_tool_evidence']}")
    print(f"  agents wired: {manifest['stats']['agents_wired']} | skills used: {used_skills} | links: {total_links}")
    print(f"  unwired agents: {manifest['stats']['unwired_agents']}")
    for agent, links in list(wiring.items())[:5]:
        print(f"    {agent} -> {[l['skill'] for l in links][:4]}")


if __name__ == "__main__":
    main()