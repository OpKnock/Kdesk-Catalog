"""Anonymous telemetry: opt-in usage stats for Kdesk CLI commands.

Writes to <root>/.kdesk/telemetry.jsonl. No network calls.
Tracks: command name, duration, success/fail. Never tracks arguments or content.

Enable with: kdesk config set telemetry true (or KD_TELEMETRY=1 env var)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

TELEMETRY_DIR = ".kdesk"
TELEMETRY_FILE = "telemetry.jsonl"


def is_enabled() -> bool:
    """Check if telemetry collection is enabled."""
    if os.environ.get("KD_TELEMETRY") == "1":
        return True
    if os.environ.get("KD_NO_TELEMETRY") == "1":
        return False
    # Check local config
    root = Path.cwd()
    for p in [root] + list(root.parents):
        cfg = p / TELEMETRY_DIR / "config.json"
        if cfg.is_file():
            try:
                return bool(json.loads(cfg.read_text(encoding="utf-8")).get("telemetry", False))
            except Exception:
                pass
    return False


def record(command: str, status: str, duration_ms: int, extra: Optional[Dict[str, Any]] = None) -> None:
    """Write an anonymous telemetry event if enabled."""
    if not is_enabled():
        return
    try:
        root = Path.cwd()
        tel_dir = root / TELEMETRY_DIR
        tel_dir.mkdir(exist_ok=True)
        path = tel_dir / TELEMETRY_FILE

        event = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "cmd": command,
            "status": status,
            "ms": duration_ms,
        }
        if extra:
            # Only allow safe keys
            safe_keys = {"count", "platform", "mode"}
            event.update({k: v for k, v in extra.items() if k in safe_keys})

        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
    except OSError:
        pass


def summary(root: Optional[Path] = None, limit: int = 50) -> Dict[str, Any]:
    """Read telemetry events and produce aggregate stats."""
    root = Path(root) if root else Path.cwd()
    path = root / TELEMETRY_DIR / TELEMETRY_FILE
    if not path.is_file():
        return {"total": 0, "commands": {}}

    counts: Dict[str, int] = {}
    total = 0
    errors = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except ValueError:
                continue
            total += 1
            cmd = e.get("cmd", "?")
            counts[cmd] = counts.get(cmd, 0) + 1
            if e.get("status") not in ("ok", "success"):
                errors += 1

    top = dict(sorted(counts.items(), key=lambda x: -x[1])[:limit])
    return {"total": total, "errors": errors, "commands": top}


class TelemetryContext:
    """Context manager that records a command execution."""

    def __init__(self, command: str):
        self.command = command
        self.t0 = 0.0

    def __enter__(self):
        self.t0 = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ms = int((time.monotonic() - self.t0) * 1000)
        status = "error" if exc_type else "ok"
        record(self.command, status, ms)


# Convenience decorator
def tracked(func):
    """Decorator that wraps a function with telemetry tracking."""
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with TelemetryContext(func.__name__):
            return func(*args, **kwargs)
    return wrapper
