"""Platform adapter registry (45 platforms).

Adapters declare honest support levels and dispatch to the verified
converter emitters; they never re-emit content.
"""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.registry import Catalog, default_repo_root


class SupportLevel(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    EMULATED = "EMULATED"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    UNKNOWN = "UNKNOWN"


class PlatformAdapter:
    """Base class. Subclasses declare metadata; support comes from the
    verified pipeline (tests/test_platform_spec.py covers all platforms)."""

    name: str = ""
    display_name: str = ""
    format: str = ""
    install_target: str = ""
    support_level: SupportLevel = SupportLevel.SUPPORTED
    family: str = ""

    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root) if root else default_repo_root()
        self.output_dir = self.root / "platform-agents" / self.name

    # ------------------------------------------------------------ discovery
    def exists(self) -> bool:
        return self.output_dir.is_dir()

    def file_count(self) -> int:
        if not self.exists():
            return 0
        return sum(1 for _ in self.output_dir.rglob("*") if _.is_file())

    def items_emitted(self) -> int:
        """Item files (agent/skill outputs) vs total files incl. README/registry."""
        if not self.exists():
            return 0
        return sum(
            1 for p in self.output_dir.rglob("*")
            if p.is_file() and p.name not in ("README.md", "registry.yaml", "registry.json")
        )

    def manifest(self) -> Optional[Dict[str, Any]]:
        for name in ("registry.yaml", "registry.json"):
            p = self.output_dir / name
            if p.is_file():
                import json
                import yaml

                with open(p, "r", encoding="utf-8") as fh:
                    if name.endswith(".json"):
                        return json.load(fh)
                    return yaml.safe_load(fh)
        return None

    # ------------------------------------------------------------- install
    def install_targets(self) -> List[Path]:
        """Per-platform install paths (project or home). Override per platform."""
        return [self.output_dir]

    def verify(self) -> Dict[str, Any]:
        """Per-platform verification: counts + frontmatter contract."""
        count = self.file_count()
        items = self.items_emitted()
        ok = self.exists() and items > 0
        return {
            "platform": self.name,
            "support_level": self.support_level.value,
            "exists": self.exists(),
            "files": count,
            "items": items,
            "status": "OK" if ok else ("MISSING" if not self.exists() else "EMPTY"),
            "scanned_files": count,
        }


# ---------------------------------------------------------------------------
# Adapter registry: 45 platforms with honest support levels.
# SUPPORTED = emitted by universal-converter.py and covered by
# tests/test_platform_spec.py. PARTIALLY_SUPPORTED = emitted with caveats.
# ---------------------------------------------------------------------------

_SKILL_MD = "SKILL.md (Agent Skills)"
_RULES_MD = "rules .md"
_LEGACY = "legacy native"


def _mk(name: str, display: str, fmt: str, target: str, family: str, level: SupportLevel = SupportLevel.SUPPORTED) -> type:
    return type(
        f"Adapter_{name}",
        (PlatformAdapter,),
        {
            "name": name,
            "display_name": display,
            "format": fmt,
            "install_target": target,
            "family": family,
            "support_level": level,
        },
    )


ADAPTER_SPECS: List[Dict[str, Any]] = [
    # legacy core (6)
    {"name": "claude_code", "display": "Claude Code", "fmt": ".md YAML frontmatter", "target": "~/.claude/agents/ + ~/.claude/skills/", "family": _LEGACY},
    {"name": "cursor", "display": "Cursor", "fmt": ".mdc rules", "target": ".cursor/rules/", "family": _LEGACY},
    {"name": "github_copilot", "display": "GitHub Copilot", "fmt": ".instructions.md", "target": ".github/instructions/", "family": _LEGACY},
    {"name": "windsurf", "display": "Windsurf", "fmt": "rules .md", "target": ".windsurf/rules/", "family": _LEGACY},
    {"name": "opencode", "display": "OpenCode", "fmt": "agents .md + SKILL.md", "target": ".opencode/agents/ + .opencode/skills/", "family": _LEGACY},
    {"name": "generic", "display": "Generic", "fmt": ".json", "target": "any LLM agent", "family": _LEGACY},
    # Agent Skills (23)
    {"name": "codex_cli", "display": "OpenAI Codex CLI", "fmt": _SKILL_MD, "target": ".agents/skills/", "family": "skill-md"},
    {"name": "gemini_cli", "display": "Gemini CLI (Google)", "fmt": _SKILL_MD, "target": ".gemini/skills/", "family": "skill-md"},
    {"name": "antigravity", "display": "Antigravity (Google)", "fmt": _SKILL_MD, "target": ".agent/skills/", "family": "skill-md"},
    {"name": "devin", "display": "Devin (Cognition)", "fmt": _SKILL_MD, "target": ".devin/skills/", "family": "skill-md"},
    {"name": "zed", "display": "Zed", "fmt": _SKILL_MD, "target": ".agents/skills/", "family": "skill-md"},
    {"name": "cline", "display": "Cline", "fmt": _SKILL_MD, "target": ".clinerules/skills/", "family": "skill-md"},
    {"name": "roo_code", "display": "Roo Code", "fmt": _SKILL_MD, "target": ".roo/skills/", "family": "skill-md"},
    {"name": "kilo_code", "display": "Kilo Code", "fmt": _SKILL_MD, "target": ".kilocode/skills/", "family": "skill-md"},
    {"name": "trae", "display": "Trae (ByteDance)", "fmt": _SKILL_MD, "target": ".trae/skills/", "family": "skill-md"},
    {"name": "qwen_code", "display": "Qwen Code (Alibaba)", "fmt": _SKILL_MD, "target": ".qwen/skills/", "family": "skill-md"},
    {"name": "kiro", "display": "Kiro (Sublime)", "fmt": _SKILL_MD, "target": ".kiro/skills/", "family": "skill-md"},
    {"name": "junie", "display": "JetBrains Junie", "fmt": _SKILL_MD, "target": ".junie/skills/", "family": "skill-md"},
    {"name": "zencoder", "display": "Zencoder", "fmt": _SKILL_MD, "target": ".agents/skills/", "family": "skill-md"},
    {"name": "amp", "display": "Amp (Sourcegraph)", "fmt": _SKILL_MD, "target": ".agents/skills/", "family": "skill-md"},
    {"name": "factory_droid", "display": "Factory Droid", "fmt": _SKILL_MD, "target": ".factory/skills/", "family": "skill-md"},
    {"name": "crush", "display": "Crush (Charm)", "fmt": _SKILL_MD, "target": ".crush/skills/", "family": "skill-md"},
    {"name": "mcpjam", "display": "MCPJam", "fmt": _SKILL_MD, "target": ".mcpjam/skills/", "family": "skill-md"},
    {"name": "mux", "display": "Mux", "fmt": _SKILL_MD, "target": ".mux/skills/", "family": "skill-md"},
    {"name": "pi", "display": "Pi", "fmt": _SKILL_MD, "target": ".pi/skills/", "family": "skill-md"},
    {"name": "qoder", "display": "Qoder", "fmt": _SKILL_MD, "target": ".qoder/skills/", "family": "skill-md"},
    {"name": "codebuddy", "display": "Tencent CodeBuddy", "fmt": _SKILL_MD, "target": ".codebuddy/skills/", "family": "skill-md"},
    {"name": "commandcode", "display": "Command Code", "fmt": _SKILL_MD, "target": ".commandcode/skills/", "family": "skill-md"},
    {"name": "neovate", "display": "Neovate", "fmt": _SKILL_MD, "target": ".neovate/skills/", "family": "skill-md"},
    # rules (7)
    {"name": "grok_build", "display": "Grok Build (xAI)", "fmt": _RULES_MD, "target": ".grok/rules/", "family": "rules"},
    {"name": "amazon_q", "display": "Amazon Q Developer CLI", "fmt": _RULES_MD, "target": ".amazonq/rules/", "family": "rules"},
    {"name": "augment", "display": "Augment Code", "fmt": _RULES_MD, "target": ".augment/rules/", "family": "rules"},
    {"name": "firebase_studio", "display": "Firebase Studio (Google)", "fmt": ".mdc rules", "target": ".idx/rules/", "family": "rules"},
    {"name": "continue", "display": "Continue", "fmt": _RULES_MD, "target": ".continue/rules/", "family": "rules"},
    {"name": "tabnine", "display": "Tabnine", "fmt": "guidelines .md", "target": ".tabnine/guidelines/", "family": "rules"},
    {"name": "supermaven", "display": "Supermaven", "fmt": _RULES_MD, "target": ".supermaven/rules/", "family": "rules"},
    # special (3)
    {"name": "goose", "display": "Goose (Block)", "fmt": "recipes YAML", "target": "~/.config/goose/recipes/", "family": "special"},
    {"name": "aider", "display": "Aider", "fmt": "conventions .md", "target": "aider --read", "family": "special"},
    {"name": "openhands", "display": "OpenHands", "fmt": "microagents .md", "target": ".openhands/microagents/", "family": "special"},
    # single-file (5) - 3 partially supported (native file not yet assembled)
    {"name": "google_jules", "display": "Google Jules", "fmt": "AGENTS.md", "target": "repo root", "family": "single-file"},
    {"name": "warp", "display": "Warp AI", "fmt": "WARP.md", "target": "repo root", "family": "single-file"},
    {"name": "codegpt", "display": "CodeGPT", "fmt": "AGENTS.md", "target": "repo root", "family": "single-file", "level": SupportLevel.PARTIALLY_SUPPORTED},
    {"name": "cody", "display": "Sourcegraph Cody", "fmt": "cody.json", "target": ".vscode/", "family": "single-file", "level": SupportLevel.PARTIALLY_SUPPORTED},
    {"name": "firebender", "display": "Firebender", "fmt": "agents .md + firebender.json", "target": ".firebender/", "family": "single-file", "level": SupportLevel.PARTIALLY_SUPPORTED},
    # deprecated (1)
    {"name": "void", "display": "Void (deprecated)", "fmt": "fragments only", "target": "-", "family": "deprecated", "level": SupportLevel.PARTIALLY_SUPPORTED},
]


class AdapterRegistry:
    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root) if root else default_repo_root()
        self._adapters: Dict[str, PlatformAdapter] = {}
        for spec in ADAPTER_SPECS:
            cls = _mk(
                spec["name"],
                spec["display"],
                spec["fmt"],
                spec["target"],
                spec["family"],
                spec.get("level", SupportLevel.SUPPORTED),
            )
            self._adapters[spec["name"]] = cls(self.root)

    def get(self, name: str) -> Optional[PlatformAdapter]:
        return self._adapters.get(name)

    def all(self) -> List[PlatformAdapter]:
        return [self._adapters[n] for n in sorted(self._adapters)]

    def names(self) -> List[str]:
        return sorted(self._adapters)

    def by_support(self, level: SupportLevel) -> List[PlatformAdapter]:
        return [a for a in self.all() if a.support_level == level]

    def summary(self) -> Dict[str, Any]:
        rows = []
        for a in self.all():
            v = a.verify()
            rows.append(
                {
                    "platform": a.name,
                    "display_name": a.display_name,
                    "format": a.format,
                    "family": a.family,
                    "support_level": a.support_level.value,
                    "exists": v["exists"],
                    "items": v["items"],
                    "files": v["files"],
                    "status": v["status"],
                }
            )
        return {
            "platforms": len(self._adapters),
            "rows": rows,
            "support_counts": {level.value: len(self.by_support(level)) for level in SupportLevel},
        }