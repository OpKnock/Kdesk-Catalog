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


def _derive_tools(agent: Dict[str, Any], platform_config: Dict[str, Any]) -> list:
    """Derive Claude Code tools allowlist from capabilities, not hard-coded."""
    if "tools" in platform_config:
        return platform_config["tools"]
    # Derive from capabilities
    bins = set()
    for cap in agent.get("capabilities", []) or []:
        for cmd in cap.get("commands", []) or []:
            if isinstance(cmd, str) and cmd.strip():
                first = cmd.strip().split()[0].lstrip("$").lower()
                # Map shell binaries to Bash, keep file tools as is
                if first in ("curl", "kubectl", "helm", "git", "docker", "npm", "yarn", "pip", "python", "node", "go", "cargo", "promtool", "jq", "psql", "bash", "sh"):
                    bins.add("Bash")
                elif first in ("read", "grep", "glob", "write", "edit"):
                    bins.add(first.capitalize())
                else:
                    bins.add("Bash")
    if not bins:
        return ["Read", "Grep", "Glob", "Bash"]
    # Ensure core read tools for Read phase
    for core in ["Read", "Grep", "Glob"]:
        bins.add(core)
    # Keep deterministic order
    order = ["Read", "Grep", "Glob", "Bash", "Write", "Edit"]
    return [t for t in order if t in bins] + sorted(bins - set(order))


def _derive_permission_mode(agent: Dict[str, Any], tools: list) -> str:
    """Map risk to permissionMode."""
    # Check explicit platform config first
    pc = agent.get("platforms", {}).get("claude_code", {}).get("permissionMode")
    if pc:
        return pc
    # Infer from tools and capabilities
    has_write = "Write" in tools or "Edit" in tools
    has_bash = "Bash" in tools
    # Check for destructive commands
    destructive_kw = ("rm ", "sudo ", "docker ", "kubectl create", "aws iam", "terraform apply", "drop ", "delete ")
    has_destructive = any(any(kw in str(c.get("commands", [])) for kw in destructive_kw) for c in agent.get("capabilities", []) or [])
    if has_destructive:
        return "plan"
    if has_write and has_bash:
        return "default"
    return "default"


def _skill_frontmatter(agent: Dict[str, Any]) -> str:
    """Build official SKILL.md frontmatter (agentskills.io spec)."""
    slug = slugify(agent['name'])
    lines = ["---"]
    lines.append(f"name: {json.dumps(slug)}")
    lines.append(f"description: {json.dumps(desc_safe(agent))}")
    # Official fields: license (default MIT for portability)
    lic = agent.get("license") or "MIT"
    lines.append(f"license: {json.dumps(str(lic))}")
    # compatibility from prerequisites/tools
    prereqs = agent.get("prerequisites") or []
    tools = agent.get("tools") or []
    compat = ""
    if prereqs or tools:
        combined = prereqs + [t for t in tools if t not in prereqs]
        compat = f"Requires {', '.join(combined[:6])}."
        if any("curl" in str(c.get("commands", [])) or "kubectl" in str(c.get("commands", [])) for c in agent.get("capabilities", []) or []):
            compat += " Needs network access."
        compat = compat[:500]
        lines.append(f"compatibility: {json.dumps(compat)}")
    # metadata
    meta = {"author": str(agent.get("author", "Kdesk")), "version": str(agent.get("version", "1.0.0")), "category": str(agent.get("category", "general"))}
    lines.append(f"metadata: {json.dumps(meta)}")
    # allowed-tools from capabilities
    bins = set()
    for cap in agent.get("capabilities", []) or []:
        for cmd in cap.get("commands", []) or []:
            if isinstance(cmd, str) and cmd.strip():
                bins.add(cmd.strip().split()[0].lstrip("$"))
    if bins:
        allowed = []
        for b in sorted(bins):
            if b.lower() in ("read", "grep", "glob", "write", "edit"):
                allowed.append(b.capitalize())
            else:
                allowed.append(f"Bash({b}:*)")
        for core in ["Read", "Grep", "Glob"]:
            if core not in allowed:
                allowed.insert(0, core)
        lines.append(f"allowed-tools: {json.dumps(' '.join(allowed[:10]))}")
    lines.append("---")
    return "\n".join(lines)


def convert_to_claude_code(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Convert to Claude Code agent format - emits .md with YAML frontmatter.

    Official spec: .claude/agents/<name>.md (agents) and .claude/skills/<slug>/SKILL.md (skills)
    with Read-Reason-Act body and proper frontmatter (tools, model, permissionMode, skills).
    """
    rel = str(agent.get('file_path', '')).replace('\\', '/')
    is_skill = "/skill/" in rel or rel.endswith("-skill.yaml")

    # Build markdown body with Read-Reason-Act
    body = build_markdown(agent)

    platform_config = agent.get('platforms', {}).get('claude_code', {})
    # Default to inherit; only use specific model if explicitly overridden
    model = platform_config.get('model', "inherit")
    if model and ("2024" in str(model) or "2025" in str(model)):
        model = "inherit"

    if is_skill:
        # Skills: official SKILL.md (agentskills.io) — name must match dir
        slug = slugify(agent['name'])
        fm = _skill_frontmatter(agent)
        return {
            "name": agent['name'],
            "rel_path": f".claude/skills/{slug}/SKILL.md",
            "content": f"{fm}\n\n{body}\n"
        }
    else:
        # Agents: derive tools, permissionMode, skills preload
        tools = _derive_tools(agent, platform_config)
        perm = _derive_permission_mode(agent, tools)
        fm_lines = ["---"]
        fm_lines.append(f"name: {json.dumps(agent['name'])}")
        fm_lines.append(f"description: {json.dumps(desc_safe(agent))}")
        fm_lines.append(f"tools: {json.dumps(tools)}")
        fm_lines.append(f"model: {json.dumps(model)}")
        if perm != "default":
            fm_lines.append(f"permissionMode: {json.dumps(perm)}")
        # Preload sub-agent skills if agent delegates
        sub_agents = agent.get("sub_agents") or []
        if sub_agents:
            # skills frontmatter preloads sub-agent contexts
            fm_lines.append(f"skills: {json.dumps([slugify(s) for s in sub_agents[:5]])}")
        # Disallow Write for read-only agents
        if tools == ["Read", "Grep", "Glob"]:
            fm_lines.append(f"disallowedTools: {json.dumps(['Write', 'Edit', 'Bash'])}")
        fm_lines.append("---")
        fm = "\n".join(fm_lines)
        return {
            "name": agent['name'],
            "rel_path": f".claude/agents/{agent['name']}.md",
            "content": f"{fm}\n\n{body}\n"
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
