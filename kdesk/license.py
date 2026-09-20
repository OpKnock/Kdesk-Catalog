"""License compliance: catalog definition license audit with policy classification."""
from __future__ import annotations

import json
from collections import Counter
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.registry import Catalog


ALLOWED = {"mit", "apache-2.0", "apache-2", "bsd-3-clause", "bsd-2-clause", "cc-by-4.0", "cc0-1.0", "unlicense"}

VALID_CLASSES = {"explicit", "inherited", "third_party", "intentionally_unspecified"}


class LicenseClass(str, Enum):
    EXPLICIT = "explicit"
    INHERITED = "inherited"
    THIRD_PARTY = "third_party"
    INTENTIONALLY_UNSPECIFIED = "intentionally_unspecified"


class LicensePolicy:
    """Persisted, reviewable license classifications keyed by definition name.

    A policy entry resolves a definition's license status without editing the
    source YAML (converted catalog definitions carry no license field). Entries
    are always surfaced in reports; nothing is silently hidden.
    """

    SCHEMA = "license-policy-v1"

    def __init__(self, entries: Optional[Dict[str, Dict[str, Any]]] = None):
        self.entries: Dict[str, Dict[str, Any]] = entries or {}

    @classmethod
    def load(cls, path: Path) -> "LicensePolicy":
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
        name: str,
        license_class: str,
        rationale: str,
        license_: Optional[str] = None,
        reviewer: str = "",
        date: str = "",
    ) -> None:
        entry: Dict[str, Any] = {"class": license_class, "rationale": rationale}
        if license_:
            entry["license"] = license_
        if reviewer:
            entry["reviewer"] = reviewer
        if date:
            entry["date"] = date
        self.entries[name] = entry

    def classification_for(self, name: str) -> Optional[Dict[str, Any]]:
        return self.entries.get(name)


class LicenseAudit:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    def audit(self, policy: Optional[LicensePolicy] = None) -> Dict[str, Any]:
        counts: Counter = Counter()
        valid: List[str] = []
        inherited: List[str] = []
        third_party: List[str] = []
        unspecified: List[str] = []
        missing: List[str] = []
        unapproved: List[str] = []
        unknown: List[str] = []
        classification: Dict[str, Dict[str, Any]] = {}
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            lic = (defn.license or "").strip().lower()
            entry = policy.classification_for(defn.name) if policy else None
            cls = (entry or {}).get("class") if entry else None
            entry_license = ((entry or {}).get("license") or "").strip().lower() if entry else ""

            if lic:
                counts[lic] += 1

            if lic in ALLOWED:
                valid.append(defn.name)
            elif entry and cls not in VALID_CLASSES:
                unknown.append(defn.name)
            elif entry and cls in ("inherited", "explicit"):
                if entry_license in ALLOWED:
                    if cls == "inherited":
                        inherited.append(defn.name)
                    else:
                        valid.append(defn.name)
                        counts[entry_license] += 1
                else:
                    unknown.append(defn.name)
            elif entry and cls == "third_party":
                third_party.append(defn.name)
            elif entry and cls == "intentionally_unspecified":
                unspecified.append(defn.name)
            elif lic:
                unapproved.append(f"{defn.name} ({lic})")
            else:
                missing.append(defn.name)

            if entry:
                classification[defn.name] = {"class": cls, "rationale": entry.get("rationale", "")}
                if entry.get("license"):
                    classification[defn.name]["license"] = entry["license"]
                if entry.get("reviewer"):
                    classification[defn.name]["reviewer"] = entry["reviewer"]
                if entry.get("date"):
                    classification[defn.name]["date"] = entry["date"]

        unresolved = missing + unapproved + unknown
        return {
            "definitions": len(self.catalog.agents) + len(self.catalog.skills),
            "license_counts": dict(sorted(counts.items())),
            "valid": sorted(valid),
            "valid_count": len(valid),
            "inherited": sorted(inherited),
            "inherited_count": len(inherited),
            "third_party": sorted(third_party),
            "third_party_count": len(third_party),
            "unspecified": sorted(unspecified),
            "unspecified_count": len(unspecified),
            "missing": sorted(missing),
            "missing_count": len(missing),
            "unapproved": sorted(unapproved),
            "unapproved_count": len(unapproved),
            "unknown": sorted(unknown),
            "unknown_count": len(unknown),
            "policy_applied": policy is not None,
            "classification": dict(sorted(classification.items())),
            "unresolved": sorted(unresolved),
            "unresolved_count": len(unresolved),
            "files_scanned": len(self.catalog.agents) + len(self.catalog.skills),
        }