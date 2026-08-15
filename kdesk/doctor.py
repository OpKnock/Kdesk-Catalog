"""kdesk doctor: per-platform install verification with scanned-file counts.

Never reports OK on an empty scan - every verdict carries scanned counts.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.adapters import AdapterRegistry


class Doctor:
    def __init__(self, adapters: AdapterRegistry, base: Optional[Path] = None):
        self.adapters = adapters
        self.base = Path(base) if base else Path.cwd()

    # ------------------------------------------------------------- verdicts
    def check(self, platform: str) -> Dict[str, Any]:
        adapter = self.adapters.get(platform)
        if adapter is None:
            return {"platform": platform, "status": "UNKNOWN", "scanned_files": 0, "note": "no adapter"}
        if not adapter.exists():
            return {"platform": platform, "status": "NOT_GENERATED", "scanned_files": 0, "note": "platform-agents/<name> missing; run converter"}
        generated = adapter.items_emitted()
        if generated == 0:
            return {"platform": platform, "status": "EMPTY", "scanned_files": 0, "note": "generated dir has no item files"}
        installed = self._find_installed(adapter)
        scanned = sum(1 for p in installed.rglob("*") if p.is_file()) if installed else 0
        if not installed:
            return {
                "platform": platform,
                "status": "MISSING",
                "scanned_files": scanned,
                "expected": generated,
                "installed": 0,
            }
        return {
            "platform": platform,
            "status": "OK",
            "scanned_files": scanned,
            "expected": generated,
            "installed": scanned,
            "install_target": str(installed),
        }

    def _find_installed(self, adapter) -> Optional[Path]:
        """Locate the installed copy for a platform (project or home)."""
        name = adapter.name
        home_candidates = {
            "claude_code": [Path.home() / ".claude"],
            "goose": [Path.home() / ".config" / "goose" / "recipes"],
            "opencode": [Path.home() / ".config" / "opencode" / "plugin"],
        }
        project_candidates = {
            "claude_code": [self.base / ".claude"],
            "cursor": [self.base / ".cursor" / "rules"],
            "github_copilot": [self.base / ".github" / "instructions"],
            "windsurf": [self.base / ".windsurf" / "rules"],
            "opencode": [self.base / ".opencode"],
            "codex_cli": [self.base / ".agents" / "skills"],
            "gemini_cli": [self.base / ".gemini" / "skills"],
            "antigravity": [self.base / ".agent" / "skills"],
            "devin": [self.base / ".devin" / "skills"],
            "zed": [self.base / ".agents" / "skills"],
            "cline": [self.base / ".clinerules" / "skills"],
            "roo_code": [self.base / ".roo" / "skills"],
            "kilo_code": [self.base / ".kilocode" / "skills"],
            "trae": [self.base / ".trae" / "skills"],
            "qwen_code": [self.base / ".qwen" / "skills"],
            "kiro": [self.base / ".kiro" / "skills"],
            "junie": [self.base / ".junie" / "skills"],
            "zencoder": [self.base / ".agents" / "skills"],
            "amp": [self.base / ".agents" / "skills"],
            "factory_droid": [self.base / ".factory" / "skills"],
            "crush": [self.base / ".crush" / "skills"],
            "mcpjam": [self.base / ".mcpjam" / "skills"],
            "mux": [self.base / ".mux" / "skills"],
            "pi": [self.base / ".pi" / "skills"],
            "qoder": [self.base / ".qoder" / "skills"],
            "codebuddy": [self.base / ".codebuddy" / "skills"],
            "commandcode": [self.base / ".commandcode" / "skills"],
            "neovate": [self.base / ".neovate" / "skills"],
            "grok_build": [self.base / ".grok" / "rules"],
            "amazon_q": [self.base / ".amazonq" / "rules"],
            "augment": [self.base / ".augment" / "rules"],
            "firebase_studio": [self.base / ".idx" / "rules"],
            "continue": [self.base / ".continue" / "rules"],
            "tabnine": [self.base / ".tabnine" / "guidelines"],
            "supermaven": [self.base / ".supermaven" / "rules"],
            "openhands": [self.base / ".openhands" / "microagents"],
            "google_jules": [self.base / "AGENTS.md"],
            "warp": [self.base / "WARP.md"],
            "codegpt": [self.base / "AGENTS.md"],
            "cody": [self.base / ".vscode"],
            "firebender": [self.base / ".firebender"],
        }
        for cand in home_candidates.get(name, []) + project_candidates.get(name, []):
            if cand.exists():
                return cand if cand.is_dir() or cand.is_file() else None
        return None

    def check_all(self) -> List[Dict[str, Any]]:
        return [self.check(a.name) for a in self.adapters.all()]

    def summary(self) -> Dict[str, Any]:
        rows = self.check_all()
        from collections import Counter

        by_status = Counter(r["status"] for r in rows)
        total_scanned = sum(r["scanned_files"] for r in rows)
        return {
            "platforms": len(rows),
            "status_counts": dict(by_status),
            "files_scanned": total_scanned,
            "rows": rows,
        }