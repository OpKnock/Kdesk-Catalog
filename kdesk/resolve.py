"""Phase K resolution: intent classification, ranked candidates, and the
environment probe. Deterministic and evidence-backed like Phase C.

Resolution chain: request -> intent -> candidate ranking (agents first,
then skills) -> per-candidate contract, tools, requirements -> environment
probe for required runtimes -> explanation strings for `kdesk why`.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from kdesk.contracts import Contract
from kdesk.indexes import IntentClassifier, RuntimeIndexes
from kdesk.registry import Catalog
from kdesk.resolvers import AgentResolver, AgentCandidate, SkillResolver, SkillMatch, _tokens

VERSION_PROBES = ["python", "python3", "node", "npm", "git", "docker", "uv",
                  "cargo", "go", "java", "ruby", "bun", "deno", "pytest",
                  "ruff", "eslint", "kubectl", "terraform"]
VERSION_ARGS = {"python": ["--version"], "python3": ["--version"], "node": ["--version"],
                "git": ["--version"], "docker": ["--version"], "npm": ["--version"],
                "uv": ["--version"], "pytest": ["--version"], "go": ["version"],
                "cargo": ["--version"], "java": ["-version"], "ruby": ["--version"],
                "bun": ["--version"], "deno": ["--version"], "ruff": ["--version"],
                "eslint": ["--version"], "kubectl": ["version", "--client=true"],
                "terraform": ["version"]}


class EnvironmentProbe:
    """Probe which runtimes are present on the host (shutil.which + version)."""

    def __init__(self, timeout_s: float = 10.0):
        self.timeout_s = timeout_s
        self._cache: Dict[str, Dict[str, Any]] = {}

    def check(self, executable: str) -> Dict[str, Any]:
        if executable in self._cache:
            return self._cache[executable]
        result = {"present": False, "version": None, "path": None}
        path = shutil.which(executable)
        if path:
            result["present"] = True
            result["path"] = path
            result["version"] = self._version(executable)
        self._cache[executable] = result
        return result

    def _version(self, executable: str) -> Optional[str]:
        args = VERSION_ARGS.get(executable, ["--version"])
        try:
            proc = subprocess.run(
                [executable] + args,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
            )
            text = (proc.stdout or proc.stderr or "").strip().splitlines()
            return text[0][:120] if text else None
        except (OSError, subprocess.TimeoutExpired, ValueError):
            return None

    def probe(self, requirements: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        targets = requirements or VERSION_PROBES
        return {name: self.check(name) for name in targets}

    def unmet(self, requirements: List[str]) -> Dict[str, Dict[str, Any]]:
        """Requirements that no probed executable satisfies."""
        missing = {}
        for req in requirements:
            name = str(req).split()[0] if str(req).split() else req
            info = self.check(name)
            if not info["present"]:
                missing[req] = info
        return missing


@dataclass
class ResolvedCandidate:
    name: str
    definition_type: str
    score: float
    signals: List[str] = field(default_factory=list)
    contract: Optional[Contract] = None
    tools: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "definition_type": self.definition_type,
            "score": round(self.score, 3),
            "signals": self.signals,
            "tools": self.tools,
            "requirements": self.requirements,
            "risk": self.contract.risk if self.contract else "safe",
            "execution_mode": self.contract.execution_mode if self.contract else "orchestrated",
        }


@dataclass
class ResolveResult:
    request: str
    intent: Dict[str, Any]
    candidates: List[ResolvedCandidate] = field(default_factory=list)
    environment: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    missing_requirements: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    reasoning: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request": self.request,
            "intent": self.intent,
            "candidates": [c.to_dict() for c in self.candidates],
            "environment": self.environment,
            "missing_requirements": self.missing_requirements,
            "reasoning": self.reasoning,
        }


class Resolver:
    """Intent classification + deterministic candidate ranking + env probe."""

    def __init__(self, catalog: Catalog, indexes: Optional[RuntimeIndexes] = None):
        self.catalog = catalog
        self.indexes = indexes or RuntimeIndexes.from_catalog(catalog)
        self.intent_classifier = IntentClassifier()
        self.agent_resolver = AgentResolver(catalog)
        self.skill_resolver = SkillResolver(catalog)
        self.probe = EnvironmentProbe()

    def resolve(self, request: str, top: int = 8,
                probe_environment: bool = True) -> ResolveResult:
        intent = self.intent_classifier.classify(request)
        agents = self.agent_resolver.resolve(request, top_k=top, min_score=0.15)
        skills = self.skill_resolver.resolve(request)[:top]
        candidates: List[ResolvedCandidate] = []
        for cand in agents:
            candidates.append(self._agent_candidate(cand))
        for match in skills:
            if match.status == "rejected":
                continue
            candidates.append(self._skill_candidate(match))
        candidates.sort(key=lambda c: (-c.score, c.name))
        environment: Dict[str, Dict[str, Any]] = {}
        missing: Dict[str, Dict[str, Any]] = {}
        if probe_environment:
            requirements = sorted({
                r for c in candidates for r in c.requirements if not r.startswith("$")
            })[:24]
            environment = self.probe.probe(requirements) if requirements else {}
            missing = {k: v for k, v in environment.items() if not v["present"]}
        reasoning = [
            f"intent classified as '{intent['intent']}' (confidence {intent['confidence']})",
        ]
        if candidates:
            reasoning.append(
                f"top candidate: {candidates[0].name} "
                f"({candidates[0].definition_type}, score {candidates[0].score:.3f})"
            )
        else:
            reasoning.append("no candidates scored above the resolution floor")
        return ResolveResult(
            request=request,
            intent=intent,
            candidates=candidates,
            environment=environment,
            missing_requirements=missing,
            reasoning=reasoning,
        )

    def _agent_candidate(self, cand: AgentCandidate) -> ResolvedCandidate:
        agent = self.catalog.agents[cand.agent]
        contract = self.indexes.contracts.get(cand.agent)
        tools = sorted(set(agent.tool_binaries()))
        requirements = sorted(set(str(r) for r in (agent.prerequisites or [])))
        requirements.extend(sorted(t for t in tools if not t.startswith("$")))
        return ResolvedCandidate(
            name=cand.agent,
            definition_type="agent",
            score=cand.score,
            signals=list(cand.signals),
            contract=contract,
            tools=tools,
            requirements=sorted(set(requirements)),
        )

    def _skill_candidate(self, match: SkillMatch) -> ResolvedCandidate:
        skill = self.catalog.skills[match.skill]
        contract = self.indexes.contracts.get(match.skill)
        tools = sorted(set(skill.tool_binaries()))
        requirements = sorted(set(str(r) for r in (skill.prerequisites or [])))
        requirements.extend(sorted(t for t in tools if not t.startswith("$")))
        return ResolvedCandidate(
            name=match.skill,
            definition_type="skill",
            score=match.confidence,
            signals=list(match.evidence),
            contract=contract,
            tools=tools,
            requirements=sorted(set(requirements)),
        )

    def explain(self, request: str, target: str) -> Dict[str, Any]:
        """Why is `target` (not) a candidate for `request`?"""
        result = self.resolve(request, top=100, probe_environment=False)
        defn = self.catalog.agents.get(target) or self.catalog.skills.get(target)
        if defn is None:
            return {"target": target, "found": False, "reason": "unknown definition"}
        candidate = next((c for c in result.candidates if c.name == target), None)
        if candidate is None:
            qset = set(_tokens(request))
            name_tokens = set(_tokens(target))
            overlap = sorted(qset & name_tokens)
            return {
                "target": target,
                "found": True,
                "selected": False,
                "reason": (
                    f"no query tokens matched (token overlap: {overlap or 'none'})"
                ),
                "signals": [],
            }
        return {
            "target": target,
            "found": True,
            "selected": True,
            "score": round(candidate.score, 3),
            "rank": next(i for i, c in enumerate(result.candidates) if c.name == target) + 1,
            "signals": candidate.signals,
            "reason": "matched query tokens with weighted signals",
        }