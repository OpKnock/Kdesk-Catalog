"""Runtime contracts: capability/IO contract model for agents and skills.

A contract describes what a definition can do (capabilities), what it
consumes (inputs), what it produces (outputs), what runtime it needs
(requirements), how risky it is (risk) and how it executes
(execution_mode). Contracts drive deterministic composition: step A can
feed step B when A's outputs satisfy B's required inputs.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from kdesk.models import BaseDefinition

_SLUG_RE = re.compile(r"[^a-z0-9_]+")
_WRITE_TOOLS = {"write_file", "edit_file", "remove", "package_install", "shell", "git"}
_SAFE_TOOLS = {"read_file", "glob", "grep", "http_get", "python", "analyze_project"}


def slugify(text: str) -> str:
    return _SLUG_RE.sub("_", text.strip().lower()).strip("_")


@dataclass
class ContractField:
    """One input or output of a contract."""

    name: str
    kind: str = "any"  # string | integer | path | file | list | any
    description: str = ""
    required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "description": self.description,
            "required": self.required,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContractField":
        return cls(
            name=str(data.get("name", "")),
            kind=str(data.get("kind", "any")),
            description=str(data.get("description", "")),
            required=bool(data.get("required", True)),
        )


@dataclass
class Contract:
    """Execution contract of one agent or skill definition."""

    definition: str
    definition_type: str  # agent | skill
    capabilities: List[str] = field(default_factory=list)
    inputs: List[ContractField] = field(default_factory=list)
    outputs: List[ContractField] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    risk: str = "safe"  # safe | review_required | dangerous | blocked
    execution_mode: str = "orchestrated"  # orchestrated | native | local
    platforms: List[str] = field(default_factory=list)

    def input_names(self) -> List[str]:
        return [f.name for f in self.inputs]

    def output_names(self) -> List[str]:
        return [f.name for f in self.outputs]

    def required_input_names(self) -> List[str]:
        return [f.name for f in self.inputs if f.required]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "definition": self.definition,
            "definition_type": self.definition_type,
            "capabilities": self.capabilities,
            "inputs": [f.to_dict() for f in self.inputs],
            "outputs": [f.to_dict() for f in self.outputs],
            "requirements": self.requirements,
            "risk": self.risk,
            "execution_mode": self.execution_mode,
            "platforms": self.platforms,
        }


def derive_contract(defn: BaseDefinition) -> Contract:
    """Derive a contract from a definition's existing fields.

    Explicit `inputs` / `outputs` / `requirements` keys in the source YAML
    win; otherwise contracts are inferred from capability parameters
    (inputs), capability names and examples (outputs), and prerequisites
    plus tool binaries (requirements).
    """
    capabilities = [c.name for c in defn.capabilities if c.name]
    raw = defn.raw or {}
    inputs: List[ContractField] = []
    for item in raw.get("inputs", []) or []:
        if isinstance(item, str):
            inputs.append(ContractField(name=slugify(item)))
        elif isinstance(item, dict):
            inputs.append(ContractField.from_dict(item))
    if not inputs:
        seen = set()
        for cap in defn.capabilities:
            for param in cap.parameters or []:
                if not isinstance(param, dict):
                    continue
                name = slugify(str(param.get("name", "")))
                if not name or name in seen:
                    continue
                seen.add(name)
                inputs.append(
                    ContractField(
                        name=name,
                        kind=str(param.get("type", "any")),
                        description=str(param.get("description", "")),
                        required=bool(param.get("required", False)),
                    )
                )
    outputs: List[ContractField] = []
    for item in raw.get("outputs", []) or []:
        if isinstance(item, str):
            outputs.append(ContractField(name=slugify(item)))
        elif isinstance(item, dict):
            outputs.append(ContractField.from_dict(item))
    if not outputs:
        seen = set()
        for cap in defn.capabilities:
            name = slugify(cap.name)
            if name and name not in seen:
                seen.add(name)
                outputs.append(ContractField(name=name, description=cap.description))
        if "report" in (defn.description or "").lower() and "report" not in seen:
            outputs.append(ContractField(name="report", description="generated report"))
    requirements = [str(r) for r in (raw.get("requirements", []) or [])]
    if not requirements:
        requirements = [str(p) for p in (defn.prerequisites or [])]
        requirements.extend(sorted(set(t for t in defn.tool_binaries() if not t.startswith("$"))))
    risk = _derive_risk(defn, raw)
    platforms = sorted(k for k in (defn.platforms or {}).keys() if k)
    mode = str(raw.get("execution_mode", "orchestrated"))
    if mode not in ("orchestrated", "native", "local"):
        mode = "orchestrated"
    return Contract(
        definition=defn.name,
        definition_type=defn.type,
        capabilities=capabilities,
        inputs=inputs,
        outputs=outputs,
        requirements=requirements,
        risk=risk,
        execution_mode=mode,
        platforms=platforms,
    )


def _derive_risk(defn: BaseDefinition, raw: Dict[str, Any]) -> str:
    explicit = str(raw.get("risk", "")).lower()
    if explicit in ("safe", "review_required", "dangerous", "blocked"):
        return explicit
    tools = set(defn.tool_binaries())
    if any(t in {"rm", "sudo", "docker"} for t in tools):
        return "dangerous"
    if any(t in {"write_file", "edit_file", "remove"} or t in _WRITE_TOOLS for t in tools):
        return "review_required"
    if any(t in _SAFE_TOOLS for t in tools) or not tools:
        return "safe"
    return "review_required"


def compatibility(source: Contract, target: Contract) -> Dict[str, Any]:
    """How well source outputs satisfy target required inputs.

    Returns a dict with `score` (0.0-1.0), `matched` and `missing` input
    names. Deterministic name matching on slugified names.
    """
    available = {slugify(o.name): o for o in source.outputs}
    matched, missing = [], []
    for req in target.required_input_names():
        key = slugify(req)
        if key in available:
            matched.append(req)
        else:
            missing.append(req)
    total = len(target.required_input_names())
    score = (len(matched) / total) if total else 1.0
    return {"score": score, "matched": matched, "missing": missing}


def can_compose(source: Contract, target: Contract, min_score: float = 0.5) -> bool:
    """True when source can feed target (no unmatched required inputs)."""
    result = compatibility(source, target)
    if result["missing"]:
        return False
    return result["score"] >= min_score