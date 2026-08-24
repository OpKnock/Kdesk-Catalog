"""Shared helpers for kdesk CLI command modules."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, List

from kdesk.registry import Catalog, default_repo_root


def _out(data: Any, fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        if isinstance(data, dict) and "rows" in data:
            for row in data["rows"]:
                print(row)
        else:
            print(json.dumps(data, indent=2, default=str))


def _catalog(args) -> Catalog:
    root = Path(args.root) if args.root else default_repo_root()
    return Catalog.from_repo(root)


def _subprocess_ok(argv: List[str], root: Path,
                   timeout: float = 120.0) -> tuple:
    import subprocess
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, cwd=str(root),
            timeout=timeout, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"
    detail = (proc.stdout or "").strip()
    if proc.returncode != 0 and proc.stderr.strip():
        detail = f"{detail}\n{proc.stderr.strip()}"
    return proc.returncode, detail


def _root_or_default(args) -> Path:
    return Path(args.root) if args.root else __import__(
        "kdesk.registry", fromlist=["default_repo_root"]).default_repo_root()
