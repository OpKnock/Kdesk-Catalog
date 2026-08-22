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
    """Stores approval records and persists to JSONL."""
    
    def __init__(self, root: Path):
        # root may be the runtime dir; the records file lives inside it
        self.path = Path(root) / "approvals.jsonl"
        self._records: List[ApprovalRecord] = []
        self._load()
    
    def _load(self) -> None:
        if self.path.is_file():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self._records.append(ApprovalRecord.from_dict(json.loads(line)))
            except (OSError, json.JSONDecodeError):
                pass
    
    def add(self, record: ApprovalRecord) -> None:
        self._records.append(record)
        self._persist()
    
    def get(self, execution_id: str, step_index: int) -> Optional[ApprovalRecord]:
        for r in self._records:
            if r.execution_id == execution_id and r.step_index == step_index:
                return r
        return None
    
    def update(self, record: ApprovalRecord) -> None:
        for i, r in enumerate(self._records):
            if r.execution_id == record.execution_id and r.step_index == record.step_index:
                self._records[i] = record
                self._persist()
                return
        self._records.append(record)
        self._persist()
    
    def list_for_execution(self, execution_id: str) -> List[ApprovalRecord]:
        return [r for r in self._records if r.execution_id == execution_id]
    
    def request(self, execution_id: str, step_index: int, tool: str, args: Any,
                risk: str, description: str = "") -> ApprovalRecord:
        """Create a new approval request for a step."""
        record = ApprovalRecord(
            execution_id=execution_id,
            step_index=step_index,
            tool=tool,
            args=args,
            risk=risk,
            state=ApprovalState.PENDING_APPROVAL,
            requested_at=now_iso()
        )
        self.add(record)
        return record
    
    def set_state(self, execution_id: str, step_index: int, state: ApprovalState,
                  note: str = "", decided_by: str = "") -> Optional[ApprovalRecord]:
        """Update the state of an approval record."""
        record = self.get(execution_id, step_index)
        if record is None:
            return None
        record.state = state
        record.note = note or record.note
        record.decided_by = decided_by or record.decided_by
        record.decided_at = now_iso()
        self.update(record)
        return record
    
    def list_for(self, execution_id: str) -> List[ApprovalRecord]:
        return [r for r in self._records if r.execution_id == execution_id]
    
    def _persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            for r in self._records:
                f.write(json.dumps(r.to_dict(), separators=(",", ":")) + "\n")


# =============================================================================
# Policy-as-Code Engine for Agent Behavior (NEW)
# =============================================================================

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PolicyRuleV2:
    """A single policy rule for agent/skill definitions."""
    id: str
    name: str
    description: str
    severity: Severity = Severity.WARNING
    condition: str = ""
    message: str = ""
    fix_hint: str = ""
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        try:
            return self._eval_condition(self.condition, context)
        except Exception:
            return False
    
    def _eval_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        def replace_var(match):
            var_name = match.group(1)
            value = self._get_nested(context, var_name)
            if value is None:
                return "null"
            if isinstance(value, str):
                return f'"{value}"'
            if isinstance(value, bool):
                return "true" if value else "false"
            if isinstance(value, (list, dict)):
                return json.dumps(value)
            return str(value)
        
        condition = re.sub(r'\$\{(\w+)\}|\{\{(\w+)\}\}', replace_var, condition)
        
        try:
            return eval(condition, {"__builtins__": {}}, {"null": None, "true": True, "false": False})
        except:
            return False
    
    def _get_nested(self, obj: Dict, path: str) -> Any:
        keys = path.split('.')
        current = obj
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and key.isdigit():
                idx = int(key)
                if idx < len(current):
                    current = current[idx]
                else:
                    return None
            else:
                return None
        return current


@dataclass
class PolicyViolation:
    rule_id: str
    rule_name: str
    severity: Severity
    message: str
    target: str
    fix_hint: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyReport:
    violations: List[PolicyViolation] = field(default_factory=list)
    passed_count: int = 0
    total_rules: int = 0
    
    @property
    def error_count(self) -> int:
        return sum(1 for v in self.violations if v.severity in (Severity.ERROR, Severity.CRITICAL))
    
    @property
    def warning_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.WARNING)
    
    @property
    def info_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.INFO)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "severity": v.severity.value,
                    "message": v.message,
                    "target": v.target,
                    "fix_hint": v.fix_hint,
                    "context": v.context
                }
                for v in self.violations
            ],
            "summary": {
                "total_rules": self.total_rules,
                "passed": self.passed_count,
                "violations": len(self.violations),
                "errors": self.error_count,
                "warnings": self.warning_count,
                "info": self.info_count
            }
        }


class PolicyEngineV2:
    """Evaluates policies against agent/skill definitions."""
    
    def __init__(self):
        self.rules: List[PolicyRuleV2] = []
        self._register_builtin_rules()
    
    def _register_builtin_rules(self):
        self.add_rule(PolicyRuleV2(
            id="agent-description-length",
            name="Agent Description Length",
            description="Agents must have a description of at least 200 characters",
            severity=Severity.ERROR,
            condition="len(agent.description) < 200",
            message="Agent description is too short (minimum 200 characters)",
            fix_hint="Add a detailed description explaining the agent's purpose and capabilities"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="agent-has-capabilities",
            name="Agent Has Capabilities",
            description="Agents must define at least one capability",
            severity=Severity.ERROR,
            condition="len(agent.capabilities) == 0",
            message="Agent has no capabilities defined",
            fix_hint="Add at least one capability with name, description, and commands"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="skill-has-tools",
            name="Skill Has Tools",
            description="Skills must declare at least one tool",
            severity=Severity.WARNING,
            condition="len(skill.tools) == 0",
            message="Skill has no tools declared",
            fix_hint="Add tools the skill requires (e.g., python, kubectl, docker)"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="capability-has-commands",
            name="Capability Has Commands",
            description="Each capability must have at least one command",
            severity=Severity.ERROR,
            condition="any(len(c.commands) == 0 for c in agent.capabilities) or any(len(c.commands) == 0 for c in skill.capabilities)",
            message="Capability has no commands",
            fix_hint="Add real working commands to each capability"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="capability-has-examples",
            name="Capability Has Examples",
            description="Each capability should have usage examples",
            severity=Severity.WARNING,
            condition="any(len(c.examples) == 0 for c in agent.capabilities) or any(len(c.examples) == 0 for c in skill.capabilities)",
            message="Capability has no usage examples",
            fix_hint="Add realistic usage examples for each capability"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="capability-has-parameters",
            name="Capability Has Parameters",
            description="Capabilities should define input parameters",
            severity=Severity.WARNING,
            condition="any(len(c.parameters) == 0 for c in agent.capabilities) or any(len(c.parameters) == 0 for c in skill.capabilities)",
            message="Capability has no input parameters defined",
            fix_hint="Define input parameters with name, type, and description"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="agent-has-instructions",
            name="Agent Has Instructions",
            description="Agents should have detailed instructions",
            severity=Severity.WARNING,
            condition="agent.instructions is None or len(str(agent.instructions)) < 50",
            message="Agent has no or very short instructions",
            fix_hint="Add detailed system prompt/instructions for the agent"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="version-format",
            name="Version Format",
            description="Version should follow semantic versioning",
            severity=Severity.WARNING,
            condition="not re.match(r'^\\d+\\.\\d+\\.\\d+', agent.version) and not re.match(r'^\\d+\\.\\d+\\.\\d+', skill.version)",
            message="Version does not follow semantic versioning (MAJOR.MINOR.PATCH)",
            fix_hint="Use semantic versioning format (e.g., 1.2.3)"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="sub-agents-exist",
            name="Sub-Agents Exist",
            description="All declared sub-agents must exist in the catalog",
            severity=Severity.ERROR,
            condition="any(sa not in catalog.agents for sa in agent.sub_agents)",
            message="Agent references non-existent sub-agent",
            fix_hint="Ensure all sub-agents exist in the catalog or remove invalid references"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="delegation-pattern-valid",
            name="Valid Delegation Pattern",
            description="Delegation pattern must be one of: sequential, parallel, conditional",
            severity=Severity.ERROR,
            condition="agent.delegation_pattern not in ['sequential', 'parallel', 'conditional', None]",
            message="Invalid delegation pattern",
            fix_hint="Use one of: sequential, parallel, conditional"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="skills-exist",
            name="Skills Exist",
            description="All skills referenced by agents must exist in the catalog",
            severity=Severity.ERROR,
            condition="any(s not in catalog.skills for s in agent.skills)",
            message="Agent references non-existent skill",
            fix_hint="Ensure all referenced skills exist in the catalog"
        ))
        
        self.add_rule(PolicyRuleV2(
            id="tools-known",
            name="Known Tools",
            description="All tools used by agents/skills should be known",
            severity=Severity.WARNING,
            condition="any(t not in known_tools for t in agent.tools + skill.tools)",
            message="Unknown tool referenced",
            fix_hint="Use known tools or add custom tool to known_tools list"
        ))
    
    def add_rule(self, rule: 'PolicyRuleV2'):
        self.rules.append(rule)
    
    def evaluate(self, catalog) -> Dict[str, Any]:
        violations = []
        passed = 0
        
        # Build context
        known_tools = set()
        for agent in catalog.agents.values():
            known_tools.update(agent.tools)
        for skill in catalog.skills.values():
            known_tools.update(skill.tools)
        for agent in catalog.agents.values():
            for cap in agent.capabilities:
                for cmd in cap.commands:
                    if cmd:
                        first = cmd.strip().split()[0] if cmd.strip() else ""
                        if first:
                            known_tools.add(first)
        for skill in catalog.skills.values():
            for cap in skill.capabilities:
                for cmd in cap.commands:
                    if cmd:
                        first = cmd.strip().split()[0] if cmd.strip() else ""
                        if first:
                            known_tools.add(first)
        
        context = {
            "catalog": catalog,
            "known_tools": list(known_tools)
        }
        
        violations = []
        passed = 0
        
        for rule in self.rules:
            rule_violations = 0
            
            # Check agents
            for name, agent in catalog.agents.items():
                context = {
                    "agent": agent.__dict__,
                    "skill": None,
                    "catalog": catalog,
                    "known_tools": known_tools
                }
                if rule.evaluate(context):
                    violations.append(PolicyViolation(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        severity=rule.severity,
                        message=rule.message,
                        target=f"agent:{name}",
                        fix_hint=rule.fix_hint,
                        context={"agent": name}
                    ))
                    rule_violations += 1
            
            # Check skills
            for name, skill in catalog.skills.items():
                context = {
                    "agent": None,
                    "skill": skill.__dict__,
                    "catalog": catalog,
                    "known_tools": known_tools
                }
                if rule.evaluate(context):
                    violations.append(PolicyViolation(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        severity=rule.severity,
                        message=rule.message,
                        target=f"skill:{name}",
                        fix_hint=rule.fix_hint,
                        context={"skill": name}
                    ))
                    rule_violations += 1
            
            if rule_violations == 0:
                passed += 1
        
        return {
            "violations": [v.__dict__ for v in violations],
            "passed": passed,
            "total_rules": len(self.rules)
        }


class PolicyLoader:
    """Load policies from files."""
    
    @staticmethod
    def from_file(path: Path) -> List[Dict[str, Any]]:
        import yaml
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            return json.load(f)
    
    @staticmethod
    def to_file(rules: List[Dict], path: Path):
        import yaml
        with open(path, 'w') as f:
            if path.suffix in ['.yaml', '.yml']:
                yaml.dump(rules, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(rules, f, indent=2)


# Default policy file path
DEFAULT_POLICY_PATH = Path("policies/agent-policies.json")


def load_default_policies() -> List[Dict]:
    if DEFAULT_POLICY_PATH.exists():
        return PolicyLoader.from_file(DEFAULT_POLICY_PATH)
    return []


if __name__ == "__main__":
    # Demo
    engine = PolicyEngine()
    print(f"Registered {len(engine.rules)} built-in rules")
    for rule in engine.rules:
        print(f"  {rule.id}: {rule.name} ({rule.severity.value})")