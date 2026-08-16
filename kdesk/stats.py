"""Authoritative Kdesk catalog statistics.

Every report and documentation statistic must come from this module.
Never hard-code agent/skill/workflow/file counts anywhere else.

The module is the single source of truth for:

    agents, skills, workflows, platforms, YAML/JSON counts,
    platform outputs, tests, wiring, checksums.

It refuses to return "success" numbers for a zero-file scan:
compute() raises StatsError when the catalog is empty, so callers
can never report a false pass.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.registry import Catalog, CatalogError, default_repo_root


class StatsError(Exception):
    pass


def _file_count(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for p in path.rglob("*") if p.is_file())


def _dir_count(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for p in path.iterdir() if p.is_dir())


_CHECKSUM_CACHE: Dict[str, Dict[str, str]] = {}
_PLATFORM_COUNT_CACHE: Dict[str, int] = {}


def _platform_count_key(platform_dir: Path) -> str:
    """Cheap mtime+name key over platform dirs and root-level files."""
    digest = hashlib.sha256()
    entries = sorted(platform_dir.iterdir(), key=lambda p: p.name)
    digest.update(len(entries).to_bytes(4, "big"))
    for p in entries:
        digest.update(p.name.encode("utf-8"))
        if p.is_dir():
            digest.update(b"d")
            digest.update(str(p.stat().st_mtime_ns).encode("utf-8"))
    return digest.hexdigest()[:16]


def _platform_output_count(platform_dir: Path) -> int:
    if not platform_dir.is_dir():
        return 0
    key = _platform_count_key(platform_dir)
    cached = _PLATFORM_COUNT_CACHE.get(key)
    if cached is not None:
        return cached
    count = sum(
        sum(1 for p in d.rglob("*") if p.is_file())
        for d in platform_dir.iterdir() if d.is_dir()
    )
    _PLATFORM_COUNT_CACHE[key] = count
    return count


def _definition_checksums(root: Path) -> Dict[str, str]:
    """sha256 (first 16 hex) per source YAML, keyed by repo-relative path.

    Cache is keyed by the catalog tree key (mtime+size of every YAML), so it
    stays correct and avoids re-reading ~2900 files on every call.
    """
    out: Dict[str, str] = {}
    universal = root / "universal-agents"
    if not universal.is_dir():
        return out
    key = Catalog._tree_key(universal)
    cached = _CHECKSUM_CACHE.get(key)
    if cached is not None:
        return cached
    for path in sorted(universal.rglob("*.yaml")):
        if path.name == "registry.yaml":
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        out[rel] = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    _CHECKSUM_CACHE[key] = out
    return out


def compute(root: Optional[Path] = None, fast: bool = False) -> Dict[str, Any]:
    """Compute authoritative, current repository statistics.

    Raises StatsError if zero definitions are found (never a false pass).
    
    If fast=True, skips the slow platform_output_files count and uses a cached value.
    """
    root = Path(root) if root else default_repo_root()
    if not (root / "universal-agents").is_dir():
        raise StatsError(f"universal-agents directory not found under {root}")

    try:
        catalog = Catalog.from_repo(root)
    except CatalogError as exc:
        raise StatsError(str(exc)) from exc
    if not catalog.agents and not catalog.skills:
        raise StatsError("0 definitions scanned - statistics aborted")

    universal = root / "universal-agents"
    yaml_files = sorted(p for p in universal.rglob("*.yaml") if p.name != "registry.yaml")
    json_files = sorted(universal.rglob("*.json"))

    workflows_dir = root / "workflows"
    workflow_files = sorted(workflows_dir.rglob("*.workflow.json")) if workflows_dir.is_dir() else []

    platform_dir = root / "platform-agents"
    platform_dirs = _dir_count(platform_dir)
    if fast:
        report = root / "reports" / "catalog-stats.json"
        if report.is_file():
            try:
                platform_output_files = int(json.loads(report.read_text(encoding="utf-8")).get("platform_output_files", 0))
            except (OSError, ValueError):
                platform_output_files = _platform_output_count(platform_dir)
        else:
            platform_output_files = _platform_output_count(platform_dir)
    else:
        platform_output_files = _platform_output_count(platform_dir)
    platform_registry_files = (
        sum(1 for p in platform_dir.iterdir() if p.is_file()) if platform_dir.is_dir() else 0
    )

    tests_dir = root / "tests"
    test_files = sorted(tests_dir.rglob("test_*.py")) if tests_dir.is_dir() else []

    wiring_stats: Dict[str, Any] = {}
    wiring_path = root / "skills" / "wiring.json"
    if wiring_path.is_file():
        try:
            wdata = json.loads(wiring_path.read_text(encoding="utf-8"))
            wiring_stats = wdata.get("stats", {})
        except (OSError, ValueError):
            wiring_stats = {"error": "unreadable wiring.json"}

    checksums = _definition_checksums(root)
    combined = "".join(f"{k}:{v}" for k, v in sorted(checksums.items()))

    return {
        "schema": "kdesk-stats-v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_files": len(yaml_files) + len(json_files),
        "agents": len(catalog.agents),
        "skills": len(catalog.skills),
        "definitions_total": len(catalog.agents) + len(catalog.skills),
        "workflows": len(workflow_files),
        "workflow_ids_on_file": len(workflow_files),
        "platforms": platform_dirs,
        "platform_output_files": platform_output_files,
        "platform_registry_files": platform_registry_files,
        "yaml_definitions": len(yaml_files),
        "json_definitions": len(json_files),
        "yaml_files": len(yaml_files),
        "json_files": len(json_files),
        "test_files": len(test_files),
        "load_errors": len(catalog.errors),
        "files_scanned": len(catalog.agents) + len(catalog.skills),
        "wiring": {
            "agents_wired": wiring_stats.get("agents_wired", 0),
            "links": wiring_stats.get("total_links", 0),
            "unwired_agents": wiring_stats.get("unwired_agents", 0),
            "skills_used": wiring_stats.get("skills_used", 0),
            "manual_links": wiring_stats.get("manual_links", 0),
        },
        "checksums": {
            "definition_count": len(checksums),
            "content_hash": hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16],
        },
    }


def format_table(stats: Dict[str, Any]) -> str:
    """Human-readable `kdesk stats` output."""
    w = stats.get("wiring", {})
    lines = [
        "Kdesk Statistics",
        "",
        f"Agents:    {stats['agents']}",
        f"Skills:    {stats['skills']}",
        f"Workflows: {stats['workflows']}",
        f"Platforms: {stats['platforms']}",
        f"YAML:      {stats['yaml_files']}",
        f"JSON:      {stats['json_files']}",
        f"Total:     {stats['total_files']}",
        "",
        f"Wired agents:      {w.get('agents_wired', 0)}",
        f"Wiring links:     {w.get('links', 0)}",
        f"Unwired agents:   {w.get('unwired_agents', 0)}",
        f"Platform outputs: {stats['platform_output_files']}",
        f"Load errors:      {stats['load_errors']}",
    ]
    return "\n".join(lines)


def write_baseline(root: Optional[Path] = None) -> Path:
    """Write reports/baseline-stats.json (immutable baseline snapshot)."""
    root = Path(root) if root else default_repo_root()
    stats = compute(root)
    reports_dir = root / "reports"
    reports_dir.mkdir(exist_ok=True)
    out = reports_dir / "baseline-stats.json"
    out.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out