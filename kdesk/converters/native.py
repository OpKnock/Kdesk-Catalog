"""Native-format converters (claude_code, cursor, copilot, windsurf, opencode, generic)."""
from __future__ import annotations

import json
from typing import Any, Dict, List

from kdesk.converters.constants import PLATFORM_SCHEMAS
from kdesk.converters.shared import (
    build_markdown,
    desc_safe,
    infer_globs,
    slugify,
)


def convert_to_claude_code(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Convert to Claude Code agent format - emits .md with YAML frontmatter."""
    rel = str(agent.get('file_path', '')).replace('\\', '/')
    is_skill = "/skill/" in rel or rel.endswith("-skill.yaml")

    # Build markdown body (shared with skill emitter)
    body = build_markdown(agent)

    platform_config = agent.get('platforms', {}).get('claude_code', {})
    tools = platform_config.get('tools', ["Bash", "Read", "Write", "Edit", "Glob", "Grep"])
    # Default to inherit; only use specific model if explicitly overridden in source
    model = platform_config.get('model', "inherit")
    if model and "2024" in model or "2025" in model:  # stale dated snapshot
        model = "inherit"

    if is_skill:
        # Skills go to .claude/skills/<slug>/SKILL.md using Agent Skills standard
        slug = slugify(agent['name'])
        return {
            "name": agent['name'],
            "rel_path": f".claude/skills/{slug}/SKILL.md",
            "content": f"---\nname: {json.dumps(slug)}\ndescription: {json.dumps(desc_safe(agent))}\n---\n\n{body}\n"
        }
    else:
        # Agents go to .claude/agents/<name>.md with frontmatter
        return {
            "name": agent['name'],
            "rel_path": f".claude/agents/{agent['name']}.md",
            "content": f"---\nname: {json.dumps(agent['name'])}\ndescription: {json.dumps(desc_safe(agent))}\ntools: {json.dumps(tools)}\nmodel: {json.dumps(model)}\n---\n\n{body}\n"
        }


def convert_to_cursor(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Convert to Cursor rule format with correct .mdc frontmatter."""
    globs = infer_globs(agent)

    content = build_markdown(agent)

    return {
        "name": agent['name'],
        "rel_path": f"{agent['name']}.mdc",
        "content": f"---\ndescription: {json.dumps(desc_safe(agent))}\nglobs: {json.dumps(globs)}\nalwaysApply: false\n---\n\n{content}\n"
    }


def convert_to_copilot(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Convert to GitHub Copilot instructions format (.instructions.md with applyTo)."""
    globs = infer_globs(agent)
    apply_to = " ".join(globs) if globs else "**"

    body = build_markdown(agent)

    return {
        "name": agent['name'],
        "rel_path": f".github/instructions/{agent['name']}.instructions.md",
        "content": f"---\napplyTo: {json.dumps(apply_to)}\n---\n\n{body}\n"
    }


def convert_to_windsurf(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Windsurf rules (.windsurf/rules/*.md, Wave 8+).

    Verified spec (2026): Markdown files with YAML frontmatter; `trigger` is
    REQUIRED (always_on | model_decision | glob | manual), `description` is
    always shown to Cascade, and `globs` is required when trigger is glob.
    Workspace rule files are capped at 12,000 chars. There is no JSON config
    and no `model` field in the rules format.
    """
    slug = slugify(agent['name'])
    d = json.dumps(desc_safe(agent))
    globs = infer_globs(agent)
    if globs:
        head = f"---\ntrigger: glob\ndescription: {d}\nglobs: {json.dumps(globs)}\n---\n\n"
    else:
        head = f"---\ntrigger: model_decision\ndescription: {d}\n---\n\n"
    content = head + build_markdown(agent) + "\n"
    if len(content) > 11900:
        content = content[:11900].rstrip() + "\n"
    return {"name": agent['name'], "rel_path": f".windsurf/rules/{slug}.md", "content": content}


def convert_to_opencode(agent: Dict[str, Any]) -> Dict[str, Any]:
    """OpenCode agents (.opencode/agent(s)/<name>.md, YAML frontmatter).

    Verified spec (opencode.ai, 2026): agents are Markdown files with
    frontmatter (description, mode: primary|subagent|all, model must be
    provider-prefixed if set; body = the agent's prompt). There is no JSON
    plugin manifest for agents - plugins are .ts/.js modules. Skill items
    route to .opencode/skills/<slug>/SKILL.md (Agent Skills standard, which
    opencode loads natively).
    """
    rel = str(agent.get('file_path', '')).replace('\\', '/')
    is_skill = "/skill/" in rel or rel.endswith("-skill.yaml")
    if is_skill:
        slug = slugify(agent['name'])
        return {
            "name": agent['name'],
            "rel_path": f".opencode/skills/{slug}/SKILL.md",
            "content": f"---\nname: {json.dumps(slug)}\ndescription: {json.dumps(desc_safe(agent))}\n---\n\n{build_markdown(agent)}\n"
        }
    content = f"---\nname: {json.dumps(agent['name'])}\ndescription: {json.dumps(desc_safe(agent))}\nmode: subagent\n---\n\n{build_markdown(agent)}\n"
    return {"name": agent['name'], "rel_path": f".opencode/agents/{agent['name']}.md", "content": content}


def convert_to_generic(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Convert to generic system prompt format"""
    platform_config = agent.get('platforms', {}).get('generic', {})
    tools = platform_config.get('available_tools', ['bash', 'read', 'write', 'edit', 'glob', 'grep'])
    system_prompt_template = platform_config.get('system_prompt_template', PLATFORM_SCHEMAS['generic']['system_prompt_template'])

    capabilities_md = "\n".join([
        f"- **{cap['name']}**: {cap['description']}"
        for cap in agent.get('capabilities', [])
    ])

    examples_md = "\n".join([
        f"- {ex}"
        for cap in agent.get('capabilities', [])
        for ex in cap.get('examples', [])
    ])

    system_prompt = system_prompt_template.format(
        display_name=agent.get('display_name', agent['name']),
        description=agent['description'],
        capabilities=capabilities_md,
        tools=", ".join(tools),
        instructions=agent.get('instructions', 'Follow best practices.'),
        examples=examples_md
    )

    return {
        "name": agent['name'],
        "description": agent['description'],
        "system_prompt": system_prompt,
        "available_tools": tools,
        "capabilities": agent.get('capabilities', []),
        "examples": agent.get('examples', [])
    }
