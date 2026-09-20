#!/usr/bin/env python3
"""
Universal Agent Converter
Converts universal YAML agents to platform-specific formats
"""
import os
import sys
import re
import yaml
import json
import argparse
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

QUIET = False

UNIVERSAL_DIR = Path("universal-agents")
OUTPUT_DIR = Path("platform-agents")

# Platform-specific schemas
PLATFORM_SCHEMAS = {
    "claude_code": {
        "required": ["name", "description", "tools", "model", "instructions", "examples"],
        "tool_map": {
            "Bash": "Bash",
            "Read": "Read",
            "Write": "Write",
            "Edit": "Edit",
            "Glob": "Glob",
            "Grep": "Grep",
            "Task": "Task",
            "WebFetch": "WebFetch",
            "WebSearch": "WebSearch"
        }
    },
    "cursor": {
        "required": ["name", "description", "rule_type", "model"],
        "rule_types": ["always", "auto", "agent"]
    },
    "github_copilot": {
        "required": ["name", "description", "prompt_file"],
        "prompt_template": """# {display_name}

{description}

## Capabilities
{capabilities}

## Commands
{commands}

## Examples
{examples}
"""
    },
    "windsurf": {
        "required": ["name", "description", "config"],
        "config_keys": ["model", "tools", "instructions"]
    },
    "opencode": {
        "required": ["name", "description", "plugin"],
        "plugin_schema": {
            "name": "string",
            "version": "string",
            "description": "string",
            "commands": "array"
        }
    },
    "generic": {
        "required": ["name", "description", "system_prompt", "available_tools"],
        "system_prompt_template": """You are {display_name}.

{description}

## Capabilities
{capabilities}

## Available Tools
{tools}

## Guidelines
{instructions}

## Examples
{examples}
"""
    }
}

# ---------------------------------------------------------------------------
# New platform families (2026 ecosystem). All emit per-file content that is
# copied into the platform's install path inside the project or home dir.
#
# NEW_SKILL_PLATFORMS: Agent Skills open standard (SKILL.md) - the universal
# skill format shared by 40+ tools. Emitted as <dir>/<slug>/SKILL.md.
# NEW_RULES_PLATFORMS: rules-directory format (<dir>/<slug>.md|.mdc).
# SPECIAL_PLATFORMS: distinctive native formats (Goose recipes YAML,
# Aider conventions markdown, OpenHands microagents).
# SINGLE_FILE_PLATFORMS: tools with one root instruction file (AGENTS.md,
# WARP.md, config.json registries) - per-item instruction files + manifest.
# ---------------------------------------------------------------------------
NEW_SKILL_PLATFORMS: Dict[str, str] = {
    "codex_cli": ".agents/skills",
    "gemini_cli": ".gemini/skills",
    "antigravity": ".agent/skills",
    "devin": ".devin/skills",
    "zed": ".agents/skills",
    "cline": ".clinerules/skills",
    "roo_code": ".roo/skills",
    "kilo_code": ".kilocode/skills",
    "trae": ".trae/skills",
    "qwen_code": ".qwen/skills",
    "kiro": ".kiro/skills",
    "junie": ".junie/skills",
    "zencoder": ".agents/skills",
    "amp": ".agents/skills",
    "factory_droid": ".factory/skills",
    "crush": ".crush/skills",
    "mcpjam": ".mcpjam/skills",
    "mux": ".mux/skills",
    "pi": ".pi/skills",
    "qoder": ".qoder/skills",
    "codebuddy": ".codebuddy/skills",
    "commandcode": ".commandcode/skills",
    "neovate": ".neovate/skills",
}

NEW_RULES_PLATFORMS: Dict[str, Tuple[str, str]] = {
    "grok_build": (".grok/rules", "plain"),
    "amazon_q": (".amazonq/rules", "plain"),
    "augment": (".augment/rules", "augment"),
    "firebase_studio": (".idx/rules", "mdc"),
    "continue": (".continue/rules", "continue"),
    "tabnine": (".tabnine/guidelines", "plain"),
    "supermaven": (".supermaven/rules", "plain"),
}

SPECIAL_PLATFORMS: Dict[str, str] = {
    "goose": "goose",
    "aider": "aider",
    "openhands": "openhands",
}

SINGLE_FILE_PLATFORMS: Dict[str, str] = {
    "google_jules": "AGENTS.md",
    "warp": "WARP.md",
    "codegpt": "AGENTS.md",
    "cody": ".vscode/cody.json",
    "firebender": "firebender.json",
}

# Deprecated tools with no documented agent-instructions file: fragments are
# still emitted for reference, but no native file is assembled.
DEPRECATED_SINGLE_FILE_PLATFORMS: Tuple[str, ...] = ("void",)

NEW_PLATFORMS: Tuple[str, ...] = (
    tuple(NEW_SKILL_PLATFORMS)
    + tuple(NEW_RULES_PLATFORMS)
    + tuple(SPECIAL_PLATFORMS)
    + tuple(SINGLE_FILE_PLATFORMS)
)

PLATFORM_INFO: Dict[str, Tuple[str, str, str]] = {
    "codex_cli": ("OpenAI Codex CLI", "SKILL.md (Agent Skills)", "Copy `.agents/skills/` into your repo root (scanned from CWD up to repo root) or `~/.agents/skills/` for personal skills."),
    "gemini_cli": ("Gemini CLI (Google)", "SKILL.md (Agent Skills)", "Copy `.gemini/skills/` into your repo root or `~/.gemini/skills/`."),
    "antigravity": ("Antigravity (Google)", "SKILL.md (Agent Skills)", "Copy `.agent/skills/` (singular) into your repo root or `~/.gemini/antigravity/skills/`."),
    "devin": ("Devin (Cognition)", "SKILL.md (Agent Skills)", "Copy `.devin/skills/` into your repo root or `~/.config/devin/skills/`."),
    "zed": ("Zed", "SKILL.md (Agent Skills)", "Copy `.agents/skills/` into your repo root or `~/.agents/skills/` (Zed also reads AGENTS.md)."),
    "cline": ("Cline", "SKILL.md (Agent Skills)", "Copy `.clinerules/skills/` into your repo root or `~/.cline/skills/` (also read from `.agents/skills/`)."),
    "roo_code": ("Roo Code", "SKILL.md (Agent Skills)", "Copy `.roo/skills/` into your repo root or `~/.roo/skills/`."),
    "kilo_code": ("Kilo Code", "SKILL.md (Agent Skills)", "Copy `.kilocode/skills/` into your repo root or `~/.kilocode/skills/`."),
    "trae": ("Trae (ByteDance)", "SKILL.md (Agent Skills)", "Copy `.trae/skills/` into your repo root."),
    "qwen_code": ("Qwen Code (Alibaba)", "SKILL.md (Agent Skills)", "Copy `.qwen/skills/` into your repo root or `~/.qwen/skills/`."),
    "kiro": ("Kiro (Sublime)", "SKILL.md (Agent Skills)", "Copy `.kiro/skills/` into your repo root or `~/.kiro/skills/`."),
    "junie": ("JetBrains Junie", "SKILL.md (Agent Skills)", "Copy `.junie/skills/` into your repo root."),
    "zencoder": ("Zencoder (Zenflow)", "SKILL.md (Agent Skills)", "Copy `.agents/skills/` into your repo root or `~/.agents/skills/` (Zencoder's recommended path)."),
    "amp": ("Amp (Sourcegraph)", "SKILL.md (Agent Skills)", "Copy `.agents/skills/` into your repo root or `~/.agents/skills/`."),
    "factory_droid": ("Factory Droid", "SKILL.md (Agent Skills)", "Copy `.factory/skills/` into your repo root or `~/.factory/skills/`."),
    "crush": ("Crush (Charm)", "SKILL.md (Agent Skills)", "Copy `.crush/skills/` into your repo root or `~/.crush/skills/`."),
    "mcpjam": ("MCPJam", "SKILL.md (Agent Skills)", "Copy `.mcpjam/skills/` into your repo root."),
    "mux": ("Mux", "SKILL.md (Agent Skills)", "Copy `.mux/skills/` into your repo root."),
    "pi": ("Pi", "SKILL.md (Agent Skills)", "Copy `.pi/skills/` into your repo root."),
    "qoder": ("Qoder", "SKILL.md (Agent Skills)", "Copy `.qoder/skills/` into your repo root."),
    "codebuddy": ("Tencent CodeBuddy", "SKILL.md (Agent Skills)", "Copy `.codebuddy/skills/` into your repo root."),
    "commandcode": ("Command Code", "SKILL.md (Agent Skills)", "Copy `.commandcode/skills/` into your repo root."),
    "neovate": ("Neovate", "SKILL.md (Agent Skills)", "Copy `.neovate/skills/` into your repo root."),
    "grok_build": ("Grok Build (xAI)", "Rules .md", "Copy `.grok/rules/` into your repo root or `~/.grok/rules/`. Grok also reads AGENTS.md/CLAUDE.md."),
    "amazon_q": ("Amazon Q Developer CLI (AWS)", "Rules .md", "Copy `.amazonq/rules/` into your repo root (recursive subdirectories allowed)."),
    "augment": ("Augment Code", "Rules .md (type: Always)", "Copy `.augment/rules/` into your repo root."),
    "firebase_studio": ("Firebase Studio (Google)", "Rules .mdc", "Copy `.idx/rules/` into your repo root."),
    "continue": ("Continue", "Rules .md (frontmatter)", "Copy `.continue/rules/` into your repo root or `~/.continue/rules/`."),
    "windsurf": ("Windsurf (Codeium)", "Rules .md (trigger frontmatter)", "Copy `.windsurf/rules/` into your repo root (workspace rules; 12,000-char limit per file). Legacy `.windsurfrules` is deprecated."),
    "opencode": ("OpenCode", "Agents .md + SKILL.md", "Copy `.opencode/agents/` into your repo root (scanned from CWD up to repo root; global copy to `~/.config/opencode/agent/`). Skills go to `.opencode/skills/`."),
    "goose": ("Goose (Block)", "Recipes YAML", "Copy `recipes/` into `~/.config/goose/recipes/` (or `.goose/recipes/` in your repo)."),
    "aider": ("Aider", "Conventions .md", "Load a file with `aider --read conventions/NAME.md` or add `read:` entries in `.aider.conf.yml`."),
    "openhands": ("OpenHands", "Microagents .md", "Copy `microagents/` into `.openhands/microagents/` in your repo root (type: knowledge + `triggers` = keyword-triggered; type: repo = always loaded)."),
    "google_jules": ("Google Jules", "AGENTS.md (single file)", "Merge any `instructions/*.md` file into your repo root `AGENTS.md`."),
    "warp": ("Warp AI", "WARP.md (single file)", "Merge any `instructions/*.md` file into your repo root `WARP.md`."),
    "void": ("Void (deprecated)", "Fragments only (⚠ unverified)", "No agent-instructions config documented: `.void/config.json` is the Void CLI OAuth token cache, not a rules file (voideditor/void is deprecated). Fragments kept for reference; native file is NOT assembled."),
    "cody": ("Sourcegraph Cody", "Custom Commands cody.json", "Assembled `.vscode/cody.json` exposes every instruction fragment as a `commands` entry (`description` + `prompt`); install in your repo's `.vscode/`."),
    "supermaven": ("Supermaven (Cursor)", "Rules .md", "Copy `.supermaven/rules/` into your repo root or `~/.supermaven/rules/` (plain markdown, per docs.supermaven.com)."),
    "codegpt": ("CodeGPT", "AGENTS.md (single file)", "CodeGPT documents project agent instructions via `AGENTS.md` at repo root (docs.codegpt.co). Assembled from `instructions/*.md`."),
    "tabnine": ("Tabnine", "Guidelines .md", "Copy `.tabnine/guidelines/` into your repo root or `~/.tabnine/guidelines/` (plain markdown, per docs.tabnine.com)."),
    "firebender": ("Firebender", "Agents .md + firebender.json", "Agent files go in `.firebender/agents/*.md` (YAML frontmatter: name/description); `firebender.json` indexes them under `agents`."),
}

ALL_PLATFORMS: List[str] = [
    "claude_code", "cursor", "github_copilot", "windsurf", "opencode", "generic",
] + list(NEW_PLATFORMS)

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
TOOLS_MANIFEST_PATH: Path = REPO_ROOT / "tools.json"

def load_tools_manifest(path: Path = TOOLS_MANIFEST_PATH) -> Dict[str, Any]:
    """Load the tools manifest (tools.json) describing every platform."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_tools_manifest(manifest: Optional[Dict[str, Any]] = None) -> List[str]:
    """Cross-check tools.json against ALL_PLATFORMS and the deprecated set.

    Returns a list of error strings (empty when the manifest is valid).
    """
    if manifest is None:
        manifest = load_tools_manifest()
    errors: List[str] = []
    tools = manifest.get("tools", {})
    expected = set(ALL_PLATFORMS) | set(DEPRECATED_SINGLE_FILE_PLATFORMS)
    missing = sorted(expected - set(tools))
    extra = sorted(set(tools) - expected)
    if missing:
        errors.append(f"tools.json missing platform entries: {', '.join(missing)}")
    if extra:
        errors.append(f"tools.json has unknown platform entries: {', '.join(extra)}")
    required = (
        "id", "label", "kebab", "accent", "icon", "order",
        "scope", "detect", "version", "format",
        "installKind", "slugFrom", "slugPrefix", "dest",
    )
    for key, entry in tools.items():
        if entry.get("id") != key:
            errors.append(f"{key}: id != manifest key")
        if entry.get("kebab") != key:
            errors.append(f"{key}: kebab != manifest key")
        for field in required:
            if field not in entry:
                errors.append(f"{key}: missing field '{field}'")
        dest = entry.get("dest", {})
        if "user" not in dest or "project" not in dest:
            errors.append(f"{key}: dest must have 'user' and 'project'")
        detect = entry.get("detect", {})
        if "dirs" not in detect or "agentsDir" not in detect:
            errors.append(f"{key}: detect must have 'dirs' and 'agentsDir'")
    return errors

def load_universal_agent(path: Path) -> Dict[str, Any]:
    """Load and validate a universal agent YAML"""
    with open(path, 'r', encoding='utf-8') as f:
        agent = yaml.safe_load(f)
    
    # Compute checksum
    content = path.read_bytes()
    agent['checksum'] = hashlib.sha256(content).hexdigest()[:16]
    agent['file_path'] = str(path)
    
    return agent

def get_all_universal_agents() -> List[Dict[str, Any]]:
    """Load all universal agents from directory"""
    agents = []
    for yaml_file in UNIVERSAL_DIR.rglob("*.yaml"):
        if yaml_file.name == "registry.yaml":
            continue
        try:
            agent = load_universal_agent(yaml_file)
            agents.append(agent)
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")
    return agents

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

def infer_globs(agent: Dict[str, Any]) -> List[str]:
    """Infer file globs from agent's capabilities and tags."""
    globs = set()
    text = " ".join([
        str(agent.get("description", "")),
        str(agent.get("instructions", "")),
        " ".join(cap.get("name", "") + " " + " ".join(cap.get("commands", []))
                 for cap in agent.get("capabilities", []))
    ]).lower()
    
    lang_globs = {
        "python": "**/*.py",
        "javascript": "**/*.{js,ts,jsx,tsx}",
        "typescript": "**/*.{ts,tsx}",
        "go": "**/*.go",
        "rust": "**/*.rs",
        "java": "**/*.java",
        "c++": "**/*.{cpp,cc,h,hpp}",
        "c#": "**/*.cs",
        "ruby": "**/*.rb",
        "php": "**/*.php",
        "swift": "**/*.swift",
        "kotlin": "**/*.kt",
        "scala": "**/*.scala",
        "r": "**/*.r",
        "julia": "**/*.jl",
        "shell": "**/*.sh",
        "bash": "**/*.sh",
        "dockerfile": "**/Dockerfile*",
        "terraform": "**/*.tf",
        "yaml": "**/*.{yaml,yml}",
        "json": "**/*.json",
        "sql": "**/*.sql",
        "html": "**/*.html",
        "css": "**/*.css",
    }
    
    for lang, glob in lang_globs.items():
        if lang in text:
            globs.add(glob)
    
    # Also check tags
    for tag in agent.get("tags", []):
        tag_lower = tag.lower()
        if tag_lower in lang_globs:
            globs.add(lang_globs[tag_lower])
    
    return sorted(globs)

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

# ---------------------------------------------------------------------------
# New platform emitters
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Lowercase alphanumeric + single hyphens, max 64 chars (SKILL.md spec)."""
    slug = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    return (slug[:64]).rstrip("-") or "skill"

def desc_safe(agent: Dict[str, Any]) -> str:
    """Flatten + truncate description for YAML frontmatter (max 1024 chars)."""
    d = " ".join(str(agent.get("description", "")).split())
    return d[:1024].rstrip(":- ")

def build_markdown(agent: Dict[str, Any]) -> str:
    """Shared agent/skill body: description + instructions + capabilities."""
    parts = [f"# {agent.get('display_name', agent['name'])}", "", str(agent.get("description", "")).strip()]
    instructions = str(agent.get("instructions", "")).strip()
    if instructions:
        parts += ["", "## Instructions", "", instructions]
    caps = agent.get("capabilities") or []
    if caps:
        parts += ["", "## Capabilities"]
        for cap in caps:
            if not isinstance(cap, dict):
                continue
            parts += ["", f"### {cap.get('name', '')}", str(cap.get("description", "")).strip()]
            cmds = cap.get("commands") or []
            if cmds:
                parts += ["", "**Commands:**"] + [f"- `{c}`" for c in cmds]
            exs = cap.get("examples") or []
            if exs:
                parts += ["", "**Examples:**"] + [f"- {e}" for e in exs]
    return "\n".join(parts)

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

def write_platform_meta(platform: str, output_dir: Path, counts: Dict[str, int]):
    """Write README.md (and manifest for single-file platforms)."""
    info = PLATFORM_INFO.get(platform)
    if not info:
        return
    name, fmt, install = info
    pd = output_dir / platform
    pd.mkdir(parents=True, exist_ok=True)
    total = counts.get('agents', 0) + counts.get('skills', 0)
    readme = (
        f"# {name} ({platform})\n\n"
        f"Format: {fmt}\n\n"
        f"## Install\n{install}\n\n"
        f"## Contents\n"
        f"- {counts.get('agents', 0)} agents\n"
        f"- {counts.get('skills', 0)} skills\n"
        f"- {total} files total\n\n"
        f"Generated by Kdesk-Catalog from `universal-agents/` (2,909 YAML definitions).\n"
    )
    (pd / "README.md").write_text(readme, encoding="utf-8")
    if platform in SINGLE_FILE_PLATFORMS or platform in DEPRECATED_SINGLE_FILE_PLATFORMS:
        files = sorted(pd.glob("instructions/*.md"))
        native = SINGLE_FILE_PLATFORMS.get(platform)
        if native:
            how_to = f"Pick the instruction file for the agent or skill you need and merge its contents into your {native} (or its rule registry)."
        else:
            how_to = "Deprecated: no documented agent-instructions file. Fragments are reference material; no native file is assembled."
        manifest = {
            "platform": platform,
            "native_file": native,
            "instruction_files": [f"instructions/{f.name}" for f in files],
            "how_to_use": how_to,
        }
        (pd / "manifest.yaml").write_text(
            yaml.safe_dump(manifest, default_flow_style=False, sort_keys=False,
                           allow_unicode=True, width=100),
            encoding="utf-8",
        )
    # Generate GitHub Copilot repo-wide index
    if platform == "github_copilot":
        write_copilot_index(pd, output_dir / platform)

def write_copilot_index(platform_dir: Path, output_dir: Path):
    """Generate curated .github/copilot-instructions.md repo-wide index."""
    instructions_dir = platform_dir / ".github" / "instructions"
    if not instructions_dir.exists():
        return
    
    items = []
    for f in sorted(instructions_dir.glob("*.instructions.md")):
        content = f.read_text(encoding="utf-8")
        name = f.stem
        desc = ""
        for line in content.split("\n"):
            if line.startswith("description:") or (line and not line.startswith("#") and not line.startswith("---")):
                desc = line.strip()
                if desc.startswith("description:"):
                    desc = desc.split(":", 1)[1].strip()
                break
        items.append((name, desc))
    
    parts = [
        "# GitHub Copilot Instructions — Kdesk-Catalog",
        "",
        "> Auto-generated index of all available agents and skills.",
        "> Copy the `.github/instructions/` directory into your repo to enable.",
        "",
        f"## Contents ({len(items)} items)",
        "",
    ]
    
    for name, desc in items:
        parts.append(f"- **{name}**: {desc[:120]}")
    
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("Generated by Kdesk-Catalog. See `platform-agents/github_copilot/.github/instructions/` for per-item files.")
    
    index_path = platform_dir / ".github" / "copilot-instructions.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"  [OK] github_copilot/.github/copilot-instructions.md ({len(items)} items)")

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

def save_agent(agent_data: Dict[str, Any], platform: str, output_dir: Path):
    """Save agent in platform-specific format; returns the written file path (or None)."""
    platform_dir = output_dir / platform
    platform_dir.mkdir(parents=True, exist_ok=True)
    
    if 'rel_path' in agent_data:
        file_path = platform_dir / agent_data['rel_path']
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(agent_data['content'])
        if not QUIET:
            print(f"  [OK] {platform}/{agent_data['rel_path']}")
        return file_path
    
    name = agent_data['name']
    
    if platform == "claude_code":
        file_path = platform_dir / f"{name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(agent_data, f, indent=2)
    elif platform == "github_copilot":
        file_path = platform_dir / agent_data['prompt_file']
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(agent_data['prompt'])
    elif platform == "generic":
        file_path = platform_dir / f"{name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(agent_data, f, indent=2)
    else:
        file_path = None
    
    if not QUIET:
        print(f"  [OK] {platform}/{name}")
    return file_path


def prune_platform_dir(platform: str, output_dir: Path, written: set) -> int:
    """Remove stale files in the platform dir that were not written this run.
    Meta files (README.md, manifest.yaml) are preserved. Returns count pruned."""
    platform_dir = output_dir / platform
    if not platform_dir.is_dir():
        return 0
    pruned = 0
    for f in sorted(platform_dir.rglob("*")):
        if f.is_file() and f.name not in ("README.md", "manifest.yaml"):
            if f.resolve().as_posix() not in written:
                try:
                    f.unlink()
                    pruned += 1
                except OSError:
                    pass
    for d in sorted(platform_dir.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            try:
                d.rmdir()
                pruned += 1
            except OSError:
                pass
    return pruned

def convert_all(platforms: List[str], output_dir: Path):
    """Convert all universal agents to specified platforms"""
    agents = get_all_universal_agents()
    print(f"Found {len(agents)} universal agents")
    
    converters = {
        "claude_code": convert_to_claude_code,
        "cursor": convert_to_cursor,
        "github_copilot": convert_to_copilot,
        "windsurf": convert_to_windsurf,
        "opencode": convert_to_opencode,
        "generic": convert_to_generic
    }
    
    for platform in platforms:
        print(f"\nConverting to {platform}...")
        counts = {"agents": 0, "skills": 0, "errors": 0}
        written: set[str] = set()
        
        for agent in agents:
            try:
                if platform in converters:
                    converted = converters[platform](agent)
                elif platform in NEW_PLATFORMS:
                    converted = convert_new_platform(platform, agent)
                else:
                    print(f"Unknown platform: {platform}")
                    break
                path = save_agent(converted, platform, output_dir)
                if path:
                    written.add(path.resolve().as_posix())
                rel = str(agent.get('file_path', '')).replace('\\', '/')
                if "/skill/" in rel or rel.endswith("-skill.yaml"):
                    counts['skills'] += 1
                else:
                    counts['agents'] += 1
            except Exception as e:
                counts['errors'] += 1
                print(f"  [ERR] {agent['name']}: {e}")
        
        pruned = prune_platform_dir(platform, output_dir, written)
        write_platform_meta(platform, output_dir, counts)
        print(f"  Done: {counts['agents']} agents, {counts['skills']} skills, "
              f"{counts['errors']} errors, {pruned} orphan files pruned")

def create_registry(agents: List[Dict[str, Any]], output_dir: Path):
    """Create registry.yaml for all agents"""
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat() + "Z",
        "total_agents": len(agents),
        "agents": []
    }
    
    for agent in agents:
        registry['agents'].append({
            "name": agent['name'],
            "display_name": agent.get('display_name', agent['name']),
            "category": agent.get('category', 'uncategorized'),
            "subcategory": agent.get('subcategory', ''),
            "description": agent['description'],
            "version": agent.get('version', '1.0.0'),
            "tags": agent.get('tags', []),
            "platforms": list(agent.get('platforms', {}).keys()),
            "checksum": agent.get('checksum', ''),
            "file_path": agent.get('file_path', '')
        })
    
    registry_path = output_dir / "registry.yaml"
    with open(registry_path, 'w', encoding='utf-8') as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)
    print(f"\nRegistry created: {registry_path}")

def validate_agents():
    """Validate all universal agents against schema"""
    agents = get_all_universal_agents()
    errors = []
    
    required_fields = ['name', 'display_name', 'category', 'description', 'version']
    
    for agent in agents:
        for field in required_fields:
            if field not in agent:
                errors.append(f"{agent.get('name', 'unknown')}: missing required field '{field}'")
        
        # Validate capabilities
        for i, cap in enumerate(agent.get('capabilities', [])):
            if 'name' not in cap:
                errors.append(f"{agent['name']}: capability {i} missing 'name'")
            if 'description' not in cap:
                errors.append(f"{agent['name']}: capability {cap.get('name', i)} missing 'description'")
    
    if errors:
        print("Validation errors:")
        for err in errors:
            print(f"  [ERR] {err}")
        return False
    
    print(f"[OK] All {len(agents)} agents validated successfully")
    return True

def parse_platforms(values) -> List[str]:
    """Split and validate --platforms values: comma- and/or space-separated, or 'all'.

    Returns the platform list; 'all' expands to every platform. Raises ValueError
    on unknown platform names.
    """
    platforms: List[str] = []
    for value in values:
        platforms.extend(p.strip() for p in value.split(",") if p.strip())
    unknown = [p for p in platforms if p not in ALL_PLATFORMS and p != "all"]
    if unknown:
        raise ValueError(f"unknown platform(s): {', '.join(unknown)}")
    if "all" in platforms:
        return list(ALL_PLATFORMS)
    return platforms

def main():
    parser = argparse.ArgumentParser(description="Universal Agent Converter")
    parser.add_argument("--platforms", "-p", nargs="+",
                       default=["all"],
                       help="Target platforms: comma-separated, space-separated, or 'all' "
                            "(e.g. --platforms claude_code,cursor,opencode)")
    parser.add_argument("--output", "-o", default="platform-agents", help="Output directory")
    parser.add_argument("--validate", action="store_true", help="Only validate agents")
    parser.add_argument("--registry", action="store_true", help="Generate registry")
    parser.add_argument("--universal-dir", default="universal-agents", help="Universal agents directory")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-file output")
    
    args = parser.parse_args()
    
    global UNIVERSAL_DIR, QUIET
    UNIVERSAL_DIR = Path(args.universal_dir)
    QUIET = args.quiet
    output_dir = Path(args.output)
    
    if args.validate:
        validate_agents()
        return
    
    try:
        platforms = parse_platforms(args.platforms)
    except ValueError as e:
        parser.error(f"{e} (choices: {', '.join(ALL_PLATFORMS + ['all'])})")
    
    manifest_errors = validate_tools_manifest()
    if manifest_errors:
        print("tools.json validation failed:")
        for err in manifest_errors:
            print(f"  [ERR] {err}")
        sys.exit(2)
    
    agents = get_all_universal_agents()
    print(f"Loaded {len(agents)} universal agents")
    
    if args.registry:
        create_registry(agents, Path(args.output))
    
    convert_all(platforms, output_dir)
    
    print(f"\n[OK] Conversion complete! Output: {output_dir}")

if __name__ == "__main__":
    main()