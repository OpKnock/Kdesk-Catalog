"""Quality scoring: content-quality gates per definition."""
from __future__ import annotations

from typing import Any, Dict, List

from kdesk.registry import Catalog


class QualityReport:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    def score(self) -> Dict[str, Any]:
        scores: List[Dict[str, Any]] = []
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            points = 0
            checks = []
            if defn.description and len(defn.description) >= 200:
                points += 1
                checks.append("description>=200ch")
            if defn.capabilities:
                points += 1
                checks.append("has_capabilities")
            if any(c.commands for c in defn.capabilities):
                points += 1
                checks.append("has_commands")
            if any(c.parameters for c in defn.capabilities):
                points += 1
                checks.append("has_parameters")
            if defn.examples:
                points += 1
                checks.append("has_examples")
            if defn.instructions:
                points += 1
                checks.append("has_instructions")
            if defn.version:
                points += 1
                checks.append("has_version")
            if defn.license:
                points += 1
                checks.append("has_license")
            if defn.platforms:
                points += 1
                checks.append("has_platforms")
            scores.append(
                {
                    "definition": defn.name,
                    "type": defn.type,
                    "score": points,
                    "max": 9,
                    "checks": checks,
                }
            )
        scores.sort(key=lambda s: (s["score"], s["definition"]))
        low = [s for s in scores if s["score"] < 5]
        return {
            "definitions": len(scores),
            "scores": scores,
            "low_score": low,
            "low_score_count": len(low),
            "files_scanned": len(scores),
        }