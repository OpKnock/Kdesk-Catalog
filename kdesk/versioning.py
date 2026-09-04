"""Agent versioning + semver resolution for installs.

Supports `kdesk install claude_code --agent my-agent@^2.0` with
version constraint checking against the catalog.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
CONSTRAINT_RE = re.compile(r"^([\^~>=<!]+)?\s*(\d+)(?:\.(\d+))?(?:\.(\d+))?$")


def parse_semver(version: str) -> Optional[Tuple[int, int, int]]:
    """Parse 'X.Y.Z' into (major, minor, patch). Returns None on failure."""
    m = SEMVER_RE.match(version.strip())
    if not m:
        return None
    return tuple(int(g) for g in m.groups())  # type: ignore


@dataclass
class Constraint:
    raw: str
    op: str = ""
    base: Tuple[int, int, int] = (0, 0, 0)

    def satisfies(self, version: str) -> bool:
        v = parse_semver(version)
        if v is None:
            return False
        b = self.base

        if self.op == "^":
            return v >= b and v[0] == b[0]
        if self.op == "~":
            return v >= b and (v[0], v[1]) == (b[0], b[1])
        if self.op in ("", "="):
            return v == b
        if self.op == ">=":
            return v >= b
        if self.op == "<=":
            return v <= b
        if self.op == ">":
            return v > b
        if self.op == "<":
            return v < b
        return True


def parse_constraint(spec: str) -> Constraint:
    """Parse a semver constraint string like '^2.0.0', '~1.2', '=1.0.0', '>1.0'.

    Partial versions are allowed: missing minor/patch default to 0
    ('^2' == '^2.0.0', '~1.2' == '~1.2.0').
    """
    spec = spec.strip()
    m = CONSTRAINT_RE.match(spec)
    if not m:
        return Constraint(raw=spec, op="", base=(0, 0, 0))
    op = m.group(1) or ""
    base = (int(m.group(2)), int(m.group(3) or 0), int(m.group(4) or 0))
    return Constraint(raw=spec, op=op, base=base)


@dataclass
class VersionedDefinition:
    name: str
    version: str
    category: str = ""

    @property
    def parsed_version(self) -> Tuple[int, int, int]:
        return parse_semver(self.version) or (0, 0, 0)


class VersionResolver:
    """Resolves agent/skill names with optional semver constraints."""

    def __init__(self):
        pass

    def resolve(self, spec: str, available: Dict[str, List[str]]) -> Optional[str]:
        """Resolve a spec like 'my-agent@^2.0' to the best matching definition name.

        Args:
            spec: Definition name, optionally with '@constraint'.
            available: Map of {base_name: [list_of_versions]}.

        Returns:
            Best matching definition name, or None.
        """
        if "@" not in spec:
            # No version constraint — exact name match or latest
            if spec in available:
                versions = sorted(available[spec], key=self._sort_key, reverse=True)
                return f"{spec}@{versions[0]}" if len(versions) > 1 else spec
            return None

        name, _, constraint_str = spec.rpartition("@")
        constraint = parse_constraint(constraint_str)

        candidates = available.get(name, [])
        matching = [v for v in candidates if constraint.satisfies(v)]
        if not matching:
            return None

        best = max(matching, key=self._sort_key)
        return f"{name}@{best}"

    @staticmethod
    def _sort_key(version: str) -> Tuple[int, int, int]:
        return parse_semver(version) or (0, 0, 0)

    def check_breaking_change(self, old_version: str, new_version: str) -> Dict[str, Any]:
        """Check if upgrading from old to new is a breaking change."""
        old_v = parse_semver(old_version)
        new_v = parse_semver(new_version)
        if old_v is None or new_v is None:
            return {"breaking": False, "reason": "unparseable version"}

        breaking = new_v[0] > old_v[0]
        minor_bump = new_v[1] > old_v[1]
        patch_bump = new_v[2] > old_v[2]

        change_type = "major" if breaking else ("minor" if minor_bump else ("patch" if patch_bump else "none"))
        return {
            "breaking": breaking,
            "change_type": change_type,
            "old": old_version,
            "new": new_version,
            "warning": f"BREAKING: major bump {old_v[0]}→{new_v[0]}" if breaking else "",
        }


def build_available_versions(catalog_definitions: Dict[str, Any]) -> Dict[str, List[str]]:
    """Build {base_name: [versions]} from catalog definitions that have version suffixes.

    Definitions named like 'foo-v2' or 'foo-2' are treated as versions of 'foo'.
    """
    import re
    result: Dict[str, List[str]] = {}

    for name in catalog_definitions.keys():
        # Try to extract version suffix: name-vN or name-N.N.N
        m = re.match(r"^(.+?)-v?(\d+(?:\.\d+)*)$", name)
        if m:
            base, ver = m.group(1), m.group(2)
            # Normalize to X.Y.Z
            parts = ver.split(".")
            while len(parts) < 3:
                parts.append("0")
            normalized = ".".join(parts[:3])
            result.setdefault(base, []).append(normalized)
        else:
            result.setdefault(name, []).append("1.0.0")

    return result
