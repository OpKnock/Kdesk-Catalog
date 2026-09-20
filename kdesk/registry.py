"""Catalog registry: loads and indexes the Kdesk universal-agents corpus.

Repo layout (either of the two coexisting shapes):
  universal-agents/<family>/agent/<name>.yaml
  universal-agents/<family>/skill/<name>.yaml
  universal-agents/<family>/<name>.yaml            (flat; skills end with -skill.yaml)
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from kdesk.models import Agent, Capability, Skill


class CatalogError(Exception):
    pass


def default_repo_root() -> Path:
    """Repo root derived from the package location or current working directory.
    Walks up from CWD to find universal-agents; falls back to package location."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / "universal-agents").is_dir():
            return parent
    # Fallback: package location (for installed package)
    return Path(__file__).resolve().parents[1]


class Catalog:
    """In-memory catalog with a mtime-keyed cache.

    Cache correctness: the tree key covers the full sorted YAML file list with
    per-file mtime+size, so ANY catalog change invalidates the cache. Repeated
    loads of an unchanged tree are free.
    """

    _cache: Dict[str, "Catalog"] = {}
    _cache_key: Dict[str, str] = {}

    def __init__(self, universal_dir: Path):
        self.universal_dir = Path(universal_dir)
        self.agents: Dict[str, Agent] = {}
        self.skills: Dict[str, Skill] = {}
        self.errors: List[str] = []
        self._load()

    @classmethod
    def from_repo(cls, root: Optional[Path] = None) -> "Catalog":
        root = Path(root) if root else default_repo_root()
        universal = root / "universal-agents"
        key = cls._tree_key(universal)
        cached = cls._cache.get(str(root))
        if cached is not None and cls._cache_key.get(str(root)) == key:
            return cached
        catalog = cls(universal)
        cls._cache[str(root)] = catalog
        cls._cache_key[str(root)] = key
        return catalog

    @staticmethod
    def _tree_key(universal: Path) -> str:
        if not universal.is_dir():
            return "missing"
        files = sorted(universal.rglob("*.yaml"))
        digest = hashlib.sha256()
        digest.update(len(files).to_bytes(4, "big"))
        for path in files:
            st = path.stat()
            rel = str(path.relative_to(universal)).replace("\\", "/")
            digest.update(rel.encode("utf-8"))
            digest.update(str(st.st_mtime_ns).encode("utf-8"))
            digest.update(str(st.st_size).encode("utf-8"))
        return digest.hexdigest()[:16]

    # ------------------------------------------------------------------ load
    def _load(self) -> None:
        if not self.universal_dir.is_dir():
            raise CatalogError(f"universal dir not found: {self.universal_dir}")
        cached_docs = self._load_parse_cache()
        if cached_docs is not None:
            for rel, doc in cached_docs:
                path = self.universal_dir / rel
                try:
                    defn = self._classify_and_build(path, doc)
                except Exception as exc:  # keep going, record the failure
                    self.errors.append(f"{path}: {exc}")
                    continue
                if isinstance(defn, Agent):
                    self._register(self.agents, defn, "agent")
                elif isinstance(defn, Skill):
                    self._register(self.skills, defn, "skill")
            return
        parsed: list = []
        yaml_files = sorted(self.universal_dir.rglob("*.yaml"))
        if not yaml_files:
            raise CatalogError(f"no YAML files found under {self.universal_dir}")
        for path in yaml_files:
            if path.name == "registry.yaml":
                continue
            try:
                doc = self._load_yaml(path)
            except Exception as exc:  # keep going, record the failure
                self.errors.append(f"{path}: {exc}")
                continue
            rel = str(path.relative_to(self.universal_dir)).replace("\\", "/")
            parsed.append((rel, doc))
            defn = self._classify_and_build(path, doc)
            if isinstance(defn, Agent):
                self._register(self.agents, defn, "agent")
            elif isinstance(defn, Skill):
                self._register(self.skills, defn, "skill")
        self._save_parse_cache(parsed)

    @staticmethod
    def _cache_path(universal_dir: Path) -> Path:
        # lives under gitignored .kdesk/runtime; keyed by tree hash (see from_repo)
        return universal_dir.parent / ".kdesk" / "runtime" / "catalog-parse-cache-v1.pkl"

    def _load_parse_cache(self):
        """Return [(rel_path, doc)] if a valid cache exists, else None.

        Validity is bound to the tree key (file list + mtime + size), so any
        catalog edit invalidates. All failures fall back to a full reparse —
        the cache can never break loading.
        """
        import pickle

        try:
            from kdesk.registry import Catalog as _Cls
            key = _Cls._tree_key(self.universal_dir)
            cache_file = self._cache_path(self.universal_dir)
            if not cache_file.is_file():
                return None
            with open(cache_file, "rb") as fh:
                payload = pickle.load(fh)
            if (not isinstance(payload, dict) or payload.get("key") != key
                    or payload.get("version") != 1):
                return None
            docs = payload.get("docs")
            if not isinstance(docs, list) or not docs:
                return None
            return docs
        except Exception:
            return None

    def _save_parse_cache(self, parsed: list) -> None:
        import pickle

        try:
            from kdesk.registry import Catalog as _Cls
            cache_file = self._cache_path(self.universal_dir)
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            tmp = cache_file.with_suffix(".tmp")
            with open(tmp, "wb") as fh:
                pickle.dump({"version": 1,
                             "key": _Cls._tree_key(self.universal_dir),
                             "docs": parsed}, fh,
                            protocol=pickle.HIGHEST_PROTOCOL)
            tmp.replace(cache_file)
        except Exception:
            pass

    @staticmethod
    def _load_yaml(path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        doc = yaml.safe_load(content)
        if not isinstance(doc, dict):
            raise CatalogError("not a mapping")
        return doc

    def _classify_and_build(self, path: Path, doc: dict) -> Agent | Skill:
        rel = str(path.relative_to(self.universal_dir)).replace("\\", "/")
        type_hint = str(doc.get("type", ""))
        if type_hint == "skill" or "/skill/" in rel or rel.endswith("-skill.yaml"):
            defn: Agent | Skill = Skill(
                name=str(doc.get("name", "")),
                display_name=str(doc.get("display_name", "")),
                category=str(doc.get("category", "")),
                subcategory=doc.get("subcategory"),
                description=str(doc.get("description", "")),
                version=str(doc.get("version", "")),
                tags=list(doc.get("tags", []) or []),
                keywords=list(doc.get("keywords", []) or []),
                author=doc.get("author"),
                license=doc.get("license"),
                created_at=doc.get("created_at"),
                updated_at=doc.get("updated_at"),
                capabilities=[Capability.from_dict(c) for c in (doc.get("capabilities") or []) if isinstance(c, dict)],
                knowledge=list(doc.get("knowledge", []) or []),
                instructions=doc.get("instructions"),
                examples=list(doc.get("examples", []) or []),
                platforms=doc.get("platforms", {}) or {},
                source_path=path,
                raw=doc,
            )
            defn.tools = list(doc.get("tools", []) or [])
            defn.prerequisites = list(doc.get("prerequisites", []) or [])
            return defn
        agent = Agent(
            name=str(doc.get("name", "")),
            display_name=str(doc.get("display_name", "")),
            category=str(doc.get("category", "")),
            subcategory=doc.get("subcategory"),
            description=str(doc.get("description", "")),
            version=str(doc.get("version", "")),
            tags=list(doc.get("tags", []) or []),
            keywords=list(doc.get("keywords", []) or []),
            author=doc.get("author"),
            license=doc.get("license"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
            capabilities=[Capability.from_dict(c) for c in (doc.get("capabilities") or []) if isinstance(c, dict)],
            knowledge=list(doc.get("knowledge", []) or []),
            instructions=doc.get("instructions"),
            examples=list(doc.get("examples", []) or []),
            platforms=doc.get("platforms", {}) or {},
            source_path=path,
            raw=doc,
        )
        agent.skills = list(doc.get("skills", []) or [])
        agent.tools = list(doc.get("tools", []) or [])
        agent.prerequisites = list(doc.get("prerequisites", []) or [])
        agent.sub_agents = list(doc.get("sub_agents", []) or [])
        agent.delegation_pattern = doc.get("delegation_pattern")
        return agent

    @staticmethod
    def _register(store: Dict[str, BaseDefinition], defn: BaseDefinition, kind: str) -> None:  # noqa: F821
        if defn.name in store:
            raise CatalogError(f"duplicate {kind} name: {defn.name}")
        store[defn.name] = defn

    # ---------------------------------------------------------------- queries
    def get(self, name: str) -> Optional[Agent | Skill]:
        return self.agents.get(name) or self.skills.get(name)

    def get_agent(self, name: str) -> Optional[Agent]:
        return self.agents.get(name)

    def get_skill(self, name: str) -> Optional[Skill]:
        return self.skills.get(name)

    def search(self, query: str, fields: Optional[List[str]] = None) -> List[Agent | Skill]:
        q = query.lower()
        fields = fields or ["name", "display_name", "description", "tags", "keywords", "category"]
        hits = []
        for defn in list(self.agents.values()) + list(self.skills.values()):
            haystack = " ".join(
                str(getattr(defn, f, "")) for f in fields if getattr(defn, f, None) is not None
            ).lower()
            if q in haystack:
                hits.append(defn)
        return hits

    def by_category(self, category: str) -> Dict[str, List[BaseDefinition]]:  # noqa: F821
        return {
            "agents": [a for a in self.agents.values() if a.category == category],
            "skills": [s for s in self.skills.values() if s.category == category],
        }

    def stats(self) -> Dict[str, int]:
        return {
            "agents": len(self.agents),
            "skills": len(self.skills),
            "total": len(self.agents) + len(self.skills),
            "errors": len(self.errors),
            "files_scanned": len(self.agents) + len(self.skills) + len(self.errors),
        }

    def checksum(self, name: str) -> Optional[str]:
        defn = self.get(name)
        if defn is None or defn.source_path is None:
            return None
        return hashlib.sha256(defn.source_path.read_bytes()).hexdigest()[:16]