"""Phase K executor: real tool execution with built-in handlers.

Handlers are deterministic and bounded:
  read_file / glob_files / grep / analyze_project  -> read-only, SAFE
  write_file                                        -> SAFE_WRITE (approval)
  run_python / shell                                -> MODERATE (approval)
  git                                               -> read-only subcommands

All captured output passes through secret redaction before it is returned
or persisted. Subprocesses use argv arrays (no shell interpolation) and
hard timeouts.
"""
from __future__ import annotations

import ast
import glob as _glob
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from kdesk.models import PermissionClass, Tool, ToolResult
from kdesk.security import REDACTED, _PATTERNS

MAX_TEXT_BYTES = 1_000_000
MAX_OUTPUT_CHARS = 200_000


def redact_text(text: str) -> str:
    """Replace every known secret pattern with REDACTED."""
    for regex in _PATTERNS.values():
        text = re.sub(regex, REDACTED, text)
    return text


def sha256_text(content: str) -> str:
    import hashlib

    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class ExecutionContextError(Exception):
    """Args violate the execution context (path escape, malformed input)."""


class ToolExecutor:
    """Executes built-in runtime tools against a bounded base directory."""

    HANDLERS: Dict[str, Callable] = {}

    def __init__(self, base: Path):
        self.base = Path(base).resolve()

    # ------------------------------------------------------------ registry
    @staticmethod
    def runtime_tools() -> List[Tool]:
        return [
            Tool(id="read_file", name="read_file", description="read a text file",
                 category="filesystem", risk=PermissionClass.READ_ONLY,
                 handler="read_file", platform_support={"kdesk": True}),
            Tool(id="glob_files", name="glob_files", description="list files by glob pattern",
                 category="filesystem", risk=PermissionClass.READ_ONLY,
                 handler="glob_files", platform_support={"kdesk": True}),
            Tool(id="grep", name="grep", description="regex search over files",
                 category="filesystem", risk=PermissionClass.READ_ONLY,
                 handler="grep", platform_support={"kdesk": True}),
            Tool(id="analyze_project", name="analyze_project",
                 description="AST-based static analysis of a Python project",
                 category="analysis", risk=PermissionClass.READ_ONLY,
                 handler="analyze_project", platform_support={"kdesk": True}),
            Tool(id="write_file", name="write_file", description="write a text file",
                 category="filesystem", risk=PermissionClass.SAFE_WRITE,
                 permission_required=True, handler="write_file",
                 platform_support={"kdesk": True}),
            Tool(id="run_python", name="run_python", description="run a python script file",
                 category="process", risk=PermissionClass.MODERATE,
                 permission_required=True, handler="run_python",
                 platform_support={"kdesk": True}),
            Tool(id="git", name="git", description="read-only git subcommands",
                 category="vcs", risk=PermissionClass.READ_ONLY,
                 handler="git", platform_support={"kdesk": True}),
            Tool(id="shell", name="shell", description="run a shell command (argv array)",
                 category="process", risk=PermissionClass.MODERATE,
                 permission_required=True, handler="shell",
                 platform_support={"kdesk": True}),
        ]

    @classmethod
    def tool_by_id(cls, tool_id: str) -> Optional[Tool]:
        return next((t for t in cls.runtime_tools() if t.id == tool_id), None)

    def risk_of(self, tool_id: str) -> str:
        tool = self.tool_by_id(tool_id)
        if tool is None:
            return "review_required"
        from kdesk.policy import permission_to_risk

        return permission_to_risk(tool.risk)

    # ------------------------------------------------------------- context
    def _resolve_path(self, raw: str) -> Path:
        path = Path(str(raw)).expanduser()
        if not path.is_absolute():
            path = self.base / path
        resolved = path.resolve()
        try:
            resolved.relative_to(self.base)
        except ValueError as exc:
            raise ExecutionContextError(
                f"path escapes execution base: {raw}"
            ) from exc
        return resolved

    def _require(self, args: Dict[str, Any], key: str) -> Any:
        value = args.get(key)
        if value is None or value == "":
            raise ExecutionContextError(f"missing required argument: {key}")
        return value

    # ----------------------------------------------------------- handlers
    def _handle_read_file(self, args: Dict[str, Any]) -> ToolResult:
        path = self._resolve_path(self._require(args, "path"))
        if not path.is_file():
            return self._result(False, error=f"not a file: {path.name}")
        data = path.read_bytes()
        if len(data) > MAX_TEXT_BYTES:
            return self._result(False, error=f"file too large ({len(data)} bytes)")
        text = data.decode("utf-8", errors="replace")
        return self._result(True, stdout=text[:MAX_OUTPUT_CHARS], output={"path": str(path.relative_to(self.base)), "bytes": len(text)})

    def _handle_glob_files(self, args: Dict[str, Any]) -> ToolResult:
        pattern = self._require(args, "pattern")
        matches = sorted(
            str(Path(p).relative_to(self.base))
            for p in _glob.glob(str(self.base / pattern), recursive=True)
            if Path(p).is_file()
        )
        return self._result(True, stdout="\n".join(matches) or "(no matches)",
                            output={"matches": matches[:500], "count": len(matches)})

    def _handle_grep(self, args: Dict[str, Any]) -> ToolResult:
        pattern = self._require(args, "pattern")
        include = str(args.get("include", "*.py"))
        try:
            regex = re.compile(pattern)
        except re.error as exc:
            return self._result(False, error=f"invalid regex: {exc}")
        hits: List[str] = []
        count = 0
        for path in sorted(self.base.rglob(include)):
            if not path.is_file() or path.name in (".gitignore",):
                continue
            if len(path.read_bytes()) > MAX_TEXT_BYTES:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if regex.search(line):
                    hits.append(f"{path.relative_to(self.base)}:{lineno}")
                    count += 1
                    if count >= 200:
                        break
            if count >= 200:
                break
        return self._result(True, stdout="\n".join(hits) or "(no matches)",
                            output={"hits": hits, "count": count})

    def _handle_analyze_project(self, args: Dict[str, Any]) -> ToolResult:
        target = self._resolve_path(str(args.get("path", ".")))
        if not target.is_dir():
            return self._result(False, error=f"not a directory: {target.name}")
        report = analyze_python_project(target)
        summary = (
            f"analyzed {report['files']} python files: "
            f"{report['functions']} functions, {report['classes']} classes, "
            f"{report['imports']} imports, {report['todos']} TODO markers"
        )
        return self._result(True, stdout=summary, output=report)

    def _handle_write_file(self, args: Dict[str, Any]) -> ToolResult:
        path = self._resolve_path(self._require(args, "path"))
        content = str(args.get("content", ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return self._result(True, stdout=f"wrote {path.relative_to(self.base)} ({len(content)} bytes)",
                            output={"path": str(path.relative_to(self.base)), "bytes": len(content)})

    def _handle_run_python(self, args: Dict[str, Any]) -> ToolResult:
        script = self._resolve_path(self._require(args, "script"))
        if not script.is_file():
            return self._result(False, error=f"not a file: {script.name}")
        argv = [sys.executable, str(script)] + [str(a) for a in (args.get("args") or [])]
        return self._subprocess(argv, timeout=float(args.get("timeout_s", 30)))

    def _handle_git(self, args: Dict[str, Any]) -> ToolResult:
        subcommands = [str(a) for a in (args.get("args") or [])]
        if not subcommands:
            return self._result(False, error="missing git subcommand")
        # Only genuinely read-only git subcommands (never mutate state)
        read_only = {"status", "log", "diff", "show", "rev-parse",
                     "ls-files", "describe"}
        # These look read-only but can create/delete/modify: branch, tag, remote, config
        if subcommands[0] not in read_only:
            return self._result(False, error=f"git subcommand '{subcommands[0]}' is not read-only")
        return self._subprocess(["git"] + subcommands, timeout=float(args.get("timeout_s", 20)))

    def _handle_shell(self, args: Dict[str, Any]) -> ToolResult:
        argv = [str(a) for a in (args.get("argv") or [])]
        if not argv:
            return self._result(False, error="missing argv")
        return self._subprocess(argv, timeout=float(args.get("timeout_s", 30)))

    # ------------------------------------------------------------ plumbing
    def _subprocess(self, argv: List[str], timeout: float) -> ToolResult:
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.base),
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
        except subprocess.TimeoutExpired as exc:
            return self._result(False, error=f"timed out after {timeout:.0f}s", exit_code=124)
        except OSError as exc:
            return self._result(False, error=f"failed to start: {exc}")
        return self._result(
            proc.returncode == 0,
            exit_code=proc.returncode,
            stdout=proc.stdout[:MAX_OUTPUT_CHARS],
            stderr=proc.stderr[:MAX_OUTPUT_CHARS],
        )

    def _result(self, success: bool, exit_code: Optional[int] = None,
                stdout: str = "", stderr: str = "", output: Any = None,
                error: str = "") -> ToolResult:
        return ToolResult(
            id=f"{time.time_ns():x}",
            request_id="",
            success=success,
            exit_code=exit_code,
            stdout=redact_text(stdout),
            stderr=redact_text(stderr),
            output=output,
            error=redact_text(error),
        )

    # ------------------------------------------------------------ dispatch
    def execute(self, tool_id: str, args: Dict[str, Any],
                timeout: float = 30.0) -> ToolResult:
        handlers = {
            "read_file": self._handle_read_file,
            "glob_files": self._handle_glob_files,
            "grep": self._handle_grep,
            "analyze_project": self._handle_analyze_project,
            "write_file": self._handle_write_file,
            "run_python": self._handle_run_python,
            "git": self._handle_git,
            "shell": self._handle_shell,
        }
        handler = handlers.get(tool_id)
        if handler is None:
            return self._result(False, error=f"unknown runtime tool: {tool_id}")
        try:
            result = handler(args)
        except ExecutionContextError as exc:
            return self._result(False, error=str(exc))
        return result

    def execute_with_retry(self, tool_id: str, args: Dict[str, Any],
                           timeout: float = 30.0, retries: int = 2,
                           backoff_s: float = 0.1) -> ToolResult:
        for attempt in range(retries + 1):
            result = self.execute(tool_id, args, timeout=timeout)
            if result.success or not _TRANSIENT_RE.search(result.stderr + result.error):
                return result
            time.sleep(backoff_s * (attempt + 1))
        return result


_TRANSIENT_RE = re.compile(r"(timed out|timeout|connection (reset|refused)|temporarily unavailable|too many files)")


def analyze_python_project(root: Path) -> Dict[str, Any]:
    """Pure-stdlib AST analysis: functions, classes, imports, TODOs, size."""
    stats = {
        "files": 0, "lines": 0, "functions": 0, "classes": 0, "imports": 0,
        "todos": 0, "errors": 0, "modules": [], "files_list": [],
    }
    seen_imports = set()
    for path in sorted(root.rglob("*.py")):
        if not path.is_file() or any(part.startswith(".") for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        stats["files"] += 1
        stats["lines"] += len(text.splitlines())
        stats["files_list"].append(str(path.relative_to(root)))
        for lineno, line in enumerate(text.splitlines(), 1):
            if re.search(r"#\s*(TODO|FIXME|XXX)", line):
                stats["todos"] += 1
            if "error" in line.lower() and ("except" in line.lower() or "raise" in line.lower()):
                stats["errors"] += 1
        try:
            tree = ast.parse(text)
        except SyntaxError:
            stats["errors"] += 1
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                stats["functions"] += 1
            elif isinstance(node, ast.ClassDef):
                stats["classes"] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    name = (alias.asname or alias.name).split(".")[0]
                    if name not in ("__future__",):
                        seen_imports.add(name)
    stats["imports"] = len(seen_imports)
    stats["modules"] = sorted(seen_imports)[:200]
    stats["files_list"] = stats["files_list"][:500]
    return stats


def validate_expected(result: ToolResult, expected_output: str) -> bool:
    """Deterministic output validation: expected token appears in output."""
    if not expected_output:
        return True
    return expected_output.lower() in (result.stdout + result.error + json.dumps(result.output or {})).lower()