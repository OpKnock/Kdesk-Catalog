"""Local JSON marketplace backend for skill publish/install/search/list.

Registry is a JSON file at <root>/marketplace-registry.json.
Supports versioned publishing, semver resolution, and dependency checking.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


REGISTRY_FILENAME = "marketplace-registry.json"
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RegistryEntry:
    name: str
    version: str
    description: str = ""
    category: str = ""
    author: str = ""
    checksum: str = ""
    published_at: str = ""
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "author": self.author,
            "checksum": self.checksum,
            "published_at": self.published_at,
            "dependencies": self.dependencies,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RegistryEntry":
        return cls(
            name=str(d.get("name", "")),
            version=str(d.get("version", "0.0.0")),
            description=str(d.get("description", "")),
            category=str(d.get("category", "")),
            author=str(d.get("author", "")),
            checksum=str(d.get("checksum", "")),
            published_at=str(d.get("published_at", "")),
            dependencies=list(d.get("dependencies", []) or []),
            tags=list(d.get("tags", []) or []),
        )


class Marketplace:
    """File-backed skill marketplace with publish, resolve, install."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.registry_path = self.root / REGISTRY_FILENAME

    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        if not self.registry_path.is_file():
            return {"skills": []}
        try:
            return json.loads(self.registry_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {"skills": []}

    def _save(self, data: Dict[str, Any]) -> None:
        self.registry_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    # ------------------------------------------------------------- publish
    def publish(self, yaml_path: Path, author: str = "", force: bool = False) -> Dict[str, Any]:
        import yaml

        doc = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or not doc.get("name"):
            raise ValueError(f"invalid YAML: {yaml_path}")

        name = str(doc["name"])
        version = str(doc.get("version", "1.0.0"))
        if not SEMVER_RE.match(version):
            raise ValueError(f"invalid semver: {version}")

        content = yaml_path.read_bytes()
        checksum = hashlib.sha256(content).hexdigest()[:16]

        data = self._load()
        skills = data.get("skills", [])

        existing = [s for s in skills if s["name"] == name]
        if any(s["version"] == version for s in existing) and not force:
            raise ValueError(f"{name}@{version} already published; use --force")
        if force:
            # Replace same-version entries instead of duplicating them.
            skills = [s for s in skills
                      if not (s["name"] == name and s["version"] == version)]

        deps = []
        for cap in doc.get("capabilities") or []:
            if isinstance(cap, dict):
                deps.extend(str(c) for c in cap.get("commands", []) if isinstance(c, str))
        dep_bins = sorted({c.split()[0] for c in deps if c.strip()})

        entry = RegistryEntry(
            name=name,
            version=version,
            description=str(doc.get("description", "")),
            category=str(doc.get("category", "")),
            author=author or str(doc.get("author", "anonymous")),
            checksum=checksum,
            published_at=_now_iso(),
            dependencies=dep_bins,
            tags=[str(t) for t in doc.get("tags", []) or []],
        )

        skills.append(entry.to_dict())
        data["skills"] = skills
        self._save(data)

        return {"status": "published", **entry.to_dict()}

    # -------------------------------------------------------------- resolve
    @staticmethod
    def _parse_version(v: str) -> Tuple[int, int, int]:
        m = SEMVER_RE.match(v)
        if not m:
            return (0, 0, 0)
        return tuple(int(g) for g in m.groups())  # type: ignore

    @staticmethod
    def _satisfies(version: str, spec: str) -> bool:
        spec = spec.strip()
        if spec == "*" or spec == "latest":
            return True
        if SEMVER_RE.match(spec):
            return version == spec
        m = re.match(r"^[\^~>=<]+\s*(\d+\.\d+\.\d+)$", spec)
        if not m:
            return True
        base = m.group(1)
        op = spec[: len(spec) - len(base)].strip()
        v, b = Marketplace._parse_version(version), Marketplace._parse_version(base)
        if op == "^":
            return v >= b and v[0] == b[0]
        if op == "~":
            return v >= b and (v[0], v[1]) == (b[0], b[1])
        if op == ">=":
            return v >= b
        if op == "<=":
            return v <= b
        if op == ">":
            return v > b
        if op == "<":
            return v < b
        return False

    def resolve(self, spec: str) -> Optional[RegistryEntry]:
        """Resolve a 'name' or 'name@semver-range' to the best matching entry."""
        if "@" in spec:
            name, range_spec = spec.rsplit("@", 1)
        else:
            name, range_spec = spec, "*"

        data = self._load()
        matches = [
            RegistryEntry.from_dict(s)
            for s in data.get("skills", [])
            if s["name"] == name and self._satisfies(s["version"], range_spec)
        ]
        if not matches:
            return None
        matches.sort(key=lambda e: self._parse_version(e.version), reverse=True)
        return matches[0]

    # --------------------------------------------------------------- search
    def search(self, query: str = "", limit: int = 20) -> List[RegistryEntry]:
        data = self._load()
        entries = [RegistryEntry.from_dict(s) for s in data.get("skills", [])]
        q = query.lower().strip()
        if not q:
            entries.sort(key=lambda e: e.published_at, reverse=True)
            return entries[:limit]

        scored: List[Tuple[int, RegistryEntry]] = []
        terms = q.split()
        for e in entries:
            hay = f"{e.name} {e.description} {e.category} {' '.join(e.tags)}".lower()
            score = sum(1 for t in terms if t in hay)
            if score > 0:
                scored.append((score, e))
        scored.sort(key=lambda x: (-x[0], x[1].name))
        return [e for _, e in scored[:limit]]

    # ----------------------------------------------------------------- list
    def list_all(self, limit: int = 100) -> List[RegistryEntry]:
        data = self._load()
        seen: Dict[str, RegistryEntry] = {}
        for s in data.get("skills", []):
            e = RegistryEntry.from_dict(s)
            key = e.name
            if key not in seen or self._parse_version(e.version) > self._parse_version(seen[key].version):
                seen[key] = e
        result = sorted(seen.values(), key=lambda e: e.name)
        return result[:limit]

    # ---------------------------------------------------------------- stats
    def stats(self) -> Dict[str, int]:
        data = self._load()
        skills = data.get("skills", [])
        names = {s["name"] for s in skills}
        return {"total_versions": len(skills), "unique_skills": len(names)}
