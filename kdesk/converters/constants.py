"""Converter constants: platform schemas, families, and paths."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

QUIET = False

UNIVERSAL_DIR = Path("universal-agents")
OUTPUT_DIR = Path("platform-agents")

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
TOOLS_MANIFEST_PATH: Path = REPO_ROOT / "tools.json"

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
    "claude_code": ".claude/skills",
    "cursor": ".cursor/rules",
    "windsurf": ".windsurf/rules",
    "github_copilot": ".github/instructions",
    "opencode": ".opencode/skills",
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
    "void": ("Void (deprecated)", "Fragments only (\u26a0 unverified)", "No agent-instructions config documented: `.void/config.json` is the Void CLI OAuth token cache, not a rules file (voideditor/void is deprecated). Fragments kept for reference; native file is NOT assembled."),
    "cody": ("Sourcegraph Cody", "Custom Commands cody.json", "Assembled `.vscode/cody.json` exposes every instruction fragment as a `commands` entry (`description` + `prompt`); install in your repo's `.vscode/`."),
    "supermaven": ("Supermaven (Cursor)", "Rules .md", "Copy `.supermaven/rules/` into your repo root or `~/.supermaven/rules/` (plain markdown, per docs.supermaven.com)."),
    "codegpt": ("CodeGPT", "AGENTS.md (single file)", "CodeGPT documents project agent instructions via `AGENTS.md` at repo root (docs.codegpt.co). Assembled from `instructions/*.md`."),
    "tabnine": ("Tabnine", "Guidelines .md", "Copy `.tabnine/guidelines/` into your repo root or `~/.tabnine/guidelines/` (plain markdown, per docs.tabnine.com)."),
    "firebender": ("Firebender", "Agents .md + firebender.json", "Agent files go in `.firebender/agents/*.md` (YAML frontmatter: name/description); `firebender.json` indexes them under `agents`."),
}

ALL_PLATFORMS: List[str] = [
    "claude_code", "cursor", "github_copilot", "windsurf", "opencode", "generic",
] + list(NEW_PLATFORMS)
