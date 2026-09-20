"""Catalog capability graph: typed relationships, transitive traversal,
topological order, cycle and conflict detection.

Relationship taxonomy (14 types):

  1.  agent_has_capability        agent -> capability
  2.  skill_has_capability        skill -> capability
  3.  capability_uses_tool        capability -> tool
  4.  agent_depends_skill         agent -> skill      (wiring / skills:)
  5.  skill_requires_skill        skill -> skill      (prerequisites)
  6.  agent_uses_tool             agent -> tool       (declared tools)
  7.  skill_uses_tool             skill -> tool       (declared tools)
  8.  agent_is_subagent           agent -> agent      (declared subagents)
  9.  platform_emits_definition   platform -> definition
  10. workflow_uses_agent         workflow -> agent
  11. workflow_uses_skill         workflow -> skill
  12. workflow_uses_capability    workflow -> capability
  13. definition_requires_prereq  definition -> prerequisite
  14. definition_has_knowledge    definition -> knowledge topic

Every edge carries a provenance (evidence string or "manual override").
No edge is invented: all edges derive from source YAML, the wiring manifest,
or explicit overrides.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from kdesk.registry import Catalog, default_repo_root


class GraphError(Exception):
    pass


# ---------------------------------------------------------------- taxonomy
RELATIONSHIP_TYPES = [
    "agent_has_capability",
    "skill_has_capability",
    "capability_uses_tool",
    "agent_depends_skill",
    "skill_requires_skill",
    "agent_uses_tool",
    "skill_uses_tool",
    "agent_is_subagent",
    "platform_emits_definition",
    "workflow_uses_agent",
    "workflow_uses_skill",
    "workflow_uses_capability",
    "definition_requires_prereq",
    "definition_has_knowledge",
]

# relationship types that contribute to dependency traversal
DEPENDENCY_TYPES = [
    "agent_depends_skill",
    "skill_requires_skill",
    "agent_is_subagent",
]

# node kinds
AGENT_NODE = "agent"
SKILL_NODE = "skill"
CAPABILITY_NODE = "capability"
TOOL_NODE = "tool"
PLATFORM_NODE = "platform"
WORKFLOW_NODE = "workflow"
PREREQ_NODE = "prerequisite"
KNOWLEDGE_NODE = "knowledge"


def _tool_of(command: str) -> str:
    parts = command.strip().split()
    return parts[0].rstrip(":") if parts else ""


class CatalogGraph:
    def __init__(self, catalog: Catalog, wiring_path: Optional[Path] = None):
        self.catalog = catalog
        self.wiring_path = Path(wiring_path) if wiring_path else default_repo_root() / "skills" / "wiring.json"
        self.edges: Dict[str, List[dict]] = {}  # node -> [{rel, target, evidence, manual}]
        self._conflict_log: List[Dict[str, Any]] = []
        self._load()

    # ---------------------------------------------------------------- load
    def _load(self) -> None:
        # agent -> skill (source yaml skills:)
        for agent in self.catalog.agents.values():
            for sid in agent.skills:
                self._add_edge(agent.name, "agent_depends_skill", sid, evidence="source yaml", manual=False)
        # wiring manifest
        self._load_wiring()
        # declared tools
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            kind = "agent" if defn.type == "agent" else "skill"
            rel = "agent_uses_tool" if kind == "agent" else "skill_uses_tool"
            for tool in defn.tools or []:
                self._add_edge(defn.name, rel, tool, evidence="source yaml tools", manual=False)
        # prerequisites as relationships (definition -> prerequisite)
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            for prereq in defn.prerequisites or []:
                self._add_edge(defn.name, "definition_requires_prereq", str(prereq),
                               evidence="source yaml prerequisites", manual=False)
        # skill -> skill prerequisites (when the prerequisite is a catalog
        # skill and not the skill itself -- a self-reference means the tool
        # binary the definition is named after, not a graph dependency)
        for skill in self.catalog.skills.values():
            for prereq in skill.prerequisites or []:
                if str(prereq) in self.catalog.skills and str(prereq) != skill.name:
                    self._add_edge(skill.name, "skill_requires_skill", str(prereq),
                                   evidence="source yaml prerequisites", manual=False)
        # capabilities
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            kind = "agent" if defn.type == "agent" else "skill"
            rel = "agent_has_capability" if kind == "agent" else "skill_has_capability"
            for cap in defn.capabilities:
                cap_id = f"{defn.name}:{cap.name}"
                self._add_edge(defn.name, rel, cap_id, evidence="source yaml capabilities", manual=False)
                for cmd in cap.commands:
                    tool = _tool_of(cmd)
                    if tool:
                        self._add_edge(cap_id, "capability_uses_tool", tool,
                                       evidence=f"command: {cmd}", manual=False)
        # knowledge topics
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            for k in defn.knowledge or []:
                topic = k.get("topic") if isinstance(k, dict) else str(k)
                if topic:
                    self._add_edge(defn.name, "definition_has_knowledge", str(topic),
                                   evidence="source yaml knowledge", manual=False)

    def _load_wiring(self) -> None:
        if not self.wiring_path.is_file():
            return
        with open(self.wiring_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        wiring = data.get("wiring") if isinstance(data, dict) else data
        if wiring is None and isinstance(data, dict) and isinstance(data.get("links"), list):
            wiring = data["links"]
        if isinstance(wiring, list):
            for link in wiring:
                agent = link.get("agent")
                skill = link.get("skill")
                if not agent or not skill:
                    continue
                evidence = link.get("evidence") or "manual override"
                manual = bool(link.get("manual"))
                self._add_edge(agent, "agent_depends_skill", skill, evidence=evidence, manual=manual)
        elif isinstance(wiring, dict):
            for agent, links in wiring.items():
                for link in links or []:
                    skill = link.get("skill")
                    if not skill:
                        continue
                    evidence = link.get("evidence") or []
                    manual = bool(link.get("manual"))
                    self._add_edge(agent, "agent_depends_skill", skill,
                                   evidence=", ".join(evidence) if evidence else "manual override",
                                   manual=manual)

    def _add_edge(self, node: str, rel: str, target: str, evidence: str, manual: bool) -> None:
        if rel not in RELATIONSHIP_TYPES:
            raise GraphError(f"unknown relationship type: {rel}")
        if rel == "agent_depends_skill":
            if node not in self.catalog.agents:
                raise GraphError(f"wired agent not in catalog: {node}")
            if target not in self.catalog.skills:
                raise GraphError(f"wired skill not in catalog: {target}")
        self.edges.setdefault(node, [])
        existing = next((e for e in self.edges[node]
                         if e["rel"] == rel and e["target"] == target), None)
        if existing is None:
            self.edges[node].append({"rel": rel, "target": target, "evidence": evidence, "manual": manual})
            return
        # duplicate pair: a manual override replaces an evidence edge and is
        # recorded as a conflict; identical provenance is a silent no-op.
        if existing["manual"] == manual and existing["evidence"] == evidence:
            return
        if manual and not existing["manual"]:
            self._conflict_log.append({
                "node": node, "rel": rel, "target": target,
                "previous": {"evidence": existing["evidence"], "manual": existing["manual"]},
                "override": {"evidence": evidence, "manual": manual},
            })
            existing["evidence"] = evidence
            existing["manual"] = True

    # ---------------------------------------------------------------- edges
    def out_edges(self, node: str, rel: Optional[str] = None) -> List[dict]:
        edges = self.edges.get(node, [])
        if rel:
            edges = [e for e in edges if e["rel"] == rel]
        return list(edges)

    def in_edges(self, node: str, rel: Optional[str] = None) -> List[dict]:
        edges = []
        for src, links in self.edges.items():
            for e in links:
                if e["target"] == node and (rel is None or e["rel"] == rel):
                    edges.append({"source": src, **e})
        return edges

    # backward-compatible helpers
    def agent_skills(self, agent: str) -> List[dict]:
        return [{"skill": e["target"], "evidence": e["evidence"], "manual": e["manual"]}
                for e in self.out_edges(agent, "agent_depends_skill")]

    def skill_agents(self, skill: str) -> List[str]:
        return [e["source"] for e in self.in_edges(skill, "agent_depends_skill")]

    def _skills_of(self, node: str) -> List[str]:
        """Direct skill dependencies of an agent (or skill prerequisites)."""
        if node in self.catalog.agents:
            return [e["target"] for e in self.out_edges(node, "agent_depends_skill")]
        if node in self.catalog.skills:
            return [e["target"] for e in self.out_edges(node, "skill_requires_skill")]
        return []

    # ------------------------------------------------------------- resolvers
    def resolve_agent_skills(self, agent: str, transitive: bool = False) -> List[str]:
        """Direct or transitive skill dependencies for an agent.

        Transitive resolution walks agent -> skill and skill -> skill
        (prerequisite) edges; cycles are broken by the visited set.
        """
        if agent not in self.catalog.agents:
            raise GraphError(f"agent not in catalog: {agent}")
        if not transitive:
            return self._skills_of(agent)
        seen: Set[str] = set()
        ordered: List[str] = []
        frontier = list(self._skills_of(agent))
        while frontier:
            sid = frontier.pop(0)
            if sid in seen:
                continue
            seen.add(sid)
            ordered.append(sid)
            frontier.extend(self._skills_of(sid))
        return ordered

    def transitive_dependencies(self, node: str) -> Dict[str, List[str]]:
        """All dependency-reachable nodes grouped by relationship type.

        Walks agent_depends_skill / skill_requires_skill / agent_is_subagent.
        """
        if node not in self.catalog.agents and node not in self.catalog.skills:
            raise GraphError(f"node not in catalog: {node}")
        result: Dict[str, List[str]] = {t: [] for t in DEPENDENCY_TYPES}
        seen: Set[Tuple[str, str]] = set()
        frontier: List[Tuple[str, str]] = [(node, rel) for rel in DEPENDENCY_TYPES]
        while frontier:
            cur, rel = frontier.pop(0)
            for e in self.out_edges(cur, rel):
                key = (rel, e["target"])
                if key in seen:
                    continue
                seen.add(key)
                if e["target"] not in result[rel]:
                    result[rel].append(e["target"])
                # subagent nodes expand further; skills expand via their
                # own prerequisites; agents via their subagents
                if e["target"] in self.catalog.skills:
                    frontier.append((e["target"], "skill_requires_skill"))
                if e["target"] in self.catalog.agents:
                    frontier.append((e["target"], "agent_is_subagent"))
        return result

    def dependency_explanation(self, node: str) -> List[str]:
        """Human-readable dependency chain for a node."""
        deps = self.transitive_dependencies(node)
        lines = [f"{node}"]
        for rel, targets in deps.items():
            for t in targets:
                lines.append(f"  - [{rel}] {t}")
        return lines

    def capability_graph_for(self, node: str) -> Dict[str, Any]:
        """The capability subgraph reachable from a node (for resolution)."""
        caps: List[str] = []
        tools: List[str] = []
        rel = "agent_has_capability" if node in self.catalog.agents else "skill_has_capability"
        for e in self.out_edges(node, rel):
            caps.append(e["target"])
            for te in self.out_edges(e["target"], "capability_uses_tool"):
                if te["target"] not in tools:
                    tools.append(te["target"])
        for te in self.out_edges(node, "agent_uses_tool" if node in self.catalog.agents else "skill_uses_tool"):
            if te["target"] not in tools:
                tools.append(te["target"])
        return {"capabilities": caps, "tools": tools}

    # ---------------------------------------------------------------- checks
    def orphans(self) -> List[str]:
        referenced = {e["target"] for links in self.edges.values()
                      for e in links if e["rel"] == "agent_depends_skill"}
        return sorted(set(self.catalog.skills) - referenced)

    def unwired_agents(self) -> List[str]:
        return sorted(a for a in self.catalog.agents
                      if not self.out_edges(a, "agent_depends_skill"))

    def cycles(self) -> List[List[str]]:
        """Tarjan SCC over dependency edges (agent/skill nodes only)."""
        nodes = set(self.catalog.agents) | set(self.catalog.skills)
        adj: Dict[str, List[str]] = {n: [] for n in nodes}
        for node, links in self.edges.items():
            if node not in adj:
                continue
            for e in links:
                if e["rel"] not in DEPENDENCY_TYPES:
                    continue
                if e["target"] in adj:
                    adj[node].append(e["target"])
        index, lowlink, on_stack, stack, result, counter = {}, {}, set(), [], [], [0]

        def strongconnect(v: str) -> None:
            index[v] = lowlink[v] = counter[0]
            counter[0] += 1
            stack.append(v)
            on_stack.add(v)
            for w in adj[v]:
                if w not in index:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif w in on_stack:
                    lowlink[v] = min(lowlink[v], index[w])
            if lowlink[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                if len(comp) > 1:
                    result.append(comp)
                elif any(w == e["target"] for e in self.out_edges(w, DEPENDENCY_TYPES)):
                    # self-loop: an entity listing itself as prerequisite
                    result.append([w])

        for n in nodes:
            if n not in index:
                strongconnect(n)
        return result

    def conflicts(self) -> List[Dict[str, Any]]:
        """Manual overrides that replaced evidence-backed edges."""
        return list(self._conflict_log)

    def topological_order(self, root: Optional[str] = None) -> List[str]:
        """Kahn's algorithm over dependency edges; deterministic by name.

        Dependencies (prerequisites) are ordered before their dependents:
        edges are reversed (target -> node) so indegree 0 = no dependencies.
        """
        nodes = set(self.catalog.agents) | set(self.catalog.skills)
        adj: Dict[str, List[str]] = {n: [] for n in nodes}
        indeg: Dict[str, int] = {n: 0 for n in nodes}
        for node, links in self.edges.items():
            if node not in nodes:
                continue
            for e in links:
                if e["rel"] not in DEPENDENCY_TYPES or e["target"] not in nodes:
                    continue
                adj[e["target"]].append(node)
                indeg[node] += 1
        if root is not None:
            if root not in nodes:
                raise GraphError(f"root not in catalog: {root}")
            reachable: Set[str] = set()
            frontier = [root]
            while frontier:
                cur = frontier.pop(0)
                for t in adj[cur]:
                    if t not in reachable:
                        reachable.add(t)
                        frontier.append(t)
            reachable.add(root)
            nodes = {n for n in nodes if n in reachable}
            adj = {n: [t for t in ts if t in reachable] for n, ts in adj.items() if n in reachable}
            indeg = {n: indeg[n] for n in nodes}
        import heapq
        heap = [n for n in nodes if indeg[n] == 0]
        heapq.heapify(heap)
        order: List[str] = []
        while heap:
            n = heapq.heappop(heap)
            order.append(n)
            for t in sorted(adj[n]):
                indeg[t] -= 1
                if indeg[t] == 0:
                    heapq.heappush(heap, t)
        return order

    # -------------------------------------------------------------- summary
    def summary(self) -> Dict[str, object]:
        return {
            "agents": len(self.catalog.agents),
            "skills": len(self.catalog.skills),
            "wired_agents": len([a for a in self.catalog.agents
                                 if self.out_edges(a, "agent_depends_skill")]),
            "links": sum(len(v) for v in self.edges.values()),
            "orphan_skills": len(self.orphans()),
            "unwired_agents": len(self.unwired_agents()),
            "cycles": self.cycles(),
            "conflicts": self.conflicts(),
            "topo_order": self.topological_order(),
            "files_scanned": len(self.catalog.agents) + len(self.catalog.skills),
        }