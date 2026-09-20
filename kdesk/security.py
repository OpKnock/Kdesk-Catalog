"""Security: secret scanning of catalog definitions with severity + auditable exceptions."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.registry import Catalog, default_repo_root


SEVERITY_ORDER = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
SEVERITY_INDEX = {s: i for i, s in enumerate(SEVERITY_ORDER)}

# Pattern -> severity. api_key is HIGH by contract (pinned test). Secrets that
# would grant access (private keys, cloud keys, tokens) are HIGH/CRITICAL.
PATTERN_SEVERITY = {
    "api_key": "HIGH",
    "private_key": "CRITICAL",
    "aws_key": "HIGH",
    "github_token": "HIGH",
    "bearer_token": "MEDIUM",
    "password_eq": "MEDIUM",
}

_PATTERNS = {
    "api_key": r"\b(?:sk|pk|ak)[_-][A-Za-z0-9]{16,}\b",
    "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
    "github_token": r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
    "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "password_eq": r"\bpassword\s*[=:]\s*['\"][^'\"]{6,}['\"]",
    "bearer_token": r"\bBearer\s+[A-Za-z0-9\-._~+/]{16,}\b",
}

REDACTED = "***REDACTED***"


def _redacted_excerpt(text: str, pattern: str, window: int = 60) -> str:
    """Return a short snippet around the first match with the secret masked."""
    regex = _PATTERNS.get(pattern)
    if not regex:
        return ""
    redacted = re.sub(regex, REDACTED, text)
    idx = redacted.find(REDACTED)
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(redacted), idx + len(REDACTED) + window)
    snippet = redacted[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(redacted):
        snippet = snippet + "..."
    return snippet


class SecurityExceptions:
    """Persisted, auditable exceptions keyed by (definition, type, field, pattern).

    No wildcards: an exception is an exact match on all four keys, so a
    reviewer has to point at the precise location before a HIGH/CRITICAL
    finding stops blocking.
    """

    SCHEMA = "security-exceptions-v1"

    def __init__(self, entries: Optional[List[Dict[str, Any]]] = None):
        self.entries: List[Dict[str, Any]] = entries or []

    @classmethod
    def load(cls, path: Path) -> "SecurityExceptions":
        if not path.is_file():
            return cls()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return cls()
        return cls(raw.get("entries") or [])

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"schema": self.SCHEMA, "entries": self.entries}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def add(
        self,
        definition: str,
        definition_type: str,
        field: str,
        pattern: str,
        rationale: str,
        reviewer: str = "",
        date: str = "",
    ) -> None:
        for key, label in (
            (definition, "definition"),
            (definition_type, "type"),
            (field, "field"),
            (pattern, "pattern"),
        ):
            if not key or "*" in key:
                raise ValueError(f"exception {label} must be non-empty and contain no wildcards")
        entry: Dict[str, Any] = {
            "definition": definition,
            "type": definition_type,
            "field": field,
            "pattern": pattern,
            "rationale": rationale,
        }
        if reviewer:
            entry["reviewer"] = reviewer
        if date:
            entry["date"] = date
        self.entries.append(entry)

    def matches(self, finding: Dict[str, Any]) -> bool:
        for e in self.entries:
            if (
                e.get("definition") == finding.get("definition")
                and e.get("type") == finding.get("type")
                and e.get("field") == finding.get("field")
                and e.get("pattern") == finding.get("pattern")
            ):
                return True
        return False


class SecurityScanner:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    def scan(self) -> List[Dict[str, Any]]:
        findings = []
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            for field, value in self._text_fields(defn):
                hits = self._scan_text(value)
                for pattern in hits:
                    findings.append(
                        {
                            "definition": defn.name,
                            "type": defn.type,
                            "field": field,
                            "pattern": pattern,
                            "severity": PATTERN_SEVERITY.get(pattern, "MEDIUM"),
                            "excerpt": _redacted_excerpt(value, pattern),
                        }
                    )
        return findings

    def _text_fields(self, defn) -> List[tuple]:
        yield "description", defn.description
        yield "instructions", str(defn.instructions or "")
        for i, cap in enumerate(defn.capabilities):
            yield f"capabilities[{i}].commands", " ".join(cap.commands)
        for i, ex in enumerate(defn.examples):
            yield f"examples[{i}]", str(ex)

    @staticmethod
    def _scan_text(text: str) -> List[str]:
        hits = []
        for name, regex in _PATTERNS.items():
            if re.search(regex, text):
                hits.append(name)
        return hits


def scan_repo(root: Path, exceptions_path: Optional[Path] = None) -> Dict[str, Any]:
    catalog = Catalog.from_repo(root)
    scanner = SecurityScanner(catalog)
    findings = scanner.scan()
    exceptions = SecurityExceptions.load(exceptions_path) if exceptions_path else SecurityExceptions()
    blocking = [
        f
        for f in findings
        if not exceptions.matches(f) and SEVERITY_INDEX.get(f["severity"], 0) >= SEVERITY_INDEX["HIGH"]
    ]
    excepted = [f for f in findings if exceptions.matches(f)]
    severity_counts: Dict[str, int] = {}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1
    return {
        "findings": findings,
        "count": len(findings),
        "definitions_scanned": len(catalog.agents) + len(catalog.skills),
        "severity_counts": dict(
            sorted(severity_counts.items(), key=lambda kv: SEVERITY_INDEX.get(kv[0], len(SEVERITY_ORDER)))
        ),
        "exceptions_applied": exceptions_path is not None,
        "excepted_count": len(excepted),
        "blocking_count": len(blocking),
        "blocking": [
            {k: f[k] for k in ("definition", "type", "field", "pattern", "severity")} for f in blocking
        ],
    }