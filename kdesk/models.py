"""Domain models for the Kdesk catalog (definition-v1 / workflow-v1) and the
KDESK Phase 2 runtime (tools, permissions, sessions, tasks, plans, results,
events, provenance, manifests)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Capability:
    name: str
    description: str = ""
    commands: List[str] = field(default_factory=list)
    examples: List[Any] = field(default_factory=list)
    parameters: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Capability":
        return cls(
            name=str(data.get("name", "")),
            description=str(data.get("description", "")),
            commands=list(data.get("commands", []) or []),
            examples=list(data.get("examples", []) or []),
            parameters=list(data.get("parameters", []) or []),
        )

    def tool_binaries(self) -> List[str]:
        """First word of each real command = the tool binary (wiring evidence)."""
        bins = []
        for cmd in self.commands:
            if not isinstance(cmd, str):
                continue
            parts = cmd.strip().split()
            if not parts:
                continue
            first = parts[0].rstrip(":")
            if first and not first.endswith(":"):
                bins.append(first)
        return bins


@dataclass
class BaseDefinition:
    name: str
    display_name: str = ""
    category: str = ""
    subcategory: Optional[str] = None
    description: str = ""
    version: str = ""
    type: str = "agent"
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    author: Optional[str] = None
    license: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    capabilities: List[Capability] = field(default_factory=list)
    knowledge: List[Dict[str, Any]] = field(default_factory=list)
    instructions: Any = None
    examples: List[Any] = field(default_factory=list)
    platforms: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    source_path: Optional[Path] = None
    checksum: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def tool_binaries(self) -> List[str]:
        bins: List[str] = []
        for cap in self.capabilities:
            bins.extend(cap.tool_binaries())
        return bins

    def all_commands(self) -> List[str]:
        cmds: List[str] = []
        for cap in self.capabilities:
            cmds.extend(cap.commands)
        return cmds


@dataclass
class Agent(BaseDefinition):
    type: str = "agent"
    skills: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class Skill(BaseDefinition):
    type: str = "skill"
    tools: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class WorkflowStep:
    id: str
    step_type: str  # skill | agent | capability
    skill: Optional[str] = None
    agent: Optional[str] = None
    capability: Optional[str] = None
    tool: Optional[str] = None
    requires: Optional[str] = None
    input: Any = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Workflow:
    id: str
    name: str = ""
    version: str = ""
    agent: str = ""
    description: str = ""
    input: Dict[str, Any] = field(default_factory=dict)
    output: Dict[str, Any] = field(default_factory=dict)
    steps: List[WorkflowStep] = field(default_factory=list)
    source_path: Optional[Path] = None

    @classmethod
    def from_file(cls, path: Path) -> "Workflow":
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        steps = []
        for s in data.get("steps", []):
            steps.append(
                WorkflowStep(
                    id=str(s.get("id", "")),
                    step_type=str(s.get("type", "")),
                    skill=s.get("skill"),
                    agent=s.get("agent"),
                    capability=s.get("capability"),
                    tool=s.get("tool"),
                    requires=s.get("requires"),
                    input=s.get("input"),
                    raw=s,
                )
            )
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            version=str(data.get("version", "")),
            agent=str(data.get("agent", "")),
            description=str(data.get("description", "")),
            input=data.get("input", {}),
            output=data.get("output", {}),
            steps=steps,
            source_path=path,
        )

    def step_ids(self) -> List[str]:
        return [s.id for s in self.steps]

    def referenced_entities(self) -> Dict[str, List[str]]:
        skills, agents = [], []
        for s in self.steps:
            if s.skill:
                skills.append(s.skill)
            if s.agent:
                agents.append(s.agent)
        return {"skills": skills, "agents": agents}


# =====================================================================
# Phase 2 runtime domain models
# =====================================================================


class PermissionClass(str, Enum):
    """Risk classification of a tool operation (permission engine)."""

    READ_ONLY = "read_only"
    SAFE_WRITE = "safe_write"
    MODERATE = "moderate"
    DESTRUCTIVE = "destructive"
    PRIVILEGED = "privileged"


class PlatformStatus(str, Enum):
    """Lifecycle status of a platform (distinct from support level)."""

    DEFINITION_GENERATED = "definition_generated"
    CONFIG_INSTALLED = "config_installed"
    PLATFORM_VALIDATED = "platform_validated"
    RUNTIME_EXECUTED = "runtime_executed"


@dataclass
class Tool:
    """A runtime tool a platform can invoke (filesystem, shell, git, http...)."""

    id: str
    name: str
    description: str = ""
    category: str = "general"
    risk: PermissionClass = PermissionClass.READ_ONLY
    permission_required: bool = False
    platform_support: Dict[str, bool] = field(default_factory=dict)
    handler: Optional[str] = None


@dataclass
class Platform:
    """Runtime platform target (Claude Code, Cursor, Codex CLI, ...)."""

    name: str
    family: str = ""
    format: str = ""
    support_level: str = "UNKNOWN"
    status: PlatformStatus = PlatformStatus.DEFINITION_GENERATED
    version: Optional[str] = None
    capabilities: List[str] = field(default_factory=list)


@dataclass
class PlatformCapability:
    platform: str
    capability: str
    supported: bool = False
    notes: str = ""


@dataclass
class Bundle:
    """Named grouping of agents/skills (backend, fullstack, security, ...)."""

    id: str
    name: str = ""
    description: str = ""
    agents: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)


@dataclass
class PermissionPolicy:
    """Rule granting or denying access to a tool/resource pattern."""

    id: str
    tool: str
    pattern: str = "*"
    action: str = "allow"  # allow | deny
    reason: str = ""
    source: str = "kdesk"


@dataclass
class Installation:
    """A definition installed onto a platform (record of an install op)."""

    platform: str
    definition_id: str
    target_path: str
    status: str = "installed"  # installed | failed | rolled_back | drifted
    installed_at: Optional[str] = None
    manifest_id: Optional[str] = None
    checksum: Optional[str] = None


@dataclass
class InstallationManifest:
    """Immutable record of what was installed, where, and how."""

    manifest_id: str
    source_definition_id: str
    source_version: str
    platform: str
    platform_version: Optional[str]
    adapter_version: str
    installed_path: str
    checksum: str
    generated_at: str
    transformations: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "source_definition_id": self.source_definition_id,
            "source_version": self.source_version,
            "platform": self.platform,
            "platform_version": self.platform_version,
            "adapter_version": self.adapter_version,
            "installed_path": self.installed_path,
            "checksum": self.checksum,
            "generated_at": self.generated_at,
            "transformations": self.transformations,
            "capabilities": self.capabilities,
            "warnings": self.warnings,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstallationManifest":
        return cls(
            manifest_id=str(data.get("manifest_id", "")),
            source_definition_id=str(data.get("source_definition_id", "")),
            source_version=str(data.get("source_version", "")),
            platform=str(data.get("platform", "")),
            platform_version=data.get("platform_version"),
            adapter_version=str(data.get("adapter_version", "")),
            installed_path=str(data.get("installed_path", "")),
            checksum=str(data.get("checksum", "")),
            generated_at=str(data.get("generated_at", "")),
            transformations=list(data.get("transformations", []) or []),
            capabilities=list(data.get("capabilities", []) or []),
            warnings=list(data.get("warnings", []) or []),
        )


@dataclass
class AgentSession:
    """Isolated session bound to one agent execution."""

    session_id: str
    agent_name: str
    platform: str = ""
    created_at: str = ""
    state: str = "created"  # created | running | completed | failed | cancelled
    context: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)

    def record_event(self, event_type: str, data: Optional[Dict[str, Any]] = None) -> None:
        self.events.append({"type": event_type, "data": data or {}, "session_id": self.session_id})


@dataclass
class TaskRequest:
    """User-level task submitted to the planner."""

    id: str
    goal: str
    context: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    desired_agents: List[str] = field(default_factory=list)
    desired_skills: List[str] = field(default_factory=list)
    mode: str = "auto"  # auto | plan | execute | review


@dataclass
class TaskPlanStep:
    action: str
    target: Optional[str] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    depends_on: List[str] = field(default_factory=list)


@dataclass
class TaskPlan:
    """Plan produced by the planner from a TaskRequest."""

    id: str
    task_id: str
    steps: List[TaskPlanStep] = field(default_factory=list)
    rationale: str = ""
    estimated_effort: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "rationale": self.rationale,
            "estimated_effort": self.estimated_effort,
            "steps": [
                {
                    "action": s.action,
                    "target": s.target,
                    "inputs": s.inputs,
                    "reason": s.reason,
                    "depends_on": s.depends_on,
                }
                for s in self.steps
            ],
        }


@dataclass
class ToolRequest:
    """A single tool invocation request."""

    id: str
    tool: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    permission_class: PermissionClass = PermissionClass.READ_ONLY
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    """Outcome of a tool invocation."""

    id: str
    request_id: str
    success: bool
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    output: Any = None
    error: str = ""


@dataclass
class ValidationResult:
    """Evidence-based validation outcome for a step/definition."""

    id: str
    validator: str
    passed: bool
    evidence: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class WorkflowResult:
    """Result of a workflow run (persisted with run_id)."""

    run_id: str
    workflow_id: str
    status: str = "created"  # created | running | completed | failed | cancelled
    outputs: Dict[str, Any] = field(default_factory=dict)
    node_results: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    error: str = ""


@dataclass
class RuntimeEvent:
    """Event emitted on the runtime event bus."""

    type: str
    run_id: str = ""
    node_id: str = ""
    timestamp: str = ""
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProvenanceRecord:
    """Traceability record linking generated output to its source."""

    definition_id: str
    source_path: str
    converter: str = ""
    tool: str = ""
    schema: str = ""
    created_at: str = ""
    checksum: Optional[str] = None