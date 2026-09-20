#!/usr/bin/env python3
"""
Kdesk-Catalog: YAML -> JSON + Workflows converter.

Converts every universal agent/skill YAML into a lossless JSON definition and
builds one workflow per agent. The source YAMLs (universal-agents/) are NEVER
modified. Target directories (agents/, skills/, workflows/) are generated
artifacts and are cleaned + rebuilt on every run.

Fidelity rules:
- Every original top-level key is preserved verbatim in the JSON.
- Derived fields (tools / skills / inputs / outputs / dependencies) are filled
  ONLY from data present in the source YAML; provenance is recorded in the
  "conversion" block so nothing invented is left untraceable.
- Nothing that is missing in the YAML is guessed; workflows contain no
  branches/loops/parallel/retry steps because the YAML defines none.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"
AGENTS = ROOT / "agents"
SKILLS = ROOT / "skills"
WORKFLOWS = ROOT / "workflows"

TOOL_NAME = "Kdesk-Catalog yaml-to-json"
WORKFLOW_SCHEMA = "workflow-v1"
JSON_SCHEMA = "definition-v1"

stats = {"agents": 0, "skills": 0, "workflows": 0, "errors": [], "warnings": []}


def is_skill(path: Path) -> bool:
    rel = str(path).replace("\\", "/")
    return "/skill/" in rel or path.name.endswith("-skill.yaml")


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    return (slug[:64]).rstrip("-") or "item"


def extract_tools(doc: dict):
    """Tools from real source data only: explicit 'tools' key, then platforms.claude_code.tools."""
    explicit = doc.get("tools")
    if isinstance(explicit, list):
        return "tools", [t for t in explicit if isinstance(t, str)]
    cc = (doc.get("platforms") or {}).get("claude_code") or {}
    pcc = cc.get("tools")
    if isinstance(pcc, list):
        return "platforms.claude_code.tools", [t for t in pcc if isinstance(t, str)]
    return "none", []


def extract_inputs(doc: dict):
    """Input parameters from capability 'parameters' blocks (real data)."""
    params = []
    for cap in doc.get("capabilities") or []:
        if not isinstance(cap, dict):
            continue
        for p in cap.get("parameters") or []:
            if isinstance(p, dict) and p.get("name"):
                params.append({
                    "capability": str(cap.get("name", "")),
                    "name": str(p["name"]),
                    "type": str(p.get("type", "")),
                    "description": str(p.get("description", "")),
                })
    return params


def extract_deps(doc: dict):
    """Dependencies: explicit 'prerequisites' key when present, else none."""
    pre = doc.get("prerequisites")
    if isinstance(pre, list):
        return "prerequisites", [str(p) for p in pre if isinstance(p, str)]
    deps = doc.get("dependencies")
    if isinstance(deps, list):
        return "dependencies", [str(d) for d in deps if isinstance(d, str)]
    return "none", []


def extract_skills(doc: dict):
    """Skill references: explicit 'skills' key when present (none today), else none."""
    s = doc.get("skills")
    if isinstance(s, list):
        return "skills", [str(x) for x in s if isinstance(x, str)]
    return "none", []


def build_definition(doc: dict, typ: str, rel: str, wiring: list = None, wiring_src: str = None,
                     provenance: dict = None) -> dict:
    """Lossless JSON: id + type, every original key verbatim, then derived fields.
    wiring: optional evidence-backed agent->skill links from skills/wiring.json;
    provenance records them so they are never confused with source YAML data.
    provenance: {source, checksum} block emitted as _provenance per spec §59."""
    out = {}
    for k, v in doc.items():
        out[k] = v
    out["id"] = str(doc["name"])
    out["type"] = typ
    tools_src, tools = extract_tools(doc)
    skills_src, skills = extract_skills(doc)
    deps_src, deps = extract_deps(doc)
    params = extract_inputs(doc)
    if typ == "agent" and wiring:
        skills = skills + [w["skill"] for w in wiring if w["skill"] not in skills]
        skills_src = f"wiring ({wiring_src})"
    out["skills"] = skills
    out["tools"] = tools
    out["inputs"] = {"parameters": params} if params else {}
    out["outputs"] = {}
    out["dependencies"] = deps
    out["conversion"] = {
        "tool": TOOL_NAME,
        "schema": JSON_SCHEMA,
        "source_yaml": rel,
        "derived": {
            "skills": skills_src,
            "tools": tools_src,
            "inputs": "capability.parameters" if params else "none",
            "outputs": "none (not present in source YAML)",
            "dependencies": deps_src,
        },
    }
    if provenance:
        out["_provenance"] = {
            "generated_by": TOOL_NAME,
            "generator_version": "1.0.0",
            "schema": JSON_SCHEMA,
            "source": f"universal-agents/{rel}",
            "checksum": provenance.get("checksum", ""),
        }
    if not skills and typ == "agent":
        stats["warnings"].append(f"agent '{doc['name']}': no explicit skill references in YAML -> skills: []")
    if not params:
        stats["warnings"].append(f"{typ} '{doc['name']}': no capability parameters -> inputs: {{}}")
    if not deps:
        stats["warnings"].append(f"{typ} '{doc['name']}': no tools/prerequisites -> dependencies: []")
    return out


def build_workflow(doc: dict, agent_id: str, rel: str, skills: list, params: list,
                   provenance: dict = None) -> dict:
    """Workflow for one agent: skill loads (only if referenced), agent step, then one
    capability step per capability in the original YAML (real execution order given by
    the capability list order). No branches/loops/parallel/retries are invented."""
    steps = []
    n = 0
    for sk in skills:
        n += 1
        steps.append({"id": f"step-{n}-load-skill-{sk}", "type": "skill", "skill": sk})
    n += 1
    agent_step = f"step-{n}-agent"
    steps.append({"id": agent_step, "type": "agent", "agent": agent_id, "input": "{{input}}"})
    last = agent_step
    for cap in doc.get("capabilities") or []:
        if not isinstance(cap, dict) or not cap.get("name"):
            continue
        n += 1
        cmds = cap.get("commands") or []
        tool = ""
        if cmds and isinstance(cmds[0], str) and cmds[0].strip():
            tool = cmds[0].strip().split()[0]
        sid = f"step-{n}-capability-{slugify(cap['name'])}"
        step = {"id": sid, "type": "capability", "capability": str(cap["name"]), "requires": agent_step}
        if tool:
            step["tool"] = tool
        steps.append(step)
        last = sid
    wf = {
        "id": f"wf-{agent_id}",
        "type": "workflow",
        "name": f"{doc.get('display_name', agent_id)} Workflow",
        "version": str(doc.get("version", "1.0.0")),
        "agent": agent_id,
        "description": str(doc.get("description", "")),
        "input": {"parameters": params} if params else {},
        "steps": steps,
        "output": {"result": f"{{{{{last}.output}}}}"},
        "conversion": {
            "tool": TOOL_NAME,
            "schema": WORKFLOW_SCHEMA,
            "source_yaml": rel,
            "note": ("steps reflect source order: skill loads (only referenced/wired skills) -> agent -> "
             "capabilities; no conditions/loops/parallel/retries defined in source"),
        },
    }
    if provenance:
        wf["_provenance"] = {
            "generated_by": TOOL_NAME,
            "generator_version": "1.0.0",
            "schema": WORKFLOW_SCHEMA,
            "source": f"universal-agents/{rel}",
            "checksum": provenance.get("checksum", ""),
        }
    return wf


def clean_targets():
    """Remove ONLY generated output, never non-generated files living in the
    output roots (e.g. skills/wiring.json)."""
    for d in (AGENTS, SKILLS, WORKFLOWS):
        if not d.exists():
            d.mkdir(parents=True)
            continue
        if not d.is_dir():
            stats["errors"].append(f"refusing to remove non-directory {d}")
            sys.exit(1)
        for child in d.iterdir():
            if d is WORKFLOWS:
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
            elif child.name in ("yaml", "json"):
                shutil.rmtree(child)


def write_json(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agents", default=str(UA), help="source YAML dir")
    ap.add_argument("--out", default=str(ROOT), help="output root (agents/, skills/, workflows/ created here)")
    ap.add_argument("--wiring", default=None,
                    help="skills/wiring.json manifest: merge evidence-backed skill links into agent JSONs and workflows")
    ap.add_argument("--inplace", action="store_true",
                    help="also write <name>.json next to each <name>.yaml inside the source dir (same path)")
    args = ap.parse_args()

    clean_targets()
    files = sorted(Path(args.agents).resolve().rglob("*.yaml"))
    if not files:
        stats["errors"].append("no YAML files found under universal-agents/")
        sys.exit(1)

    wiring_map = {}
    if args.wiring:
        try:
            w = json.loads(Path(args.wiring).read_text(encoding="utf-8"))
            wiring_map = {aid: [l for l in links if l.get("skill")]
                          for aid, links in w.get("wiring", {}).items()}
            stats["warnings"].append(f"wiring manifest {args.wiring}: {len(wiring_map)} agents with skill links")
        except Exception as e:
            stats["errors"].append(f"failed to load wiring manifest: {e}")
            sys.exit(1)

    for f in files:
        if f.name == "registry.yaml":
            continue
        rel = str(f.relative_to(UA)).replace("\\", "/")
        try:
            raw = f.read_text(encoding="utf-8")
            doc = yaml.safe_load(raw) if raw.strip() else None
            if not isinstance(doc, dict):
                stats["errors"].append(f"{rel}: YAML did not parse to a dict")
                continue
            if not doc.get("name"):
                stats["errors"].append(f"{rel}: missing 'name' field")
                continue
        except Exception as e:
            stats["errors"].append(f"{rel}: YAML parse error: {e}")
            continue

        typ = "skill" if is_skill(f) else "agent"
        stem = f.stem
        base = SKILLS if typ == "skill" else AGENTS
        src_sha = hashlib.sha256(f.read_bytes()).hexdigest()
        provenance = {"source": f"universal-agents/{rel}", "checksum": src_sha}

        # 1. copy YAML untouched (byte-identical)
        (base / "yaml" / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, base / "yaml" / rel)

        # 2. lossless JSON (mirror the source-relative path)
        wiring = wiring_map.get(str(doc["name"])) if typ == "agent" else None
        definition = build_definition(doc, typ, rel,
                                      wiring=wiring, wiring_src=args.wiring or "none",
                                      provenance=provenance)
        write_json(base / "json" / Path(rel).with_suffix(".json"), definition)

        # 3. workflow per agent
        if typ == "agent":
            params = extract_inputs(doc)
            skills = list(definition["skills"])
            wf = build_workflow(doc, str(doc["name"]), rel, skills, params, provenance=provenance)
            write_json(WORKFLOWS / Path(rel).with_name(f"{stem}.workflow.json"), wf)
            stats["workflows"] += 1

        # 4. optional in-place JSON: same path as the source YAML
        if args.inplace:
            write_json(Path(args.agents).resolve() / Path(rel).with_suffix(".json"), definition)

        if typ == "skill":
            stats["skills"] += 1
        else:
            stats["agents"] += 1

    print(f"Agents: {stats['agents']} | Skills: {stats['skills']} | Workflows: {stats['workflows']}")
    print(f"Errors: {len(stats['errors'])} | Warnings: {len(stats['warnings'])}")
    for w in stats["warnings"][:5]:
        print("  WARN:", w)
    for e in stats["errors"][:10]:
        print("  ERR:", e)


if __name__ == "__main__":
    main()