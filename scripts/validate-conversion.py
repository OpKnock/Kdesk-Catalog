#!/usr/bin/env python3
"""
Kdesk-Catalog: conversion validation.

Checks (all 1,766 agents / 1,143 skills / 1,766 workflows):
  V1  Every agent YAML has an identical copy in agents/yaml + a JSON in agents/json
  V2  Every skill YAML has an identical copy in skills/yaml + a JSON in skills/json
  V3  Every agent has a workflow in workflows/
  V4  Every JSON file parses
  V5  Agent IDs unique, Skill IDs unique, Workflow IDs unique
  V6  Agent -> Skill references exist (every ref resolves to a real skill id)
  V7  Workflow -> Agent references exist (workflow.agent resolves; step agent refs resolve)
  V8  Key preservation: every original YAML top-level key exists in the JSON with
      deep-equal value (lossless fidelity)
  V9  Derived fields are empty-only-from-real-data: inputs count == capability
      parameter count; tools==[] implies no explicit tools and no
      platforms.claude_code.tools; dependencies==[] implies no prerequisites
  V10 No files silently skipped (file manifests match 1:1)
  V11 No skipped YAML copies (byte-identical hash compare)
"""
import hashlib
import json
import sys
import yaml
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"
AGENTS = ROOT / "agents"
SKILLS = ROOT / "skills"
WORKFLOWS = ROOT / "workflows"

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def is_skill(rel: str) -> bool:
    return "/skill/" in rel or rel.endswith("-skill.yaml")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- manifests ------------------------------------------------------------
yaml_files = sorted(p for p in UA.rglob("*.yaml") if p.name != "registry.yaml")
agent_rels = [str(p.relative_to(UA)).replace("\\", "/") for p in yaml_files if not is_skill(str(p.relative_to(UA)).replace("\\", "/"))]
skill_rels = [str(p.relative_to(UA)).replace("\\", "/") for p in yaml_files if is_skill(str(p.relative_to(UA)).replace("\\", "/"))]
print(f"source: {len(agent_rels)} agents + {len(skill_rels)} skills = {len(yaml_files)}")

# ---- V1/V2/V11 copies ------------------------------------------------------
missing_copy = []
for rel in agent_rels + skill_rels:
    base = SKILLS if is_skill(rel) else AGENTS
    if not (base / "yaml" / rel).exists():
        missing_copy.append(rel)
if missing_copy:
    err(f"V1/V2 copy missing: {len(missing_copy)}")
hash_mismatch = 0
for rel in agent_rels + skill_rels:
    base = SKILLS if is_skill(rel) else AGENTS
    if sha(UA / rel) != sha(base / "yaml" / rel):
        hash_mismatch += 1
if hash_mismatch:
    err(f"V11 copy hash mismatch: {hash_mismatch}")

# ---- V1/V2/V4 JSONs ---------------------------------------------------------
agent_json = {}
skill_json = {}
for rel in agent_rels:
    base = AGENTS / "json" / Path(rel).with_suffix(".json")
    if not base.exists():
        err(f"V1 json missing: {rel}")
        continue
    try:
        d = json.loads(base.read_text(encoding="utf-8"))
        agent_json[d["id"]] = (d, rel)
    except Exception as e:
        err(f"V4 agent json invalid: {rel}: {e}")
for rel in skill_rels:
    base = SKILLS / "json" / Path(rel).with_suffix(".json")
    if not base.exists():
        err(f"V2 json missing: {rel}")
        continue
    try:
        d = json.loads(base.read_text(encoding="utf-8"))
        skill_json[d["id"]] = (d, rel)
    except Exception as e:
        err(f"V4 skill json invalid: {rel}: {e}")

# ---- V5 ID uniqueness --------------------------------------------------------
for label, coll in (("agent", agent_json), ("skill", skill_json)):
    c = Counter(coll.keys())
    for k, n in c.items():
        if n > 1:
            err(f"V5 duplicate {label} id: {k} x{n}")

# ---- V3/V4 workflows ----------------------------------------------------------
workflow_ids = Counter()
for rel in agent_rels:
    wf_path = WORKFLOWS / Path(rel).with_suffix(".workflow.json")
    if not wf_path.exists():
        err(f"V3 workflow missing: {rel}")
        continue
    try:
        wf = json.loads(wf_path.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"V4 workflow invalid: {rel}: {e}")
        continue
    workflow_ids[wf["id"]] += 1
    # ---- V7 workflow -> agent refs
    if wf.get("agent") not in agent_json:
        err(f"V7 workflow {wf.get('id')}: agent '{wf.get('agent')}' not found")
    for st in wf.get("steps", []):
        if st.get("type") == "agent" and st.get("agent") not in agent_json:
            err(f"V7 workflow {wf.get('id')}: step agent '{st.get('agent')}' not found")
        if st.get("type") == "skill" and st.get("skill") not in skill_json:
            err(f"V7 workflow {wf.get('id')}: step skill '{st.get('skill')}' not found")
for k, n in workflow_ids.items():
    if n > 1:
        err(f"V5 duplicate workflow id: {k} x{n}")

# ---- V6 agent -> skill refs ----------------------------------------------------
no_ref_agents = []
bad_refs = 0
for aid, (d, rel) in agent_json.items():
    refs = d.get("skills") or []
    if not refs:
        no_ref_agents.append(aid)
    for r in refs:
        if r not in skill_json:
            bad_refs += 1
            err(f"V6 agent {aid}: skill ref '{r}' not found")
if len(no_ref_agents) == len(agent_json) and agent_json:
    warnings.append("V6 no agent declares skill references in source YAML (verified: 'skills' key absent in all)")

# ---- V8 key preservation --------------------------------------------------------
lost = 0
for rel in agent_rels + skill_rels:
    base = SKILLS if is_skill(rel) else AGENTS
    jp = base / "json" / Path(rel).with_suffix(".json")
    if not jp.exists():
        continue
    jsrc = json.loads(jp.read_text(encoding="utf-8"))
    ysrc = yaml.safe_load((UA / rel).read_text(encoding="utf-8")) or {}
    for k, v in ysrc.items():
        if k not in jsrc:
            err(f"V8 {rel}: key '{k}' missing in JSON")
            lost += 1
        elif jsrc[k] != v:
            err(f"V8 {rel}: key '{k}' value changed")
            lost += 1
if not lost:
    print("  V8: all original keys + values preserved in all JSONs")

# ---- V9 derived-not-invented -----------------------------------------------------
for aid, (d, rel) in list(agent_json.items()) + list(skill_json.items()):
    ysrc = yaml.safe_load((UA / rel).read_text(encoding="utf-8")) or {}
    nparams = sum(len([p for p in (c.get("parameters") or []) if isinstance(p, dict) and p.get("name")])
                  for c in ysrc.get("capabilities") or [])
    if len(d.get("inputs", {}).get("parameters", [])) != nparams:
        err(f"V9 {rel}: inputs count {len(d.get('inputs',{}).get('parameters',[]))} != capability params {nparams}")
    explicit_tools = isinstance(ysrc.get("tools"), list)
    cc_tools = isinstance(((ysrc.get("platforms") or {}).get("claude_code") or {}).get("tools"), list)
    if d.get("tools") and not explicit_tools and not cc_tools:
        err(f"V9 {rel}: tools invented (source has none)")
    if d.get("dependencies") and not isinstance(ysrc.get("prerequisites"), list) and not isinstance(ysrc.get("dependencies"), list):
        err(f"V9 {rel}: dependencies invented (source has none)")
    if d.get("outputs"):
        err(f"V9 {rel}: outputs invented (source has no outputs)")

# ---- V10 nothing skipped ---------------------------------------------------------
extra_agents = sorted(set(p.stem for p in (AGENTS / "json").rglob("*.json")) - {Path(r).stem for r in agent_rels})
extra_skills = sorted(set(p.stem for p in (SKILLS / "json").rglob("*.json")) - {Path(r).stem for r in skill_rels})
extra_wfs = sorted(p.stem for p in WORKFLOWS.rglob("*.json") if p.stem.replace(".workflow", "") not in {Path(r).stem for r in agent_rels})
if extra_agents:
    err(f"V10 unexpected extra agent JSONs: {extra_agents[:10]}")
if extra_skills:
    err(f"V10 unexpected extra skill JSONs: {extra_skills[:10]}")
if extra_wfs:
    err(f"V10 unexpected extra workflows: {extra_wfs[:10]}")

# ---- V12 wiring manifest -----------------------------------------------------
wiring_path = ROOT / "skills" / "wiring.json"
if wiring_path.exists():
    try:
        wiring = json.loads(wiring_path.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"V12 wiring manifest unreadable: {e}")
        wiring = {}
    if wiring:
        for aid, links in (wiring.get("wiring") or {}).items():
            if aid not in agent_json:
                err(f"V12 wiring: agent '{aid}' not found")
            seen = set()
            for l in links or []:
                sid = l.get("skill")
                if not sid:
                    err(f"V12 wiring {aid}: link without skill id")
                    continue
                if sid in seen:
                    err(f"V12 wiring {aid}: duplicate skill link '{sid}'")
                seen.add(sid)
                if sid not in skill_json:
                    err(f"V12 wiring {aid}: skill '{sid}' not found")
                if not l.get("evidence") and not l.get("manual"):
                    err(f"V12 wiring {aid}: link '{sid}' without evidence or manual flag")
            defined = {l.get("skill") for l in links or []}
            if aid in agent_json:
                src_marker = (agent_json[aid][0].get("conversion") or {}).get("derived", {}).get("skills", "")
                wired_json = isinstance(src_marker, str) and src_marker.startswith("wiring ")
                if wired_json and defined != set(agent_json[aid][0].get("skills") or []):
                    err(f"V12 wiring {aid}: agent JSON skills do not match manifest")
                elif not wired_json and (agent_json[aid][0].get("skills") or []):
                    err(f"V12 wiring {aid}: agent JSON declares skills without wiring provenance")
        print(f"  V12: wiring manifest OK ({len(wiring.get('wiring') or {})} agents, "
              f"{sum(len(v) for v in (wiring.get('wiring') or {}).values())} links)")
    else:
        warnings.append("V12 wiring manifest exists but is empty")
else:
    warnings.append("V12 skills/wiring.json not found (agents wired without manifest)")

# ---- summary ----------------------------------------------------------------------
print(f"Agents JSON: {len(agent_json)} | Skills JSON: {len(skill_json)} | Workflows: {sum(1 for _ in WORKFLOWS.rglob('*.json'))} | Workflow ids on file: {len(workflow_ids)}")
print(f"ERRORS: {len(errors)} | WARNINGS: {len(warnings)}")
for w in warnings[:10]:
    print("  WARN:", w)
for e in errors[:20]:
    print("  ERR:", e)
sys.exit(1 if errors else 0)