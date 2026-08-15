"""Phase C: deterministic resolvers and planner.

AgentResolver     ranked agent candidates with per-signal explanations
SkillResolver     required/optional/rejected skills with confidence + evidence
SkillLoader       ordered, context-limited skill loading (transitive)
TaskPlanner       TaskRequest -> TaskPlan

All resolution is deterministic and evidence-backed: signals come from
catalog fields (name, display_name, category, subcategory, tags, keywords,
tools, description) and the capability graph. No LLM is used.

Scoring: per-query-token maximum contribution across fields, normalized by
token count -- one token can only contribute once, from its strongest field.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from kdesk.graph import CatalogGraph
from kdesk.models import TaskPlan, TaskPlanStep, TaskRequest
from kdesk.registry import Catalog

# per-field contribution of a single matched query token
FIELD_WEIGHTS = {
    "name": 1.0,
    "display": 0.8,
    "category": 0.6,
    "tag": 0.5,
    "tool": 0.4,
    "description": 0.25,
}
EXACT_NAME_BONUS = 0.3


def _tokens(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9]+", (text or "").lower()) if len(t) > 1]


def _token_set(text: str) -> set:
    return set(_tokens(text))


def _fields(name: str, agent, with_description: bool = True) -> Dict[str, set]:
    fields = {
        "name": _token_set(name),
        "display": _token_set(agent.display_name),
        "category": _token_set(agent.category),
        "tag": _token_set(" ".join(agent.tags + agent.keywords)),
        "tool": _token_set(" ".join(agent.tool_binaries())),
    }
    if with_description:
        fields["description"] = _token_set(agent.description)
    return fields


def _score(fields: Dict[str, set], qset: set) -> Tuple[float, List[str]]:
    """Per-token maximum contribution, normalized by query size."""
    if not qset:
        return 0.0, []
    total = 0.0
    signals: List[str] = []
    for token in sorted(qset):
        best_field, best = None, 0.0
        for fname, tokens in fields.items():
            if token in tokens and FIELD_WEIGHTS[fname] > best:
                best, best_field = FIELD_WEIGHTS[fname], fname
        if best > 0.0:
            total += best
            signals.append(f"{token} -> {best_field}")
    return total / len(qset), signals


# ------------------------------------------------------------ AgentResolver
@dataclass
class AgentCandidate:
    agent: str
    score: float
    signals: List[str] = field(default_factory=list)

    def explain(self) -> List[str]:
        return [f"  - {self.agent} ({self.score:.2f}): {s}" for s in self.signals]


class AgentResolver:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self._index: List[Tuple[str, Any, Dict[str, set]]] = []
        for name, agent in catalog.agents.items():
            self._index.append((name, agent, _fields(name, agent)))

    def resolve(self, query: str, top_k: int = 5, min_score: float = 0.0) -> List[AgentCandidate]:
        q = query.strip().lower()
        qset = _token_set(q)
        results: List[AgentCandidate] = []
        for name, agent, fields in self._index:
            score, signals = _score(fields, qset)
            if name == q:
                score = min(1.0, score + EXACT_NAME_BONUS)
                signals.insert(0, f"exact name match: {name}")
            elif q and name.startswith(q):
                score = min(1.0, score + EXACT_NAME_BONUS)
                signals.insert(0, f"name prefix match: {name}")
            if score > 0.0:
                results.append(AgentCandidate(agent=name, score=score, signals=signals))
        results.sort(key=lambda c: (-c.score, c.agent))
        return [c for c in results if c.score >= min_score][:top_k]


# ------------------------------------------------------------ SkillResolver
@dataclass
class SkillMatch:
    skill: str
    status: str  # required | optional | rejected
    confidence: float
    evidence: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


class SkillResolver:
    def __init__(self, catalog: Catalog, graph: Optional[CatalogGraph] = None):
        self.catalog = catalog
        self.graph = graph or CatalogGraph(catalog)

    def resolve(self, goal: str, required_topics: Optional[List[str]] = None,
                excluded: Optional[List[str]] = None) -> List[SkillMatch]:
        qset = _token_set(goal)
        excluded = excluded or []
        matches: List[SkillMatch] = []
        for name, skill in self.catalog.skills.items():
            if name in excluded:
                matches.append(SkillMatch(skill=name, status="rejected", confidence=0.0,
                                          evidence=["explicitly excluded"]))
                continue
            fields = _fields(name, skill)
            score, signals = _score(fields, qset)
            if score <= 0.0:
                continue
            conf = min(1.0, 0.25 + 0.75 * score)
            status = "required" if score >= 0.5 else "optional"
            deps = [e["target"] for e in self.graph.out_edges(name, "skill_requires_skill")]
            matches.append(SkillMatch(
                skill=name, status=status, confidence=conf,
                evidence=signals, dependencies=sorted(deps),
            ))
        # hard-require skills that match a required topic by name/display
        for topic in (required_topics or []):
            topic_tokens = _token_set(topic)
            for name, skill in self.catalog.skills.items():
                if not (topic_tokens <= _token_set(name) or topic_tokens <= _token_set(skill.display_name)):
                    continue
                existing = next((m for m in matches if m.skill == name), None)
                if existing is None:
                    matches.append(SkillMatch(
                        skill=name, status="required", confidence=1.0,
                        evidence=[f"required topic: {topic}"],
                        dependencies=sorted(e["target"] for e in self.graph.out_edges(name, "skill_requires_skill")),
                    ))
                elif existing.status == "optional":
                    existing.status = "required"
                    existing.confidence = 1.0
                    existing.evidence.append(f"required topic: {topic}")
        matches.sort(key=lambda m: (0 if m.status == "required" else 1 if m.status == "optional" else 2,
                                    -m.confidence, m.skill))
        return matches


# ------------------------------------------------------------- SkillLoader
class SkillLoader:
    """Loads skills in dependency order within a context budget.

    budget is an approximate token budget: description + first 2 knowledge
    entries + instructions text length.
    """

    def __init__(self, catalog: Catalog, graph: Optional[CatalogGraph] = None):
        self.catalog = catalog
        self.graph = graph or CatalogGraph(catalog)

    @staticmethod
    def _size(skill) -> int:
        raw = skill.raw or {}
        text = str(raw.get("description", "")) + " " + str(raw.get("instructions", ""))
        for k in (raw.get("knowledge") or [])[:2]:
            text += " " + str(k.get("content", "") if isinstance(k, dict) else k)
        return max(1, len(text) // 4)

    def load_order(self, skills: List[str], budget: int = 6000, max_skills: int = 12) -> List[str]:
        chosen: List[str] = []
        seen: set = set()
        for sid in skills:
            if sid in seen or sid not in self.catalog.skills:
                continue
            seen.add(sid)
            chosen.append(sid)
        # prerequisites first (transitive closure, post-order, stable)
        ordered: List[str] = []
        visited: set = set()
        for sid in chosen:
            stack: List[Tuple[str, bool]] = [(sid, False)]
            while stack:
                cur, expanded = stack.pop()
                if expanded:
                    ordered.append(cur)
                    continue
                if cur in visited or cur not in self.catalog.skills:
                    continue
                visited.add(cur)
                stack.append((cur, True))
                deps = [e["target"] for e in self.graph.out_edges(cur, "skill_requires_skill")]
                for d in reversed(deps):
                    stack.append((d, False))
        result: List[str] = []
        used = 0
        for sid in ordered:
            if len(result) >= max_skills:
                break
            size = self._size(self.catalog.skills[sid])
            if used + size > budget and result:
                break
            used += size
            result.append(sid)
        return result

    def load(self, skills: List[str], budget: int = 6000, max_skills: int = 12) -> Dict[str, Dict[str, Any]]:
        order = self.load_order(skills, budget=budget, max_skills=max_skills)
        return {sid: {"skill": self.catalog.skills[sid].raw, "order": i} for i, sid in enumerate(order)}


# ------------------------------------------------------------- TaskPlanner
class TaskPlanner:
    def __init__(self, catalog: Catalog, graph: Optional[CatalogGraph] = None):
        self.catalog = catalog
        self.graph = graph or CatalogGraph(catalog)
        self.agent_resolver = AgentResolver(catalog)
        self.skill_resolver = SkillResolver(catalog, self.graph)
        self.skill_loader = SkillLoader(catalog, self.graph)

    def plan(self, request: TaskRequest) -> TaskPlan:
        agents = self.agent_resolver.resolve(request.goal, top_k=3, min_score=0.15)
        matches = self.skill_resolver.resolve(
            request.goal,
            required_topics=request.desired_skills or None,
        )
        required = [m.skill for m in matches if m.status == "required"]
        optional = [m.skill for m in matches if m.status == "optional"][:8]
        load = self.skill_loader.load_order(required + optional, max_skills=12)
        steps: List[TaskPlanStep] = []
        if agents:
            primary = agents[0].agent
            steps.append(TaskPlanStep(action="run_agent", target=primary,
                                      inputs={"goal": request.goal}, reason="primary agent"))
        for i, sid in enumerate(load):
            steps.append(TaskPlanStep(action="load_skill", target=sid,
                                      inputs={"order": i}, reason="capability dependency",
                                      depends_on=steps[-1:]))
        rationale_parts = []
        if agents:
            rationale_parts.append(f"agents: {', '.join(a.agent for a in agents)}")
        if load:
            rationale_parts.append(f"skills ({len(load)}): {', '.join(load[:6])}")
        effort = "low" if len(steps) <= 2 else "medium" if len(steps) <= 6 else "high"
        return TaskPlan(
            id=f"plan-{request.id}",
            task_id=request.id,
            steps=steps,
            rationale="; ".join(rationale_parts) or "no resolution signals",
            estimated_effort=effort,
        )