#!/usr/bin/env python3
"""Generate an interactive HTML dependency graph of the agent/skill catalog.

Usage:
    python scripts/generate-graph.py --output graph.html [--category ml] [--max-nodes 200]

Produces a self-contained HTML file with an interactive force-directed graph
showing agent->skill wiring, sub-agent delegation, and tool usage.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from kdesk.registry import Catalog, default_repo_root  # noqa: E402


def _load_wiring(root: Path):
    """Load agent->skill wiring from skills/wiring.json."""
    wiring_path = root / "skills" / "wiring.json"
    if not wiring_path.is_file():
        return {}
    try:
        data = json.loads(wiring_path.read_text(encoding="utf-8"))
        return {aid: [l["skill"] for l in links if l.get("skill")]
                for aid, links in (data.get("wiring") or {}).items()}
    except (OSError, ValueError, KeyError):
        return {}


def build_graph_data(catalog: Catalog, root=None, category=None, max_nodes=300):
    """Build nodes/links arrays for visualization."""
    import random
    random.seed(42)

    root = root or default_repo_root()
    wiring = _load_wiring(root)

    nodes = []
    links = []
    node_ids = set()

    def add_node(id, label, group, size=5):
        if id not in node_ids:
            nodes.append({"id": id, "label": label, "group": group, "size": size})
            node_ids.add(id)
            return True
        return False

    agents = list(catalog.agents.values())
    skills = list(catalog.skills.values())

    if category:
        agents = [a for a in agents if a.category == category]
        skills = [s for s in skills if s.category == category]

    # Budget allocation
    budget_agents = int(max_nodes * 0.45)
    budget_skills = int(max_nodes * 0.35)
    budget_tools = max_nodes - budget_agents - budget_skills

    # Prioritize wired agents (have skill links via wiring.json or YAML)
    wired_agents = [a for a in agents if a.skills or wiring.get(a.name)]
    unwired_agents = [a for a in agents if not (a.skills or wiring.get(a.name))]

    # Collect referenced skills
    referenced_skills = set()
    for a in wired_agents:
        referenced_skills.update(a.skills[:10])
        referenced_skills.update(wiring.get(a.name, [])[:10])

    skill_by_name = {s.name: s for s in skills}
    ref_skills = [skill_by_name[s] for s in sorted(referenced_skills) if s in skill_by_name]

    selected_agents = wired_agents[:budget_agents]
    remaining = budget_agents - len(selected_agents)
    if remaining > 0:
        selected_agents += random.sample(unwired_agents, min(remaining, len(unwired_agents)))
    selected_skills = ref_skills[:budget_skills]

    for agent in selected_agents:
        add_node(agent.name, agent.display_name or agent.name, "agent",
                 size=max(4, min(15, len(agent.capabilities) + 2)))

    for skill in selected_skills:
        add_node(skill.name, skill.display_name or skill.name, "skill", size=6)

    # Links: wiring-based agent -> skill
    for agent in selected_agents:
        all_skills = set(agent.skills) | set(wiring.get(agent.name, []))
        for sid in sorted(all_skills)[:10]:
            if sid in node_ids:
                links.append({"source": agent.name, "target": sid, "type": "uses_skill"})
        for sa in agent.sub_agents[:8]:
            if sa in node_ids:
                links.append({"source": agent.name, "target": sa, "type": "delegates_to"})

    # Tool links
    from collections import Counter
    tool_counts = Counter()
    for d in list(catalog.agents.values()) + list(catalog.skills.values()):
        for t in d.tools:
            tool_counts[t] += 1

    top_tools = [t for t, _ in tool_counts.most_common(budget_tools)]
    for t in top_tools:
        tid = f"tool:{t}"
        add_node(tid, t, "tool", size=max(3, min(12, tool_counts[t] // 2)))

    for d in selected_agents + selected_skills:
        for t in d.tools:
            tid = f"tool:{t}"
            if tid in node_ids and d.name in node_ids:
                links.append({"source": d.name, "target": tid, "type": "uses_tool"})

    return {"nodes": nodes, "links": links,
            "meta": {"agents": len(selected_agents), "skills": len(selected_skills),
                     "categories": sorted({a.category for a in selected_agents})}}


HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Kdesk Catalog Dependency Graph</title>
<style>
  body { margin: 0; overflow: hidden; background: #0d1117; font-family: -apple-system, sans-serif; }
  #controls { position: absolute; top: 10px; left: 10px; z-index: 10; color: #c9d1d9;
              background: rgba(22,27,34,.9); padding: 12px; border-radius: 8px; }
  #controls h3 { margin: 0 0 8px; font-size: 14px; color: #58a6ff; }
  .legend-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
  svg { width: 100vw; height: 100vh; cursor: grab; }
  .link { stroke-opacity: 0.35; }
  .node-label { fill: #c9d1d9; font-size: 9px; pointer-events: none; text-anchor: middle; }
  #tooltip { position: absolute; pointer-events: none; background: #161b22; color: #c9d1d9;
             border: 1px solid #30363d; padding: 6px 10px; border-radius: 6px; font-size: 12px;
             display: none; z-index: 20; }
  #search { background:#0d1117; color:#c9d1d9; border:1px solid #30363d; border-radius:4px; padding:4px 8px; width:180px;}
</style>
</head>
<body>
<div id="controls">
  <h3>&#128295; Kdesk Catalog Graph</h3>
  <div><span class="legend-dot" style="background:#58a6ff"></span>Agents</div>
  <div><span class="legend-dot" style="background:#3fb950"></span>Skills</div>
  <div><span class="legend-dot" style="background:#f0883e"></span>Tools</div>
  <input id="search" placeholder="Search nodes..." oninput="highlight(this.value)">
  <div id="stats" style="margin-top:6px;font-size:11px;color:#8b949e"></div>
</div>
<svg id="graph"></svg>
<div id="tooltip"></div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const DATA = __DATA__;
const COLORS = { agent: "#58a6ff", skill: "#3fb950", tool: "#f0883e" };
const LINK_COLORS = { uses_skill: "#3fb95055", delegates_to: "#bc8cff88", uses_tool: "#f0883e33" };
const LINK_WIDTHS = { uses_skill: 1.2, delegates_to: 2.2, uses_tool: 0.7 };

const width = window.innerWidth, height = window.innerHeight;
const svg = d3.select("#graph");
const g = svg.append("g");

svg.call(d3.zoom().scaleExtent([0.05, 8]).on("zoom", e => g.attr("transform", e.transform)));

const simulation = d3.forceSimulation(DATA.nodes)
  .force("link", d3.forceLink(DATA.links).id(d => d.id).distance(d =>
      d.type === "delegates_to" ? 90 : d.type === "uses_tool" ? 60 : 70))
  .force("charge", d3.forceManyBody().strength(-60))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collision", d3.forceCollide().radius(d => d.size + 2));

const link = g.append("g").selectAll("line")
  .data(DATA.links).join("line")
  .attr("class", "link")
  .attr("stroke", d => LINK_COLORS[d.type] || "#30363d")
  .attr("stroke-width", d => LINK_WIDTHS[d.type] || 1);

const node = g.append("g").selectAll("circle")
  .data(DATA.nodes).join("circle")
  .attr("r", d => d.size)
  .attr("fill", d => COLORS[d.group])
  .attr("stroke", "#0d1117").attr("stroke-width", 1)
  .call(drag(simulation))
  .on("mouseover", showTip).on("mouseout", hideTip);

const labels = g.append("g").selectAll("text")
  .data(DATA.nodes.filter(d => d.group !== "tool")).join("text")
  .text(d => d.label.length > 24 ? d.label.slice(0,22)+"…" : d.label)
  .attr("class", "node-label")
  .attr("dy", d => d.size + 11);

simulation.on("tick", () => {
  link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  node.attr("cx", d => d.x).attr("cy", d => d.y);
  labels.attr("x", d => d.x).attr("y", d => d.y);
});

function drag(sim) {
  return d3.drag().on("start", (e,d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on("drag", (e,d) => { d.fx = e.x; d.fy = e.y; })
    .on("end", (e,d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; });
}

const tip = document.getElementById("tooltip");
function showTip(e, d) {
  const conn = DATA.links.filter(l => l.source.id === d.id || l.target.id === d.id).length;
  tip.innerHTML = `<b style="color:${COLORS[d.group]}">${d.label}</b><br>type: ${d.group}<br>connections: ${conn}`;
  tip.style.display = "block";
  tip.style.left = (e.pageX + 12) + "px"; tip.style.top = (e.pageY - 10) + "px";
}
function hideTip() { tip.style.display = "none"; }

function highlight(q) {
  q = q.toLowerCase();
  node.attr("opacity", d => !q || d.label.toLowerCase().includes(q) ? 1 : 0.12);
  labels.attr("opacity", d => !q || d.label.toLowerCase().includes(q) ? 1 : 0.12);
  link.attr("opacity", d => !q ||
    (d.source.label && d.source.label.toLowerCase().includes(q)) ||
    (d.target.label && d.target.label.toLowerCase().includes(q)) ? 1 : 0.06);
}

document.getElementById("stats").textContent =
  `${DATA.meta.agents} agents · ${DATA.meta.skills} skills · ${DATA.nodes.length} nodes`;
</script>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", default="catalog-graph.html", help="output HTML path")
    ap.add_argument("--root", default=None, help="repo root")
    ap.add_argument("--category", default=None, help="filter to one category/division")
    ap.add_argument("--max-nodes", type=int, default=400, help="max nodes to render")
    args = ap.parse_args()

    root = Path(args.root) if args.root else default_repo_root()
    catalog = Catalog.from_repo(root)

    data = build_graph_data(catalog, root=root, category=args.category, max_nodes=args.max_nodes)

    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    out = Path(args.output)
    out.write_text(html, encoding="utf-8")

    print(f"[OK] wrote {out} ({len(data['nodes'])} nodes, {len(data['links'])} links)")
    print(f"     open in browser: {out.resolve()}")


if __name__ == "__main__":
    main()