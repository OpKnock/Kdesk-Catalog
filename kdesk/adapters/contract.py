"""Phase F: runtime adapter contract for real CLI platforms.

Extends the file-emission adapter base with a runtime contract:
detect / version / capabilities / paths / render_* / install / uninstall /
update / validate / launch / invoke / invoke_subagent / get_mcp_config /
get_permission_model / explain_limitations.

Honesty rules:
- claude_code: agents (YAML frontmatter) + skills; subagent invocation via
  `claude -p --agent` only when the CLI is detected.
- cursor: rules (.mdc) only. Cursor has no subagent delegation contract, so
  invoke_subagent raises ExecutionError (never labeled as supported).
- codex_cli: skills (SKILL.md). Codex CLI has no subagent contract, so
  invoke_subagent raises ExecutionError.

All CLI execution is guarded by detect(); missing binaries yield a
ToolResult with success=False rather than an exception.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.execution import ExecutionError
from kdesk.models import PermissionClass, ToolResult, ValidationResult


@dataclass
class AdapterCapabilities:
    """What a platform adapter can actually do at runtime."""

    detect: bool = False
    version: bool = False
    install: bool = True
    uninstall: bool = True
    update: bool = True
    validate: bool = True
    launch: bool = False
    invoke: bool = False
    invoke_subagent: bool = False
    mcp_config: bool = False
    permission_model: bool = False

    def to_dict(self) -> Dict[str, bool]:
        return {name: getattr(self, name) for name in (
            "detect", "version", "install", "uninstall", "update", "validate",
            "launch", "invoke", "invoke_subagent", "mcp_config", "permission_model",
        )}


class RuntimeAdapter:
    """Base runtime adapter: subclasses declare CLI binary + formats."""

    name: str = ""
    display_name: str = ""
    binary: str = ""            # CLI executable on PATH
    project_dir_names: List[str] = []  # config dirs in a repo
    home_dir_names: List[str] = []     # config dirs under home
    subagents: bool = False     # whether platform supports subagent delegation

    def __init__(self, project_root: Optional[Path] = None,
                 home: Optional[Path] = None) -> None:
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.home = Path(home) if home else Path.home()

    # ------------------------------------------------------------ detection
    def detect(self) -> bool:
        if self.binary and shutil.which(self.binary):
            return True
        return any((self.project_root / d).is_dir() for d in self.project_dir_names) or \
            any((self.home / d).is_dir() for d in self.home_dir_names)

    def version(self) -> Optional[str]:
        if not self.binary or not shutil.which(self.binary):
            return None
        try:
            proc = subprocess.run([self.binary, "--version"], capture_output=True,
                                  text=True, timeout=15)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if proc.returncode != 0:
            return None
        return (proc.stdout or proc.stderr or "").strip().splitlines()[0] if \
            (proc.stdout or proc.stderr) else None

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            detect=self.detect(), version=bool(self.version()),
            install=True, uninstall=True, update=True, validate=True,
            launch=self.detect(), invoke=self.detect(),
            invoke_subagent=self.subagents and self.detect(),
            mcp_config=self.has_mcp_config(), permission_model=True,
        )

    # -------------------------------------------------------------- paths
    def paths(self) -> Dict[str, str]:
        raise NotImplementedError

    def has_mcp_config(self) -> bool:
        return False

    # -------------------------------------------------------------- render
    def render_agent(self, definition: Dict[str, Any]) -> Dict[str, str]:
        raise NotImplementedError

    def render_skill(self, skill: Dict[str, Any]) -> Dict[str, str]:
        raise NotImplementedError

    def render_rules(self, definition: Dict[str, Any]) -> Dict[str, str]:
        raise NotImplementedError

    # ------------------------------------------------------------ install
    def install(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Plan an install: returns rendered content + target paths. Writing is
        done by the transactional installer (Phase G)."""
        rendered = self.render_agent(definition) if "name" in definition \
            else self.render_skill(definition)
        return {
            "adapter": self.name,
            "definition": definition.get("name", definition.get("skill", "")),
            "targets": {rel: str(self._abs(rel)) for rel in rendered},
            "content": rendered,
            "dry_run": True,
        }

    def _abs(self, relative: str) -> Path:
        path = Path(relative)
        if not path.is_absolute():
            path = self.project_root / path
        return path

    def uninstall(self, target: str) -> Dict[str, Any]:
        return {"adapter": self.name, "target": target, "action": "uninstall",
                "dry_run": True}

    def update(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        return {"adapter": self.name, "definition": definition.get("name", ""),
                "action": "update", "dry_run": True}

    # ----------------------------------------------------------- validate
    def validate(self, rendered: Dict[str, str]) -> ValidationResult:
        """Evidence-based validation of rendered output."""
        evidence: Dict[str, Any] = {}
        errors: List[str] = []
        for rel, content in rendered.items():
            ok, detail = self._check_content(rel, content)
            evidence[rel] = {"ok": ok, "detail": detail}
            if not ok:
                errors.append(f"{rel}: {detail}")
        return ValidationResult(id=f"{self.name}-validate", validator=self.name,
                                passed=not errors, evidence=evidence, errors=errors)

    def _check_content(self, rel: str, content: str) -> tuple:
        if not content.strip():
            return False, "empty content"
        if not content.lstrip().startswith("---"):
            return False, "missing YAML frontmatter"
        return True, "frontmatter present"

    # ------------------------------------------------------------ launch
    def launch(self, args: Optional[List[str]] = None,
               timeout: int = 120) -> ToolResult:
        if not self.binary or not shutil.which(self.binary):
            return ToolResult(id="launch", request_id="", success=False,
                              error=f"{self.binary or self.name} CLI not installed")
        try:
            proc = subprocess.run([self.binary] + (args or []),
                                  capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return ToolResult(id="launch", request_id="", success=False,
                              error=f"{self.binary} timed out after {timeout}s")
        except OSError as exc:
            return ToolResult(id="launch", request_id="", success=False, error=str(exc))
        return ToolResult(id="launch", request_id="", success=proc.returncode == 0,
                          exit_code=proc.returncode, stdout=proc.stdout,
                          stderr=proc.stderr)

    # ------------------------------------------------------------ invoke
    def invoke(self, prompt: str, timeout: int = 300) -> ToolResult:
        """Send a prompt to the platform CLI in headless mode."""
        raise NotImplementedError

    def invoke_subagent(self, agent_name: str, prompt: str,
                        context: Optional[Dict[str, Any]] = None,
                        timeout: int = 300) -> ToolResult:
        if not self.subagents:
            raise ExecutionError(
                f"{self.display_name} does not expose a subagent delegation "
                "contract; delegate via the kdesk orchestrator instead")
        if not self.binary or not shutil.which(self.binary):
            return ToolResult(id="subagent", request_id="", success=False,
                              error=f"{self.binary} CLI not installed")
        try:
            proc = subprocess.run(
                [self.binary, "-p", prompt, "--agent", agent_name],
                capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return ToolResult(id="subagent", request_id="", success=False,
                              error=f"{self.binary} timed out after {timeout}s")
        except OSError as exc:
            return ToolResult(id="subagent", request_id="", success=False, error=str(exc))
        return ToolResult(id="subagent", request_id="", success=proc.returncode == 0,
                          exit_code=proc.returncode, stdout=proc.stdout,
                          stderr=proc.stderr)

    def get_mcp_config(self) -> Optional[Dict[str, Any]]:
        return None

    def get_permission_model(self) -> Dict[str, Any]:
        return {"platform": self.name, "model": "unknown"}

    def explain_limitations(self) -> str:
        return (f"{self.display_name}: {self.name} adapter; "
                f"subagent delegation: {'yes' if self.subagents else 'no'}.")


class ClaudeCodeAdapter(RuntimeAdapter):
    name = "claude_code"
    display_name = "Claude Code"
    binary = "claude"
    home_dir_names = [".claude"]
    subagents = True

    def paths(self) -> Dict[str, str]:
        home_claude = self.home / ".claude"
        return {
            "agents_dir": str(home_claude / "agents"),
            "skills_dir": str(home_claude / "skills"),
            "config": str(home_claude / "settings.json"),
            "mcp_config": str(home_claude / ".mcp.json"),
        }

    def has_mcp_config(self) -> bool:
        return (self.home / ".claude" / ".mcp.json").is_file()

    def _frontmatter(self, definition: Dict[str, Any], extra: Dict[str, Any]) -> str:
        body = definition.get("body") or definition.get("content") or ""
        if not body:
            body = definition.get("description") or ""
        fields = {"name": definition.get("name") or definition.get("id"),
                  "description": definition.get("description") or ""}
        fields.update(extra)
        lines = ["---"]
        for key in ("name", "description", "tools", "model"):
            if key in fields:
                lines.append(f"{key}: {json.dumps(fields[key])}")
        lines.append("---")
        lines.append("")
        return "\n".join(lines) + body + "\n"

    def render_agent(self, definition: Dict[str, Any]) -> Dict[str, str]:
        slug = definition.get("name", "agent")
        rel = f".claude/agents/{slug}.md"
        return {rel: self._frontmatter(definition, {
            "tools": definition.get("tools") or [],
            "model": definition.get("model") or "claude-4",
        })}

    def render_skill(self, skill: Dict[str, Any]) -> Dict[str, str]:
        name = skill.get("skill") or skill.get("name", "skill")
        body = skill.get("body") or skill.get("instructions") or ""
        rel = f".claude/skills/{name}/SKILL.md"
        return {rel: self._frontmatter(skill, {}) if body.startswith("---") else
                "---\n" + f"name: {json.dumps(name)}\ndescription: "
                f"{json.dumps(skill.get('description') or '')}\n---\n\n" + body + "\n"}

    def invoke(self, prompt: str, timeout: int = 300) -> ToolResult:
        if not shutil.which(self.binary):
            return ToolResult(id="invoke", request_id="", success=False,
                              error="claude CLI not installed")
        try:
            proc = subprocess.run([self.binary, "-p", prompt],
                                  capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return ToolResult(id="invoke", request_id="", success=False,
                              error=f"claude timed out after {timeout}s")
        except OSError as exc:
            return ToolResult(id="invoke", request_id="", success=False, error=str(exc))
        return ToolResult(id="invoke", request_id="", success=proc.returncode == 0,
                          exit_code=proc.returncode, stdout=proc.stdout,
                          stderr=proc.stderr)

    def get_mcp_config(self) -> Optional[Dict[str, Any]]:
        mcp = self.home / ".claude" / ".mcp.json"
        if mcp.is_file():
            try:
                return json.loads(mcp.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
        return None

    def get_permission_model(self) -> Dict[str, Any]:
        return {"platform": self.name, "model": "permission-modes",
                "modes": ["default", "acceptEdits", "plan", "bypassPermissions"],
                "prompt_threshold": "require approval above READ_ONLY by default"}

    def explain_limitations(self) -> str:
        return ("Claude Code: agents installed to ~/.claude/agents/ and skills "
                "to ~/.claude/skills/. Subagent invocation requires the claude "
                "CLI and the --agent flag; verification of every catalog agent "
                "in this platform is out of scope.")


class CursorAdapter(RuntimeAdapter):
    name = "cursor"
    display_name = "Cursor"
    binary = "cursor"
    project_dir_names = [".cursor"]
    subagents = False

    def paths(self) -> Dict[str, str]:
        return {"rules_dir": str(self.project_root / ".cursor" / "rules")}

    def render_rules(self, definition: Dict[str, Any]) -> Dict[str, str]:
        slug = definition.get("name", "rule")
        content = definition.get("body") or definition.get("description") or ""
        rel = f".cursor/rules/{slug}.mdc"
        head = (f"---\ndescription: {json.dumps(definition.get('description') or '')}\n"
                f"globs: {json.dumps(definition.get('globs') or ['**/*'])}\n"
                f"alwaysApply: false\n---\n\n")
        return {rel: head + content + "\n"}

    def invoke(self, prompt: str, timeout: int = 300) -> ToolResult:
        return ToolResult(id="invoke", request_id="", success=False,
                          error="Cursor has no headless CLI prompt contract")

    def get_permission_model(self) -> Dict[str, Any]:
        return {"platform": self.name, "model": "allowlist-rules",
                "note": "Cursor applies .mdc rules by glob; no runtime permission prompt API"}

    def explain_limitations(self) -> str:
        return ("Cursor: rules are emitted as .mdc files under .cursor/rules/. "
                "Cursor does not expose a subagent delegation or headless "
                "invocation contract, so invoke/invoke_subagent are unsupported.")


class CodexCliAdapter(RuntimeAdapter):
    name = "codex_cli"
    display_name = "OpenAI Codex CLI"
    binary = "codex"
    project_dir_names = [".agents"]
    subagents = False

    def paths(self) -> Dict[str, str]:
        return {"skills_dir": str(self.project_root / ".agents" / "skills")}

    def render_skill(self, skill: Dict[str, Any]) -> Dict[str, str]:
        name = skill.get("skill") or skill.get("name", "skill")
        body = skill.get("body") or skill.get("instructions") or ""
        rel = f".agents/skills/{name}/SKILL.md"
        head = (f"---\nname: {json.dumps(name)}\n"
                f"description: {json.dumps(skill.get('description') or '')}\n---\n\n")
        return {rel: head + body + "\n"}

    def invoke(self, prompt: str, timeout: int = 300) -> ToolResult:
        if not shutil.which(self.binary):
            return ToolResult(id="invoke", request_id="", success=False,
                              error="codex CLI not installed")
        try:
            proc = subprocess.run([self.binary, "exec", prompt],
                                  capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return ToolResult(id="invoke", request_id="", success=False,
                              error=f"codex timed out after {timeout}s")
        except OSError as exc:
            return ToolResult(id="invoke", request_id="", success=False, error=str(exc))
        return ToolResult(id="invoke", request_id="", success=proc.returncode == 0,
                          exit_code=proc.returncode, stdout=proc.stdout,
                          stderr=proc.stderr)

    def get_permission_model(self) -> Dict[str, Any]:
        return {"platform": self.name, "model": "sandbox",
                "modes": ["workspace-write", "edit", "sandbox"]}

    def explain_limitations(self) -> str:
        return ("Codex CLI: skills are emitted as SKILL.md under .agents/skills/. "
                "Codex CLI does not expose a subagent delegation contract; use "
                "the kdesk orchestrator for multi-agent workflows.")


RUNTIME_ADAPTERS: Dict[str, type] = {
    "claude_code": ClaudeCodeAdapter,
    "cursor": CursorAdapter,
    "codex_cli": CodexCliAdapter,
}


class RuntimeAdapterRegistry:
    def __init__(self, project_root: Optional[Path] = None,
                 home: Optional[Path] = None) -> None:
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.home = Path(home) if home else Path.home()
        self._adapters: Dict[str, RuntimeAdapter] = {
            name: cls(self.project_root, self.home)
            for name, cls in RUNTIME_ADAPTERS.items()
        }

    def get(self, name: str) -> Optional[RuntimeAdapter]:
        return self._adapters.get(name)

    def names(self) -> List[str]:
        return sorted(self._adapters)

    def detect_all(self) -> Dict[str, bool]:
        return {name: a.detect() for name, a in sorted(self._adapters.items())}

    def version_all(self) -> Dict[str, Optional[str]]:
        return {name: a.version() for name, a in sorted(self._adapters.items())}

    def capabilities_all(self) -> Dict[str, Dict[str, bool]]:
        return {name: a.capabilities().to_dict()
                for name, a in sorted(self._adapters.items())}