"""Phase G: transactional installer (manifest / drift / rollback).

Copies emitted platform output (`platform-agents/<platform>/`) into each
platform's real install target (project or home), records a manifest of
installed files (sha256 per target) under `<base>/.kdesk/manifest.json`,
snapshots overwritten content to `<base>/.kdesk/backups/`, and supports
uninstall / drift reporting / rollback.

Contract (pinned by tests/test_kdesk_install.py):
    Installer(registry, dry_run=False)
    installer.install(platform, target="project"|"home", base=Path)
        -> {"results": [{"status": "DRY-RUN"|"OK", "copied": int, ...}]}
    InstallError for unknown platforms and deprecated `void`.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from kdesk.adapters import AdapterRegistry, PlatformAdapter
from kdesk.execution import ExecutionError

MANIFEST_REL = ".kdesk/manifest.json"
BACKUPS_REL = ".kdesk/backups"
SKIP_NAMES = {"README.md", "registry.yaml", "registry.json"}
_HOME_MARKERS = ("~", "~/")


class InstallError(ExecutionError):
    """Raised for unknown/deprecated platforms and not-installed updates."""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _dest_specs(install_target: str) -> List[str]:
    """Split '~/.claude/agents/ + ~/.claude/skills/' into path specs."""
    return [part.strip() for part in install_target.split("+") if part.strip()]


_DEF_INDEX_CACHE: Dict[str, Dict[str, set]] = {}
_DEF_CATEGORY_CACHE: Dict[str, Dict[str, set]] = {}


def _def_index(root: Path) -> Dict[str, set]:
    """def id (file stem) -> set of capability tool names.

    Built from agents/json and skills/json; used by the ``tool`` filter.
    """
    key = str(Path(root))
    cached = _DEF_INDEX_CACHE.get(key)
    if cached is not None:
        return cached
    index: Dict[str, set] = {}
    for base in (Path(root) / "agents" / "json", Path(root) / "skills" / "json"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            tools = data.get("tools")
            if isinstance(tools, list):
                index[path.stem] = set(tools)
    _DEF_INDEX_CACHE[key] = index
    return index


def _def_categories(root: Path) -> Dict[str, set]:
    """def id (file stem) -> set of category names (first path component).

    JSON definitions live at ``<base>/<category>/<kind>/<name>.json`` (agents)
    or ``<base>/<name>/...`` (skills); the category is the first component.
    """
    key = str(Path(root))
    cached = _DEF_CATEGORY_CACHE.get(key)
    if cached is not None:
        return cached
    index: Dict[str, set] = {}
    for base in (Path(root) / "agents" / "json", Path(root) / "skills" / "json"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.json"):
            rel = path.relative_to(base).parts
            if rel:
                index.setdefault(path.stem, set()).add(rel[0])
    _DEF_CATEGORY_CACHE[key] = index
    return index


def _source_files(source: Path, spec: str) -> List[Tuple[Path, str]]:
    """(src, rel) pairs for a spec.

    Emitted trees already carry their target-relative prefix (e.g.
    ``.claude/agents/...`` inside ``platform-agents/claude_code/``), so files
    under ``source/<spec_rel>`` map with that prefix stripped; platforms with
    flat output (cursor) contribute top-level files only.
    """
    spec_rel = Path(spec.lstrip("~/"))
    base_dir = source / spec_rel
    if base_dir.is_dir():
        files = [p for p in base_dir.rglob("*") if p.is_file()
                 and p.name not in SKIP_NAMES]
        return [(p, p.relative_to(base_dir).as_posix()) for p in files]
    files = [p for p in source.iterdir() if p.is_file()
             and p.name not in SKIP_NAMES]
    return [(p, p.name) for p in files]


class InstallManifest:
    """JSON manifest: platform -> {"installed_at", "targets": {rel: sha256}}."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.is_file():
            return {"version": 1, "installs": {}}
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(raw, dict) and isinstance(raw.get("installs"), dict):
                return raw
        except (OSError, json.JSONDecodeError):
            pass
        return {"version": 1, "installs": {}}

    def entry(self, platform: str) -> Optional[Dict[str, Any]]:
        return self.data["installs"].get(platform)

    def put(self, platform: str, entry: Dict[str, Any]) -> None:
        self.data["installs"][platform] = entry

    def remove(self, platform: str) -> bool:
        if platform not in self.data["installs"]:
            return False
        del self.data["installs"][platform]
        return True

    def platforms(self) -> List[str]:
        return sorted(self.data["installs"])

    def all(self) -> Dict[str, Dict[str, Any]]:
        return self.data["installs"]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        os.replace(tmp, self.path)


class Installer:
    def __init__(self, registry: AdapterRegistry, dry_run: bool = False,
                 base: Optional[Path] = None,
                 home_dir: Optional[Path] = None) -> None:
        self.registry = registry
        self.dry_run = dry_run
        self.base = Path(base) if base else registry.root
        self.home_dir = Path(home_dir) if home_dir else Path.home()
        self.manifest = InstallManifest(self.base / MANIFEST_REL)
        self.backups_dir = self.base / BACKUPS_REL

    # ------------------------------------------------------------- helpers
    def _adapter(self, platform: str) -> PlatformAdapter:
        adapter = self.registry.get(platform)
        if adapter is None:
            raise InstallError(f"unknown platform: {platform}")
        if platform == "void":
            raise InstallError("void is deprecated and not installable")
        return adapter

    def _dest_root(self, spec: str, target: str, base: Path) -> Path:
        if spec.startswith(_HOME_MARKERS) or target == "home":
            return self.home_dir / spec.lstrip("~/")
        return base / spec.lstrip("~/")

    def _key(self, spec: str, rel: str) -> str:
        """Manifest key: install-target-relative posix path."""
        return (Path(spec.lstrip("~/")) / rel).as_posix()

    def _backup(self, base: Path, platform: str, rel: str,
                target: Path) -> Optional[str]:
        if not target.is_file():
            return None
        digest = hashlib.sha256(rel.encode("utf-8")).hexdigest()[:16]
        backup = base / BACKUPS_REL / platform / f"{digest}.bak"
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(target.read_bytes())
        return backup.relative_to(base).as_posix()

    def _copy_one(self, base: Path, platform: str, src: Path, dst: Path,
                  key: str) -> Tuple[str, Optional[str]]:
        """Returns (status, backup_rel)."""
        data = src.read_bytes()
        digest = _sha256_bytes(data)
        if dst.is_file() and _sha256_bytes(dst.read_bytes()) == digest:
            return "unchanged", None
        if self.dry_run:
            return "DRY-RUN", None
        backup_rel = self._backup(base, platform, key, dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(dst.parent), suffix=".kdesk-tmp")
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(data)
            os.replace(tmp, dst)
        except OSError:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise
        return "OK", backup_rel

    def _link_one(self, base: Path, platform: str, src: Path, dst: Path,
                  key: str) -> str:
        """Symlink src -> dst; fall back to a copy when the OS refuses."""
        try:
            if dst.is_symlink() or dst.is_file():
                if dst.resolve() == src.resolve():
                    return "unchanged"
        except OSError:
            pass
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.symlink_to(src)
            return "LINK"
        except OSError:
            return self._copy_one(base, platform, src, dst, key)[0]

    # -------------------------------------------------------------- install
    def install(self, platform: str, target: str = "project",
                base: Optional[Path] = None, scope: Optional[str] = None,
                tool: Optional[str] = None,
                agents: Optional[set] = None,
                category: Optional[set] = None,
                link: bool = False) -> Dict[str, Any]:
        adapter = self._adapter(platform)
        source = adapter.output_dir
        if not source.is_dir():
            raise InstallError(f"{platform} has not been generated "
                               "(missing platform-agents/{platform})")
        if scope is not None and scope not in ("agents", "skills"):
            raise InstallError(f"unknown scope: {scope}")
        tool_ids: Optional[set] = None
        if tool is not None:
            index = _def_index(self.registry.root)
            tool_ids = {tid for tid, tools in index.items() if tool in tools}
            if not tool_ids:
                raise InstallError(f"unknown tool: {tool} "
                                   "(no definitions invoke it)")
        cat_index: Optional[Dict[str, set]] = None
        if category is not None:
            cat_index = _def_categories(self.registry.root)
        base = Path(base) if base else self.base
        manifest = InstallManifest(base / MANIFEST_REL)
        results = []
        specs = _dest_specs(adapter.install_target)
        total_matched = 0
        for spec in specs:
            dest_root = self._dest_root(spec, target, base)
            mapping = _source_files(source, spec)
            if scope is not None or tool is not None or agents is not None \
                    or category is not None:
                mapping = [
                    (src, rel) for src, rel in mapping
                    if (scope is None
                        or scope in Path(self._key(spec, rel)).parts)
                    and (tool is None or Path(rel).stem in tool_ids)
                    and (agents is None or Path(rel).stem in agents)
                    and (category is None
                         or (Path(rel).stem in cat_index
                             and cat_index[Path(rel).stem] & category))
                ]
            total_matched += len(mapping)
            copied = 0
            for src, rel in mapping:
                key = self._key(spec, rel)
                dst = dest_root / rel
                if link and not self.dry_run:
                    status = self._link_one(base, platform, src, dst, key)
                else:
                    status, _ = self._copy_one(base, platform, src, dst, key)
                if status in ("OK", "DRY-RUN", "LINK"):
                    copied += 1
            results.append({
                "platform": platform,
                "target": target,
                "destination": str(dest_root),
                "status": "DRY-RUN" if self.dry_run else "OK",
                "copied": copied,
                "files": len(mapping),
            })
        if total_matched == 0:
            detail = f"scope={scope}" if scope is not None else (
                f"tool={tool}" if tool is not None else (
                    f"agents={agents}" if agents is not None
                    else f"category={category}"))
            raise InstallError(f"filter ({detail}) matched no files "
                               f"for {platform}")
        if not self.dry_run:
            targets = {}
            for spec in specs:
                dest_root = self._dest_root(spec, target, base)
                for src, rel in _source_files(source, spec):
                    dst = dest_root / rel
                    if dst.is_file():
                        targets[self._key(spec, rel)] = _sha256_bytes(
                            dst.read_bytes())
            manifest.put(platform, {
                "platform": platform,
                "installed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "targets": targets,
            })
            manifest.save()
        return {"results": results}

    @staticmethod
    def _prune_empty(root: Path) -> None:
        if not root.is_dir():
            return
        for dirpath, dirnames, filenames in os.walk(root, topdown=False):
            if not dirnames and not filenames and dirpath != str(root):
                os.rmdir(dirpath)
        if not any(root.iterdir()):
            os.rmdir(root)

    # ------------------------------------------------------------ uninstall
    def uninstall(self, platform: str,
                  base: Optional[Path] = None) -> Dict[str, Any]:
        adapter = self._adapter(platform)
        base = Path(base) if base else self.base
        manifest = InstallManifest(base / MANIFEST_REL)
        entry = manifest.entry(platform)
        if entry is None:
            raise InstallError(f"not installed: {platform}")
        removed = []
        for spec in _dest_specs(adapter.install_target):
            dest_root = self._dest_root(spec, "project", base)
            spec_rel = Path(spec.lstrip("~/")).as_posix()
            for key in entry["targets"]:
                if not (key == spec_rel or key.startswith(spec_rel + "/")):
                    continue
                rel = key[len(spec_rel):].lstrip("/")
                dst = dest_root / rel
                if not dst.is_file():
                    removed.append({"target": key, "status": "missing"})
                    continue
                if not self.dry_run:
                    self._backup(base, platform, key, dst)
                    dst.unlink()
                removed.append({"target": key, "status": "removed"})
            if not self.dry_run:
                self._prune_empty(dest_root)
        if not self.dry_run:
            manifest.remove(platform)
            manifest.save()
        return {"platform": platform, "removed": removed}

    # ---------------------------------------------------------------- drift
    def drift(self, platform: Optional[str] = None,
              base: Optional[Path] = None) -> Dict[str, Any]:
        base = Path(base) if base else self.base
        manifest = InstallManifest(base / MANIFEST_REL)
        platforms = [platform] if platform else manifest.platforms()
        if platform and platform not in manifest.all():
            raise InstallError(f"no manifest entries for platform: {platform}")
        report: Dict[str, Any] = {"clean": True, "platforms": {}}
        for name in platforms:
            entry = manifest.all()[name]
            adapter = self.registry.get(name)
            missing, modified = [], []
            for spec in _dest_specs(adapter.install_target):
                dest_root = self._dest_root(spec, "project", base)
                spec_rel = Path(spec.lstrip("~/")).as_posix()
                for key, digest in entry["targets"].items():
                    if not (key == spec_rel or key.startswith(spec_rel + "/")):
                        continue
                    rel = key[len(spec_rel):].lstrip("/")
                    dst = dest_root / rel
                    if not dst.is_file():
                        missing.append(key)
                    elif _sha256_bytes(dst.read_bytes()) != digest:
                        modified.append(key)
            if missing or modified:
                report["clean"] = False
            report["platforms"][name] = {"missing": missing, "modified": modified}
        return report

    # ------------------------------------------------------------- rollback
    def rollback(self, platform: str,
                 base: Optional[Path] = None) -> Dict[str, Any]:
        adapter = self._adapter(platform)
        base = Path(base) if base else self.base
        manifest = InstallManifest(base / MANIFEST_REL)
        entry = manifest.entry(platform)
        if entry is None:
            raise InstallError(f"not installed: {platform}")
        restored = []
        for key in entry["targets"]:
            digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
            backup = base / BACKUPS_REL / platform / f"{digest}.bak"
            dst = None
            for spec in _dest_specs(adapter.install_target):
                dest_root = self._dest_root(spec, "project", base)
                spec_rel = Path(spec.lstrip("~/")).as_posix()
                if key == spec_rel or key.startswith(spec_rel + "/"):
                    dst = dest_root / key[len(spec_rel):].lstrip("/")
                    break
            if dst is None or not backup.is_file():
                restored.append({"target": key,
                                 "status": "no-backup" if dst else "skipped"})
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=str(dst.parent), suffix=".kdesk-tmp")
            with os.fdopen(fd, "wb") as fh:
                fh.write(backup.read_bytes())
            os.replace(tmp, dst)
            restored.append({"target": key, "status": "restored"})
        return {"platform": platform, "restored": restored}

    # -------------------------------------------------------------- status
    def status(self, base: Optional[Path] = None) -> Dict[str, Any]:
        base = Path(base) if base else self.base
        manifest = InstallManifest(base / MANIFEST_REL)
        rows = []
        for platform, entry in manifest.all().items():
            rows.append({
                "platform": platform,
                "installed_at": entry.get("installed_at"),
                "targets": len(entry.get("targets", {})),
            })
        return {"installs": len(rows), "rows": rows}