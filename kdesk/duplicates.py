"""Duplicates: near-duplicate family detection with persisted classifications."""
from __future__ import annotations

import difflib
import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from kdesk.registry import Catalog


class DuplicateClass(str, Enum):
    KEEP_VARIANT = "keep_variant"
    MERGE = "merge"
    ALIAS = "alias"
    INTENTIONAL_DUPLICATE = "intentional_duplicate"
    FALSE_POSITIVE = "false_positive"


class DuplicatePolicy:
    """Persisted, reviewable duplicate-family classifications keyed by family id.

    A family id is the sorted member names joined by '|', so entries survive
    any deterministic re-detection ordering. A classification documents a human
    review decision; it never modifies or deletes source files by itself.
    """

    SCHEMA = "duplicate-classifications-v1"

    def __init__(self, entries: Optional[Dict[str, Dict[str, Any]]] = None):
        self.entries: Dict[str, Dict[str, Any]] = entries or {}

    @classmethod
    def family_id(cls, members: List[str]) -> str:
        return "|".join(sorted(members))

    @classmethod
    def load(cls, path: Path) -> "DuplicatePolicy":
        if not path.is_file():
            return cls()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return cls()
        return cls(raw.get("entries") or {})

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"schema": self.SCHEMA, "entries": self.entries}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def set_entry(
        self,
        family_id: str,
        dup_class: str,
        rationale: str,
        members: Optional[List[str]] = None,
        reviewer: str = "",
        date: str = "",
    ) -> None:
        entry: Dict[str, Any] = {"class": dup_class, "rationale": rationale}
        if members:
            entry["members"] = members
        if reviewer:
            entry["reviewer"] = reviewer
        if date:
            entry["date"] = date
        self.entries[family_id] = entry

    def classification_for(self, family_id: str) -> Optional[Dict[str, Any]]:
        return self.entries.get(family_id)


class DuplicateDetector:
    def __init__(self, catalog: Catalog, threshold: float = 0.85):
        self.catalog = catalog
        self.threshold = threshold

    def detect(self, policy: Optional[DuplicatePolicy] = None) -> Dict[str, Any]:
        definitions = list(self.catalog.agents.values()) + list(self.catalog.skills.values())
        families: List[List[Tuple[str, str]]] = []  # [(name, signature)]
        checked: set = set()
        # O(n^2) over 2,900+ definitions is prohibitive. Group candidates by
        # (type, category, rounded length) and gate with quick_ratio so full
        # SequenceMatcher runs only on plausible near-duplicates.
        buckets: Dict[Tuple[str, str, int], List] = {}
        for d in definitions:
            key = (d.type, d.category or "", len(d.description or "") // 20)
            buckets.setdefault(key, []).append(d)
        for bucket in buckets.values():
            for i, a in enumerate(bucket):
                if a.name in checked:
                    continue
                family = [(a.name, a.description or "")]
                for j, b in enumerate(bucket):
                    if i == j or b.name in checked:
                        continue
                    da, db = a.description or "", b.description or ""
                    if abs(len(da) - len(db)) > 0.25 * max(len(da), len(db), 1):
                        continue
                    sm = difflib.SequenceMatcher(None, da, db)
                    if sm.quick_ratio() < self.threshold:
                        continue
                    if sm.ratio() >= self.threshold:
                        family.append((b.name, db))
                        checked.add(b.name)
                if len(family) > 1:
                    families.append(family)
                checked.add(a.name)

        report_families: List[Dict[str, Any]] = []
        classified_count = 0
        unresolved_ids: List[str] = []
        for fam in families:
            members = [m[0] for m in fam]
            fid = DuplicatePolicy.family_id(members)
            entry = policy.classification_for(fid) if policy else None
            family: Dict[str, Any] = {
                "id": fid,
                "members": members,
                "similarity": ">= {:.0%}".format(self.threshold),
            }
            if entry:
                classified_count += 1
                family["class"] = entry.get("class")
                if entry.get("rationale"):
                    family["rationale"] = entry["rationale"]
            else:
                unresolved_ids.append(fid)
            report_families.append(family)

        report_families.sort(key=lambda f: f["id"])
        unresolved_ids.sort()

        return {
            "families": report_families,
            "family_count": len(report_families),
            "definitions_scanned": len(definitions),
            "policy_applied": policy is not None,
            "classified_count": classified_count,
            "unresolved_count": len(unresolved_ids),
            "unresolved_families": unresolved_ids,
        }