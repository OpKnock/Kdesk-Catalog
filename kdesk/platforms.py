"""Canonical platform registry — single source of truth for all platform metadata.

Every other module (adapters, scanner, compatibility, converter, installer)
must derive platform facts from this registry rather than defining their own.

Usage:
    from kdesk.platforms import PlatformRegistry, PlatformSpec

    registry = PlatformRegistry.load()
    cursor = registry.get("cursor")
    print(cursor.display_name)   # "Cursor"
    print(cursor.detect_dirs)    # [".cursor/rules"]
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class SupportLevel(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    EXPERIMENTAL = "experimental"
    UNVERIFIED = "unverified"
    DEPRECATED = "deprecated"


@dataclass(frozen=True)
class PlatformSpec:
    """Immutable platform specification."""
    id: str
    display_name: str
    family: str                    # legacy-core, skill-md, rules, special, single-file, deprecated
    support_level: SupportLevel
    agent_format: str              # ".md", ".mdc", ".instructions.md", etc.
    skill_format: str              # "SKILL.md", ".mdc", "", etc.
    project_paths: List[str]       # where files go in a project
    global_paths: List[str]        # where files go globally (~)
    detect_dirs: List[str]         # directories that indicate this platform is active
    frontmatter_required: List[str]
    supported_fields: List[str]
    unsupported_fields: List[str]
    max_file_size: int             # bytes; 0 = unlimited
    install_kind: str              # "roster", "per-agent", "none"
    slug_from: str                 # "filename" | "dirname"
    deprecation_reason: str = ""
    replacement: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "display_name": self.display_name,
            "family": self.family,
            "support_level": self.support_level.value,
            "agent_format": self.agent_format,
            "skill_format": self.skill_format,
            "project_paths": self.project_paths,
            "global_paths": self.global_paths,
            "detect_dirs": self.detect_dirs,
            "frontmatter_required": self.frontmatter_required,
            "supported_fields": self.supported_fields,
            "unsupported_fields": self.unsupported_fields,
            "max_file_size": self.max_file_size,
            "install_kind": self.install_kind,
            "slug_from": self.slug_from,
            "deprecation_reason": self.deprecation_reason,
            "replacement": self.replacement,
        }


def _p(
    id: str,
    display: str,
    family: str,
    level: SupportLevel = SupportLevel.FULL,
    agent_fmt: str = "",
    skill_fmt: str = "",
    project: List[str] = None,
    global_: List[str] = None,
    detect: List[str] = None,
    fm_req: List[str] = None,
    supported: List[str] = None,
    unsupported: List[str] = None,
    max_size: int = 100000,
    install_kind: str = "roster",
    slug_from: str = "filename",
    **kw,
) -> PlatformSpec:
    return PlatformSpec(
        id=id,
        display_name=display,
        family=family,
        support_level=level,
        agent_format=agent_fmt,
        skill_format=skill_fmt,
        project_paths=project or [],
        global_paths=global_ or [],
        detect_dirs=detect or [],
        frontmatter_required=fm_req or [],
        supported_fields=supported or [],
        unsupported_fields=unsupported or [],
        max_file_size=max_size,
        install_kind=install_kind,
        slug_from=slug_from,
        **kw,
    )


_REGISTRY: Dict[str, PlatformSpec] = {}


def _reg(spec: PlatformSpec):
    _REGISTRY[spec.id] = spec


# ─── legacy core (6) ─────────────────────────────────────────────────────────

_reg(_p("claude_code", "Claude Code", "legacy-core",
    agent_fmt=".md", skill_fmt="SKILL.md",
    project=[".claude/agents/", ".claude/skills/"],
    global_=["~/.claude/agents/", "~/.claude/skills/"],
    detect=[".claude/agents", ".claude/skills"],
    fm_req=["name", "description"],
    supported=["name", "description", "tools", "instructions", "examples", "system_prompt"],
))

_reg(_p("cursor", "Cursor", "rules",
    agent_fmt=".mdc",
    project=[".cursor/rules/"],
    global_=["~/.cursor/rules/"],
    detect=[".cursor/rules"],
    fm_req=["description"],
    supported=["description", "globs", "alwaysApply"],
    unsupported=["model", "tools", "name"],
    max_size=50000,
))

_reg(_p("github_copilot", "GitHub Copilot", "rules",
    agent_fmt=".instructions.md",
    project=[".github/instructions/"],
    detect=[".github/instructions"],
    fm_req=["applyTo"],
    supported=["applyTo", "description"],
    unsupported=["model", "tools", "name"],
))

_reg(_p("windsurf", "Windsurf", "rules",
    agent_fmt=".md",
    project=[".windsurf/rules/"],
    global_=["~/.windsurf/rules/"],
    detect=[".windsurf/rules"],
    fm_req=["trigger", "description"],
    supported=["trigger", "description", "globs", "alwaysApply"],
    unsupported=["model", "tools", "name"],
    max_size=12000,
))

_reg(_p("opencode", "OpenCode", "legacy-core",
    agent_fmt=".md", skill_fmt="SKILL.md",
    project=[".opencode/agents/", ".opencode/skills/"],
    detect=[".opencode/agents", ".opencode/skills"],
    fm_req=["name", "description", "mode"],
    supported=["name", "description", "mode", "model", "instructions", "examples", "tools"],
))

_reg(_p("generic", "Generic", "legacy-core",
    agent_fmt=".json",
    install_kind="per-agent",
    supported=["*"],
))

# ─── Agent Skills / SKILL.md (23) ────────────────────────────────────────────

_SKILL_PLATFORMS = [
    ("codex_cli", "OpenAI Codex CLI"),
    ("gemini_cli", "Gemini CLI (Google)"),
    ("antigravity", "Antigravity (Google)", ".agent/skills/"),
    ("devin", "Devin (Cognition)", ".devin/skills/"),
    ("zed", "Zed", ".agents/skills/"),
    ("cline", "Cline", ".clinerules/skills/"),
    ("roo_code", "Roo Code", ".roo/skills/"),
    ("kilo_code", "Kilo Code", ".kilocode/skills/"),
    ("trae", "Trae (ByteDance)", ".trae/skills/"),
    ("qwen_code", "Qwen Code (Alibaba)", ".qwen/skills/"),
    ("kiro", "Kiro (Sublime)", ".kiro/skills/"),
    ("junie", "JetBrains Junie", ".junie/skills/"),
    ("zencoder", "Zencoder", ".agents/skills/"),
    ("amp", "Amp (Sourcegraph)", ".agents/skills/"),
    ("factory_droid", "Factory Droid", ".factory/skills/"),
    ("crush", "Crush (Charm)", ".crush/skills/"),
    ("mcpjam", "MCPJam", ".mcpjam/skills/"),
    ("mux", "Mux", ".mux/skills/"),
    ("pi", "Pi", ".pi/skills/"),
    ("qoder", "Qoder", ".qoder/skills/"),
    ("codebuddy", "Tencent CodeBuddy", ".codebuddy/skills/"),
    ("commandcode", "Command Code", ".commandcode/skills/"),
    ("neovate", "Neovate", ".neovate/skills/"),
]

for entry in _SKILL_PLATFORMS:
    pid, display = entry[0], entry[1]
    proj_dir = entry[2] if len(entry) > 2 else f".{pid}/skills/"
    _reg(_p(pid, display, "skill-md",
        skill_fmt="SKILL.md",
        project=[proj_dir],
        detect=[proj_dir.rstrip("/")],
        fm_req=["name", "description"],
        supported=["name", "description", "instructions", "examples"],
    ))

# ─── Rules-based (7) ────────────────────────────────────────────────────────

_reg(_p("grok_build", "Grok Build (xAI)", "rules",
    agent_fmt=".md",
    project=[".grok/rules/"], global_=["~/.grok/rules/"],
    detect=[".grok/rules"],
))
_reg(_p("amazon_q", "Amazon Q Developer CLI (AWS)", "rules",
    agent_fmt=".md",
    project=[".amazonq/rules/"],
    detect=[".amazonq/rules"],
))
_reg(_p("augment", "Augment Code", "rules",
    agent_fmt=".md",
    project=[".augment/rules/"],
    detect=[".augment/rules"],
))
_reg(_p("firebase_studio", "Firebase Studio (Google)", "rules",
    agent_fmt=".mdc",
    project=[".idx/rules/"],
    detect=[".idx/rules"],
))
_reg(_p("continue", "Continue", "rules",
    agent_fmt=".md",
    project=[".continue/rules/"], global_=["~/.continue/rules/"],
    detect=[".continue/rules"],
))
_reg(_p("tabnine", "Tabnine", "rules",
    agent_fmt=".md",
    project=[".tabnine/guidelines/"], global_=["~/.tabnine/guidelines/"],
    detect=[".tabnine/guidelines"],
))
_reg(_p("supermaven", "Supermaven", "rules",
    agent_fmt=".md",
    project=[".supermaven/rules/"], global_=["~/.supermaven/rules/"],
    detect=[".supermaven/rules"],
))

# ─── Special (3) ────────────────────────────────────────────────────────────

_reg(_p("goose", "Goose (Block)", "special",
    agent_fmt=".yaml",
    project=[".goose/recipes/"], global_=["~/.config/goose/recipes/"],
    detect=[".goose/recipes", "recipes"],
))
_reg(_p("aider", "Aider", "special",
    agent_fmt=".md",
    project=["conventions/"],
    detect=["conventions"],
))
_reg(_p("openhands", "OpenHands", "special",
    agent_fmt=".md",
    project=[".openhands/microagents/"],
    detect=[".openhands/microagents"],
))

# ─── Single-file (5) ─────────────────────────────────────────────────────────

for pid, display in [("google_jules", "Google Jules"), ("warp", "Warp AI"), ("codegpt", "CodeGPT")]:
    fname = "WARP.md" if pid == "warp" else "AGENTS.md"
    level = SupportLevel.PARTIAL if pid == "codegpt" else SupportLevel.FULL
    _reg(_p(pid, display, "single-file",
        level=level,
        agent_fmt=".md",
        project=[fname],
        install_kind="per-agent",
    ))

_reg(_p("cody", "Sourcegraph Cody", "single-file",
    level=SupportLevel.PARTIAL,
    agent_fmt=".json",
    project=[".vscode/cody.json"],
    install_kind="per-agent",
))
_reg(_p("firebender", "Firebender", "single-file",
    level=SupportLevel.PARTIAL,
    agent_fmt=".json",
    project=[".firebender/"],
    install_kind="per-agent",
))

# ─── Deprecated (1) ──────────────────────────────────────────────────────────

_reg(_p("void", "Void (deprecated)", "deprecated",
    level=SupportLevel.DEPRECATED,
    deprecation_reason="Platform discontinued",
))


class PlatformRegistry:
    """Canonical platform registry. Load once, query anywhere."""

    _instance: Optional["PlatformRegistry"] = None

    def __init__(self):
        self._platforms = dict(_REGISTRY)

    @classmethod
    def load(cls) -> "PlatformRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get(self, platform_id: str) -> Optional[PlatformSpec]:
        return self._platforms.get(platform_id)

    def all(self) -> List[PlatformSpec]:
        return sorted(self._platforms.values(), key=lambda p: p.id)

    def ids(self) -> List[str]:
        return sorted(self._platforms.keys())

    def by_family(self, family: str) -> List[PlatformSpec]:
        return [p for p in self._platforms.values() if p.family == family]

    def active(self) -> List[PlatformSpec]:
        """Platforms that are not deprecated."""
        return [p for p in self._platforms.values()
                if p.support_level != SupportLevel.DEPRECATED]

    def detect(self, root: Path) -> List[PlatformSpec]:
        """Detect which platforms have config dirs under root."""
        found = []
        for spec in self._platforms.values():
            for d in spec.detect_dirs:
                if (root / d).is_dir():
                    found.append(spec)
                    break
        return found

    def validate_unique(self) -> List[str]:
        """Assert no duplicate IDs exist."""
        errors = []
        seen = set()
        for pid in self._platforms:
            if pid in seen:
                errors.append(f"duplicate platform ID: {pid}")
            seen.add(pid)
        return errors

    def summary(self) -> Dict[str, Any]:
        families = {}
        levels = {}
        for p in self._platforms.values():
            families[p.family] = families.get(p.family, 0) + 1
            levels[p.support_level.value] = levels.get(p.support_level.value, 0) + 1
        return {
            "total_platforms": len(self._platforms),
            "families": families,
            "support_levels": levels,
        }

    def to_json(self, path: Path) -> None:
        data = {pid: spec.to_dict() for pid, spec in sorted(self._platforms.items())}
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def compatibility_matrix(self) -> Dict[str, Dict[str, str]]:
        """Generate platform × feature compatibility matrix."""
        matrix = {}
        features = ["frontmatter", "tools", "instructions", "examples", "parameters", "sub_agents"]
        for spec in self._platforms.values():
            row = {}
            for feat in features:
                if feat == "frontmatter":
                    row[feat] = "supported" if spec.frontmatter_required else "n/a"
                elif feat == "tools":
                    row[feat] = "supported" if "tools" in spec.supported_fields else "transformed"
                elif feat in ("instructions", "examples"):
                    row[feat] = "supported" if feat in spec.supported_fields else "embedded"
                elif feat == "parameters":
                    row[feat] = "supported" if spec.agent_format in (".md", ".json") else "transformed"
                elif feat == "sub_agents":
                    row[feat] = "unsupported" if spec.family == "deprecated" else "transformed"
            matrix[spec.id] = row
        return matrix


# Module-level convenience
def get_registry() -> PlatformRegistry:
    return PlatformRegistry.load()
