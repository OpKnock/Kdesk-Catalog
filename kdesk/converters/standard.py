"""Open-standard emitters (SKILL.md, rules, goose, aider, openhands, singlefile)."""
from __future__ import annotations

import json
from typing import Any, Dict, List

import yaml

from kdesk.converters.constants import (
    DEPRECATED_SINGLE_FILE_PLATFORMS,
    NEW_RULES_PLATFORMS,
    NEW_SKILL_PLATFORMS,
    SINGLE_FILE_PLATFORMS,
)
from kdesk.converters.shared import (
    build_markdown,
    desc_safe,
    infer_globs,
    slugify,
)


def convert_to_skill_md(agent: Dict[str, Any], skills_dir: str) -> Dict[str, Any]:
    """Agent Skills standard (SKILL.md) - read by 40+ tools."""
    slug = slugify(agent['name'])
    content = f"---\nname: {json.dumps(slug)}\ndescription: {json.dumps(desc_safe(agent))}\n---\n\n{build_markdown(agent)}\n"
    return {"name": agent['name'], "rel_path": f"{skills_dir}/{slug}/SKILL.md", "content": content}


def convert_to_rules_md(agent: Dict[str, Any], rules_dir: str, kind: str) -> Dict[str, Any]:
    """Rules-directory markdown (plain or with platform frontmatter)."""
    slug = slugify(agent['name'])
    d = json.dumps(desc_safe(agent))
    body = build_markdown(agent)
    if kind == "continue":
        globs = infer_globs(agent)
        head = f"---\nname: {json.dumps(agent.get('display_name', agent['name']))}\ndescription: {d}\nglobs: {json.dumps(globs)}\nalwaysApply: false\n---\n\n"
    elif kind == "augment":
        head = f"---\ntype: agent_requested\ndescription: {d}\n---\n\n"
    elif kind == "mdc":
        globs = infer_globs(agent)
        head = f"---\ndescription: {d}\nglobs: {json.dumps(globs)}\nalwaysApply: false\n---\n\n"
    else:
        head = ""
    ext = "mdc" if kind == "mdc" else "md"
    return {"name": agent['name'], "rel_path": f"{rules_dir}/{slug}.{ext}", "content": head + body}


def convert_to_goose_recipe(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Goose recipe YAML (~/.config/goose/recipes/, .goose/recipes/).

    Verified spec (block/goose recipe-reference): title + description are
    REQUIRED, plus at least one of instructions/prompt (prompt is REQUIRED
    for headless/CLI mode). Optional: version, activities, extensions,
    parameters, settings, response, retry, sub_recipes.
    """
    slug = slugify(agent['name'])
    recipe = {
        "title": agent.get('display_name', agent['name']),
        "description": str(agent.get("description", "")).strip(),
        "version": str(agent.get('version', '1.0.0')),
        "instructions": build_markdown(agent),
        "prompt": f"Act as {agent.get('display_name', agent['name'])} and handle the task per the instructions.",
    }
    content = yaml.safe_dump(recipe, default_flow_style=False, sort_keys=False,
                             allow_unicode=True, width=100)
    return {"name": agent['name'], "rel_path": f"recipes/{slug}.yaml", "content": content}


def convert_to_aider_convention(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Aider convention markdown (loaded via --read / read: in .aider.conf.yml)."""
    slug = slugify(agent['name'])
    return {"name": agent['name'], "rel_path": f"conventions/{slug}.md",
            "content": build_markdown(agent) + "\n"}


def openhands_triggers(agent: Dict[str, Any]) -> List[str]:
    """Keyword triggers for OpenHands knowledge microagents: the agent's name
    plus its capability names (distinctive, avoids generic false activations)."""
    trigs = [agent['name']]
    for cap in agent.get('capabilities') or []:
        if not isinstance(cap, dict):
            continue
        t = str(cap.get('name', '')).strip().lower()
        if t and t not in trigs:
            trigs.append(t)
    return trigs[:10]


def convert_to_openhands_microagent(agent: Dict[str, Any]) -> Dict[str, Any]:
    """OpenHands microagent (.openhands/microagents/).

    Verified spec (OpenHands docs + microagent/types.py): type is
    repo (always-on), knowledge (keyword-triggered via `triggers`), or task.
    `triggers` only applies to knowledge-type. Specialized agents are
    emitted as knowledge + triggers so they don't occupy context always;
    fall back to repo only if no capabilities exist to derive triggers from.
    """
    slug = slugify(agent['name'])
    trigs = openhands_triggers(agent)
    if trigs:
        content = (f"---\nname: {json.dumps(slug)}\ndescription: {json.dumps(desc_safe(agent))}\n"
                   f"type: knowledge\ntriggers: {json.dumps(trigs)}\n---\n\n{build_markdown(agent)}\n")
    else:
        content = (f"---\nname: {json.dumps(slug)}\ndescription: {json.dumps(desc_safe(agent))}\n"
                   f"type: repo\n---\n\n{build_markdown(agent)}\n")
    return {"name": agent['name'], "rel_path": f"microagents/{slug}.md", "content": content}


def convert_to_singlefile(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Per-item instruction file for single-root-file platforms."""
    slug = slugify(agent['name'])
    return {"name": agent['name'], "rel_path": f"instructions/{slug}.md",
            "content": build_markdown(agent) + "\n"}


def convert_new_platform(platform: str, agent: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch one agent/skill to the right new-platform emitter."""
    if platform in NEW_SKILL_PLATFORMS:
        return convert_to_skill_md(agent, NEW_SKILL_PLATFORMS[platform])
    if platform in NEW_RULES_PLATFORMS:
        rdir, kind = NEW_RULES_PLATFORMS[platform]
        return convert_to_rules_md(agent, rdir, kind)
    if platform == "goose":
        return convert_to_goose_recipe(agent)
    if platform == "aider":
        return convert_to_aider_convention(agent)
    if platform == "openhands":
        return convert_to_openhands_microagent(agent)
    if platform in SINGLE_FILE_PLATFORMS or platform in DEPRECATED_SINGLE_FILE_PLATFORMS:
        return convert_to_singlefile(agent)
    raise ValueError(f"Unknown new platform: {platform}")
