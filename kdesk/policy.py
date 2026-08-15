"""Runtime policy: risk classes, policy decisions, and the approval store.

Risk classes (master spec): SAFE, REVIEW_REQUIRED, DANGEROUS, BLOCKED.
Approval states: PENDING_APPROVAL, APPROVED, REJECTED, AUTO_APPROVED, BLOCKED.
Decisions are deterministic: deny rules win, then risk vs threshold.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.models import PermissionClass

RISK_ORDER = ["safe", "review_required", "dangerous", "blocked"]


def risk_index(risk: str) -> int:
    try:
        return RISK_ORDER.index(risk)
    except ValueError:
        return 0


def permission_to_risk(permission: PermissionClass) -> str:
    mapping = {
        PermissionClass.READ_ONLY: "safe",
        PermissionClass.SAFE_WRITE: "review_required",
        PermissionClass.MODERATE: "review_required",
        PermissionClass.DESTRUCTIVE: "dangerous",
        PermissionClass.PRIVILEGED: "blocked",
    }
    return mapping.get(permission, "review_required")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Decision(str, Enum):
    ALLOWED = "allowed"
    REQUIRE_APPROVAL = "require_approval"
    DENIED = "denied"
    BLOCKED = "blocked"


class ApprovalState(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"
    BLOCKED = "blocked"


@dataclass
class PolicyDecision:
    decision: Decision
    reason: str
    risk: str = "safe"
    rule_id: Optional[str] = None


@dataclass
class PolicyRule:
    id: str
    tool: str  # glob: * matches any
    action: str  # allow | deny
    pattern: str = "*"  # regex over "tool args..." (empty means any)
    reason: str = ""

    def matches(self, tool: str, args_text: str) -> bool:
        if self.tool != "*" and not re.fullmatch(self.tool.replace("*", ".*"), tool):
            return False
        if self.pattern == "*" or not self.pattern:
            return True
        try:
            return re.search(self.pattern, args_text) is not None
        except re.error:
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tool": self.tool,
            "action": self.action,
            "pattern": self.pattern,
            "reason": self.reason,
        }


DEFAULT_POLICY_RULES: List[PolicyRule] = [
    PolicyRule("deny-rm-rf", "remove", "deny", r"(^|\s)-r[fi]*\s", "recursive force remove"),
    PolicyRule("deny-shell-rm-rf", "shell", "deny", r"rm\s+-[a-z]*r[a-z]*", "rm -r via shell"),
    PolicyRule("deny-shell-sudo", "shell", "deny", r"(^|\s)sudo\b", "sudo via shell"),
    PolicyRule("deny-shell-env-write", "shell", "deny", r"(^|\s)(export|unset|alias)\s", "env mutation"),
    PolicyRule("deny-remove-root", "remove", "deny", r"(^|/)(\.|\.\.)?$", "removing base dir"),
]


class PolicyEngine:
    """Deterministic tool policy: deny rules, then risk vs threshold.

    threshold is a RiskClass; steps at or above it require approval unless
    an allow rule matches. Denied steps never execute.
    """

    def __init__(
        self,
        threshold: str = "review_required",
        rules: Optional[List[PolicyRule]] = None,
    ):
        self.threshold = threshold
        self.rules = list(rules) if rules is not None else list(DEFAULT_POLICY_RULES)

    def decide(self, tool: str, args: Any, risk: str) -> PolicyDecision:
        args_text = " ".join(self._flatten(args))
        for rule in self.rules:
            if rule.action == "deny" and rule.matches(tool, args_text):
                return PolicyDecision(
                    decision=Decision.DENIED,
                    reason=f"denied by policy rule '{rule.id}': {rule.reason}",
                    risk=risk,
                    rule_id=rule.id,
                )
        if risk_index(risk) >= risk_index(self.threshold):
            for rule in self.rules:
                if rule.action == "allow" and rule.matches(tool, args_text):
                    return PolicyDecision(
                        decision=Decision.ALLOWED,
                        reason=f"allowed by policy rule '{rule.id}': {rule.reason}",
                        risk=risk,
                        rule_id=rule.id,
                    )
            return PolicyDecision(
                decision=Decision.REQUIRE_APPROVAL,
                reason=f"risk '{risk}' at or above threshold '{self.threshold}'",
                risk=risk,
            )
        return PolicyDecision(decision=Decision.ALLOWED, reason=f"risk '{risk}' below threshold", risk=risk)

    @staticmethod
    def _flatten(args: Any) -> List[str]:
        """Flatten nested args (lists, dicts) into a deterministic token list."""
        if args is None:
            return []
        if isinstance(args, dict):
            out: List[str] = []
            for key in sorted(args):
                out.extend(PolicyEngine._flatten(args[key]))
            return out
        if isinstance(args, (list, tuple)):
            out = []
            for item in args:
                out.extend(PolicyEngine._flatten(item))
            return out
        return [str(args)]


@dataclass
class ApprovalRecord:
    execution_id: str
    step_index: int
    tool: str
    args: Any = field(default_factory=list)
    risk: str = "safe"
    state: ApprovalState = ApprovalState.PENDING_APPROVAL
    note: str = ""
    decided_by: str = ""
    requested_at: str = ""
    decided_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "step_index": self.step_index,
            "tool": self.tool,
            "args": self.args,
            "risk": self.risk,
            "state": self.state.value,
            "note": self.note,
            "decided_by": self.decided_by,
            "requested_at": self.requested_at,
            "decided_at": self.decided_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApprovalRecord":
        try:
            state = ApprovalState(str(data.get("state", ApprovalState.PENDING_APPROVAL.value)))
        except ValueError:
            state = ApprovalState.PENDING_APPROVAL
        return cls(
            execution_id=str(data.get("execution_id", "")),
            step_index=int(data.get("step_index", 0)),
            tool=str(data.get("tool", "")),
            args=list(data.get("args", []) or []),
            risk=str(data.get("risk", "safe")),
            state=state,
            note=str(data.get("note", "")),
            decided_by=str(data.get("decided_by", "")),
            requested_at=str(data.get("requested_at", "")),
            decided_at=str(data.get("decided_at", "")),
        )


class ApprovalStore:
    """JSONL persistence for approval records under <root>/.kdesk/runtime/."""

    def __init__(self, runtime_dir: Path):
        self.runtime_dir = Path(runtime_dir)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self.runtime_dir / "approvals.jsonl"

    def _load(self) -> List[ApprovalRecord]:
        if not self.path.exists():
            return []
        records = []
        with open(self.path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(ApprovalRecord.from_dict(json.loads(line)))
                except (ValueError, TypeError):
                    continue
        return records

    def _append(self, record: ApprovalRecord) -> None:
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record.to_dict()) + "\n")

    def request(self, execution_id: str, step_index: int, tool: str,
                args: Any, risk: str) -> ApprovalRecord:
        record = ApprovalRecord(
            execution_id=execution_id,
            step_index=step_index,
            tool=tool,
            args=args,
            risk=risk,
            requested_at=now_iso(),
        )
        self._append(record)
        return record

    def get(self, execution_id: str, step_index: int) -> Optional[ApprovalRecord]:
        for record in reversed(self._load()):
            if record.execution_id == execution_id and record.step_index == step_index:
                return record
        return None

    def set_state(self, execution_id: str, step_index: int, state: ApprovalState,
                  note: str = "", decided_by: str = "") -> Optional[ApprovalRecord]:
        record = self.get(execution_id, step_index)
        if record is None:
            return None
        record.state = state
        record.note = note
        record.decided_by = decided_by
        record.decided_at = now_iso()
        self._rewrite_all()
        return record

    def _rewrite_all(self) -> None:
        records = self._load()
        with open(self.path, "w", encoding="utf-8") as fh:
            for record in records:
                fh.write(json.dumps(record.to_dict()) + "\n")

    def list_for(self, execution_id: str) -> List[ApprovalRecord]:
        return [r for r in self._load() if r.execution_id == execution_id]

    def list_pending(self, limit: int = 20) -> List[ApprovalRecord]:
        pending = [r for r in self._load() if r.state == ApprovalState.PENDING_APPROVAL]
        return pending[:limit]

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()