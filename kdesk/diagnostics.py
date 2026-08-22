"""Diagnostic models for Kdesk Doctor."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from pathlib import Path


# Secret redaction patterns
SECRET_PATTERNS = [
    (re.compile(r'(?i)(api[_-]?key|token|password|secret|credential)[\s:=]+[\w\-]+'), '***REDACTED***'),
    (re.compile(r'(?i)(api[_-]?key|token|password|secret|credential)[\s:=]+\"[\w\-]+\"'), '"***REDACTED***"'),
    # Only redact very long strings that are likely keys (40+ chars, not file paths)
    (re.compile(r'(?<![\w\-\.\/])[\w\-]{40,}(?![\w\-\.\/])'), '***REDACTED***'),
]

def redact_secrets(text: str) -> str:
    """Redact potential secrets from text."""
    if not isinstance(text, str):
        return text
    result = text
    for pattern, replacement in SECRET_PATTERNS:
        result = pattern.sub(replacement, result)
    return result

def redact_dict_secrets(d: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively redact secrets from dictionary."""
    if not isinstance(d, dict):
        return redact_secrets(d) if isinstance(d, str) else d
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = redact_dict_secrets(v)
        elif isinstance(v, list):
            result[k] = [redact_dict_secrets(item) if isinstance(item, dict) else redact_secrets(item) if isinstance(item, str) else item for item in v]
        elif isinstance(v, str):
            result[k] = redact_secrets(v)
        else:
            result[k] = v
    return result


class Severity(str, Enum):
    """Issue severity levels."""
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

    def weight(self) -> int:
        return {"CRITICAL": 10, "ERROR": 5, "WARNING": 2, "INFO": 1}[self.value]


class Category(str, Enum):
    """Issue categories."""
    UNSUPPORTED_FIELD = "unsupported_field"
    UNSUPPORTED_TOOL = "unsupported_tool"
    UNSUPPORTED_METADATA = "unsupported_metadata"
    INVALID_STRUCTURE = "invalid_structure"
    PLATFORM_SYNTAX = "platform_syntax"
    MISSING_REQUIRED = "missing_required"
    MISSING_DEPENDENCY = "missing_dependency"
    UNSUPPORTED_WORKFLOW = "unsupported_workflow"
    INCOMPATIBLE_SKILL = "incompatible_skill"
    INCOMPATIBLE_AGENT = "incompatible_agent"
    INVALID_CONFIG = "invalid_config"
    MISSING_REQUIRED_METADATA = "missing_required_metadata"
    PLATFORM_MISMATCH = "platform_mismatch"
    VALIDATION_FAILURE = "validation_failure"


@dataclass
class Issue:
    """A compatibility or validation issue."""
    id: str
    severity: Severity
    category: Category
    file: str
    line: Optional[int] = None
    column: Optional[int] = None
    component: str = ""
    platform: str = ""
    message: str = ""
    reason: str = ""
    suggested_fix: str = ""
    fixable: bool = False
    fix_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return redact_dict_secrets({
            "id": self.id,
            "severity": self.severity.value,
            "category": self.category.value,
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "component": self.component,
            "platform": self.platform,
            "message": self.message,
            "reason": self.reason,
            "suggested_fix": self.suggested_fix,
            "fixable": self.fixable,
            "fix_data": self.fix_data,
        })


@dataclass
class ComponentReport:
    """Report for a single component (agent/skill/workflow)."""
    name: str
    type: str  # agent, skill, workflow, command, config
    file: str
    platform: str
    issues: List[Issue] = field(default_factory=list)
    supported: bool = True

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity in (Severity.CRITICAL, Severity.ERROR))

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.INFO)

    @property
    def fixable_count(self) -> int:
        return sum(1 for i in self.issues if i.fixable)


@dataclass
class DiagnosticReport:
    """Complete diagnostic report for a project."""
    project_root: str
    platform: str
    score: int = 0
    max_score: int = 100
    components: List[ComponentReport] = field(default_factory=list)
    issues: List[Issue] = field(default_factory=list)
    scan_metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_components(self) -> int:
        return len(self.components)

    @property
    def total_issues(self) -> int:
        return len(self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity in (Severity.CRITICAL, Severity.ERROR))

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.INFO)

    @property
    def fixable_count(self) -> int:
        return sum(1 for i in self.issues if i.fixable)

    def to_dict(self) -> Dict[str, Any]:
        return redact_dict_secrets({
            "project_root": self.project_root,
            "platform": self.platform,
            "score": self.score,
            "max_score": self.max_score,
            "components": [
                {
                    "name": c.name,
                    "type": c.type,
                    "file": c.file,
                    "platform": c.platform,
                    "supported": c.supported,
                    "issues": [i.to_dict() for i in c.issues],
                    "error_count": c.error_count,
                    "warning_count": c.warning_count,
                    "info_count": c.info_count,
                    "fixable_count": c.fixable_count,
                }
                for c in self.components
            ],
            "issues": [i.to_dict() for i in self.issues],
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "fixable_count": self.fixable_count,
            "scan_metadata": self.scan_metadata,
        })

    def to_summary_dict(self) -> Dict[str, Any]:
        """Minimal summary for CLI output."""
        return {
            "project_root": self.project_root,
            "platform": self.platform,
            "score": self.score,
            "max_score": self.max_score,
            "components": self.total_components,
            "errors": self.error_count,
            "warnings": self.warning_count,
            "info": self.info_count,
            "fixable": self.fixable_count,
        }


@dataclass
class FixResult:
    """Result of applying a fix."""
    issue_id: str
    success: bool
    message: str
    backup_path: Optional[str] = None
    validation_passed: bool = False
    new_issues: List[Issue] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return redact_dict_secrets({
            "issue_id": self.issue_id,
            "success": self.success,
            "message": self.message,
            "backup_path": self.backup_path,
            "validation_passed": self.validation_passed,
            "new_issues": [i.to_dict() for i in self.new_issues],
        })


@dataclass
class FixReport:
    """Report of all fixes applied."""
    project_root: str
    platform: str
    before_score: int
    after_score: int
    fixes: List[FixResult] = field(default_factory=list)
    manual_actions: List[str] = field(default_factory=list)

    @property
    def successful(self) -> int:
        return sum(1 for f in self.fixes if f.success)

    @property
    def failed(self) -> int:
        return sum(1 for f in self.fixes if not f.success)

    @property
    def validation_passed(self) -> int:
        return sum(1 for f in self.fixes if f.validation_passed)

    def to_dict(self) -> Dict[str, Any]:
        return redact_dict_secrets({
            "project_root": self.project_root,
            "platform": self.platform,
            "before_score": self.before_score,
            "after_score": self.after_score,
            "fixes": [f.to_dict() for f in self.fixes],
            "manual_actions": self.manual_actions,
            "successful": self.successful,
            "failed": self.failed,
            "validation_passed": self.validation_passed,
        })