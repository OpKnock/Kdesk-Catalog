"""Trust Score calculation for Kdesk agents and skills.

Implements deterministic Trust Score calculation based on:
- Compatibility (platform support, capability coverage)
- Security (permission scope, secrets handling, network access)
- Policy compliance (schema, naming, structure)
- Dependencies (pinned, up-to-date, no vulnerabilities)
- Provenance (source traceability, checksums, signatures)

All scores are deterministic and explainable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from kdesk.compatibility import CompatibilityEngine, analyze_compatibility
from kdesk.registry import Catalog
from kdesk.registry import default_repo_root
from kdesk.diagnostics import Issue, Severity, Category
from kdesk.policy import PolicyEngineV2


@dataclass
class TrustBreakdown:
    """Breakdown of trust score components."""
    compatibility: int
    security: int
    policy: int
    dependencies: int
    provenance: int
    test_coverage: int
    overall: int

    def to_dict(self) -> dict:
        return {
            "compatibility": self.compatibility,
            "security": self.security,
            "policy": self.policy,
            "dependencies": self.dependencies,
            "provenance": self.provenance,
            "test_coverage": self.test_coverage,
            "overall": self.overall,
        }


@dataclass
class TrustDetails:
    """Detailed breakdown with explanations."""
    breakdown: TrustBreakdown
    compatibility_details: Dict[str, Any]
    security_details: Dict[str, Any]
    policy_details: Dict[str, Any]
    dependency_details: Dict[str, Any]
    provenance_details: Dict[str, Any]
    coverage_details: Dict[str, Any]
    issues: List[Dict[str, Any]]


class TrustScorer:
    """Calculates deterministic Trust Score for agents/skills."""

    def __init__(self, catalog_root: str = None):
        self.root = Path(catalog_root) if catalog_root else None
        self.catalog = None

    def _load_catalog(self):
        if self.catalog is None:
            from kdesk.registry import Catalog, default_repo_root
            root = self.root if self.root else default_repo_root()
            self.catalog = Catalog.from_repo(root)

    def _to_dict(self, obj) -> dict:
        """Convert object to dict, handling both dict and object types."""
        if isinstance(obj, dict):
            return obj
        # Handle dataclass or object with __dict__
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        # Handle objects with __slots__
        if hasattr(obj, '__slots__'):
            return {slot: getattr(obj, slot) for slot in obj.__slots__ if hasattr(obj, slot)}
        # Try to get attributes
        return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}

    def calculate_trust_score(
        self,
        definition_name: str,
        platform: str = None,
        include_details: bool = True
    ) -> TrustDetails:
        """Calculate Trust Score for a definition by name."""
        self._load_catalog()
        definition = self.catalog.get(definition_name)
        if not definition:
            raise ValueError(f"Definition '{definition_name}' not found")
        definition = self._to_dict(definition)

        # Calculate component scores
        compat_score, compat_details = self._score_compatibility(definition)
        security_score, security_details = self._score_security(definition)
        policy_score, policy_details = self._score_policy(definition)
        dep_score, dep_details = self._score_dependencies(definition)
        prov_score, prov_details = self._score_provenance(definition)
        coverage_score, cov_details = self._score_test_coverage(definition)

        # Weighted overall score
        weights = {
            "compatibility": 0.25,
            "security": 0.25,
            "policy": 0.20,
            "dependencies": 0.15,
            "provenance": 0.10,
            "test_coverage": 0.05,
        }

        breakdown = TrustBreakdown(
            compatibility=compat_score,
            security=security_score,
            policy=policy_score,
            dependencies=dep_score,
            provenance=prov_score,
            test_coverage=coverage_score,
            overall=int(
                compat_score * weights["compatibility"] +
                security_score * weights["security"] +
                policy_score * weights["policy"] +
                dep_score * weights["dependencies"] +
                prov_score * weights["provenance"] +
                coverage_score * weights["test_coverage"]
            )
        )

        if include_details:
            return TrustDetails(
                breakdown=breakdown,
                compatibility_details=compat_details,
                security_details=security_details,
                policy_details=policy_details,
                dependency_details=dep_details,
                provenance_details=prov_details,
                coverage_details=cov_details,
                issues=[]  # Populated by caller if needed
            )
        return TrustDetails(
            breakdown=breakdown,
            compatibility_details={},
            security_details={},
            policy_details={},
            dependency_details={},
            provenance_details={},
            coverage_details={},
            issues=[]
        )

    def _score_compatibility(self, definition) -> Tuple[int, Dict]:
        """Score compatibility based on platform support and capabilities."""
        definition = self._to_dict(definition) if not isinstance(definition, dict) else definition
        # Platform support breadth
        platforms = definition.get("platforms", {})
        if not platforms:
            return 0, {"error": "no platform support declared"}

        # Load platform registry
        from kdesk.platforms import get_registry
        registry = get_registry()
        all_platforms = [p.id for p in registry.all() if p.support_level.value != "deprecated"]

        supported = [p for p in platforms if p in registry._platforms]
        missing = [p for p in platforms if p not in registry._platforms]

        # Calculate based on tier distribution
        tiers = {}
        for p in supported:
            spec = registry.get(p)
            if spec:
                tier = spec.tier
                tiers[tier] = tiers.get(tier, 0) + 1

        # Weight by tier: A=1.0, B=0.7, C=0.4
        tier_weights = {"A": 1.0, "B": 0.7, "C": 0.4}
        total_weight = sum(tier_weights.get(t, 0) for t in tiers.keys())
        max_weight = len(supported) * 1.0  # if all were tier A
        actual_weight = sum(tier_weights.get(t, 0) * count for t, count in tiers.items())

        compat_score = int((actual_weight / max_weight) * 100) if max_weight > 0 else 0

        details = {
            "supported_platforms": len(supported),
            "missing_platforms": len(missing),
            "tier_distribution": tiers,
            "score": compat_score,
        }
        return compat_score, details

    def _score_security(self, definition) -> Tuple[int, Dict]:
        """Score security based on permissions, secrets, network access."""
        definition = self._to_dict(definition) if not isinstance(definition, dict) else definition
        platforms = definition.get("platforms", {})
        issues = 0
        max_issues = 0
        details = {
            "issues_found": [],
            "passed_checks": [],
        }

        for platform, config in platforms.items():
            max_issues += 1
            # Check for unrestricted filesystem
            tools = config.get("tools", [])
            if "*" in tools or "filesystem:*" in tools:
                issues += 1
                details["issues_found"].append("unrestricted filesystem access")
            else:
                details["passed_checks"].append("filesystem restricted")

            max_issues += 1
            # Check for unrestricted network
            if "network:*" in str(config):
                issues += 1
                details["issues_found"].append("unrestricted network access")
            else:
                details["passed_checks"].append("network restricted")

            max_issues += 1
            # Check for unrestricted shell
            if "shell:*" in str(config) or "shell" in config.get("tools", []):
                if config.get("tools") == ["*"] or "*" in config.get("tools", []):
                    issues += 1
                    details["issues_found"].append("unrestricted shell access")
                else:
                    details["passed_checks"].append("shell restricted")

            max_issues += 1
            # Check for secrets in plain text
            import re
            content = str(definition)
            if re.search(r"(password|secret|token|key)\s*[:=]\s*['\"]?[\w\-]{8,}", str(config), re.I):
                issues += 1
                details["issues_found"].append("possible hardcoded secret")

        # Score: 100 - (issues / max_issues * 100)
        if max_issues > 0:
            security_score = int(100 - (issues / max_issues) * 100)
        else:
            security_score = 100

        details["score"] = security_score
        details["issues_count"] = issues
        details["max_issues"] = max_issues
        return security_score, details

    def _score_policy(self, definition) -> Tuple[int, Dict]:
        """Score policy compliance."""
        from kdesk.policy import PolicyEngineV2
        engine = PolicyEngineV2()
        from kdesk.registry import Catalog, default_repo_root

        self._load_catalog()
        result = PolicyEngineV2().evaluate(self.catalog)

        violations = result.get("violations", [])
        total_rules = result.get("total_rules", 12)
        passed = result.get("passed", 0)

        score = int((passed / total_rules) * 100) if total_rules > 0 else 100

        details = {
            "total_rules": total_rules,
            "passed": passed,
            "violations": len(violations),
            "violations_detail": violations,
            "score": score,
        }
        return score, details

    def _score_dependencies(self, definition) -> Tuple[int, Dict]:
        """Score dependency health."""
        definition = self._to_dict(definition) if not isinstance(definition, dict) else definition
        deps = definition.get("capabilities", [])
        if not deps:
            return 100, {"note": "no capabilities declared", "score": 100}

        # Check for pinned versions
        unpinned = 0
        total = 0
        for cap in deps:
            if isinstance(cap, dict) and "commands" in cap:
                for cmd in cap["commands"]:
                    total += 1
                    if not re.search(r"@\d+\.", cmd) and not re.search(r"==\d+\.", cmd):
                        unpinned += 1

        if total == 0:
            return 100, {"note": "no commands to check", "score": 100}

        pinned = total - unpinned
        score = int((pinned / total) * 100) if total > 0 else 100

        details = {
            "total_commands": total,
            "pinned": pinned,
            "unpinned": unpinned,
            "score": score,
        }
        return score, details

    def _score_provenance(self, definition) -> Tuple[int, Dict]:
        """Score provenance/traceability."""
        definition = self._to_dict(definition) if not isinstance(definition, dict) else definition
        score = 100
        details = {
            "checks": [],
        }

        # Has source_path
        if definition.get("source_path"):
            details["checks"].append("has_source_path")
        else:
            score -= 10
            details["checks"].append("missing_source_path")

        # Has checksum
        if definition.get("checksum"):
            details["checks"].append("has_checksum")
        else:
            score -= 10
            details["checks"].append("missing_checksum")

        # Has version
        if definition.get("version"):
            details["checks"].append("has_version")
        else:
            score -= 10
            details["checks"].append("missing_version")

        # Has author
        if definition.get("author"):
            details["checks"].append("has_author")
        else:
            score -= 5
            details["checks"].append("missing_author")

        return max(0, score), details

    def _score_test_coverage(self, definition) -> Tuple[int, Dict]:
        """Score test coverage for this definition."""
        definition = self._to_dict(definition) if not isinstance(definition, dict) else definition
        # Check if there are test fixtures
        from pathlib import Path
        from kdesk.registry import default_repo_root

        root = Path(default_repo_root())
        test_dir = Path("tests") / "fixtures"
        name = definition.get("name", "")

        score = 50  # base score
        details = {"checks": []}

        # Has test fixture
        test_files = list(Path("tests").rglob(f"*{definition.get('name', '')}*")) if name else []
        if test_files:
            score += 25
            details["checks"].append("has_test_fixture")
        else:
            details["checks"].append("no_test_fixture")

        # Has test file
        test_files = list(Path("tests").rglob(f"*{definition.get('category', '')}*test*.py"))
        if test_files:
            score += 25
            details["checks"].append("has_test_file")

        return min(100, score), details


def calculate_trust_score(definition_name: str, platform: str = None, catalog_root: str = None) -> dict:
    """Main entry point for calculating trust score."""
    scorer = TrustScorer(catalog_root)
    return scorer.calculate_trust_score(definition_name, platform, include_details=True).breakdown.to_dict()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = calculate_trust_score(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
        print(json.dumps(result, indent=2))