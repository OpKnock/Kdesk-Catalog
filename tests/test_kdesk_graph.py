"""kdesk unit tests: wiring graph, cycles, resolvers."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.graph import CatalogGraph, GraphError
from kdesk.registry import Catalog


def _catalog(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    (base / "devops" / "skill").mkdir(parents=True)
    for name in ("agent-a", "agent-b"):
        (base / "devops" / "agent" / f"{name}.yaml").write_text(
            f"name: {name}\ncategory: devops\ndescription: {'x' * 250}\ntype: agent\nskills: []\n",
            encoding="utf-8",
        )
    for name in ("skill-1", "skill-2"):
        (base / "devops" / "skill" / f"{name}.yaml").write_text(
            f"name: {name}\ncategory: devops\ndescription: {'x' * 250}\ntype: skill\n",
            encoding="utf-8",
        )
    return Catalog(base)


def _wiring(tmp_path, links):
    wiring = tmp_path / "skills" / "wiring.json"
    wiring.parent.mkdir(parents=True, exist_ok=True)
    wiring.write_text(json.dumps({"links": links}), encoding="utf-8")
    return wiring


def test_graph_edges_from_source_and_wiring(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = _wiring(
        tmp_path,
        [{"agent": "agent-a", "skill": "skill-1", "evidence": "helm", "manual": False}],
    )
    graph = CatalogGraph(catalog, wiring)
    assert graph.agent_skills("agent-a") == [{"skill": "skill-1", "evidence": "helm", "manual": False}]
    assert graph.skill_agents("skill-1") == ["agent-a"]


def test_graph_source_yaml_edges(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    (base / "devops" / "skill").mkdir(parents=True)
    (base / "devops" / "agent" / "agent-a.yaml").write_text(
        f"name: agent-a\ncategory: devops\ndescription: {'x' * 250}\ntype: agent\nskills: ['skill-1']\n",
        encoding="utf-8",
    )
    (base / "devops" / "skill" / "skill-1.yaml").write_text(
        f"name: skill-1\ncategory: devops\ndescription: {'x' * 250}\ntype: skill\n",
        encoding="utf-8",
    )
    catalog = Catalog(base)
    graph = CatalogGraph(catalog, tmp_path / "nope-wiring.json")
    links = graph.agent_skills("agent-a")
    assert len(links) == 1 and links[0]["skill"] == "skill-1"


def test_graph_missing_wiring_ok(tmp_path):
    catalog = _catalog(tmp_path)
    graph = CatalogGraph(catalog, tmp_path / "no-such-wiring.json")
    assert graph.summary()["links"] == 0


def test_graph_unknown_agent_raises(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = _wiring(tmp_path, [{"agent": "ghost", "skill": "skill-1"}])
    with pytest.raises(GraphError):
        CatalogGraph(catalog, wiring)


def test_graph_unknown_skill_raises(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = _wiring(tmp_path, [{"agent": "agent-a", "skill": "ghost"}])
    with pytest.raises(GraphError):
        CatalogGraph(catalog, wiring)


def test_graph_orphans_and_unwired(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = _wiring(tmp_path, [{"agent": "agent-a", "skill": "skill-1"}])
    graph = CatalogGraph(catalog, wiring)
    assert graph.orphans() == ["skill-2"]
    assert graph.unwired_agents() == ["agent-b"]


def test_graph_cycles_none_in_bipartite(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = _wiring(
        tmp_path,
        [{"agent": "agent-a", "skill": "skill-1"}, {"agent": "agent-b", "skill": "skill-2"}],
    )
    graph = CatalogGraph(catalog, wiring)
    assert graph.cycles() == []


def test_graph_duplicate_link_dedup(tmp_path):
    catalog = _catalog(tmp_path)
    wiring = _wiring(
        tmp_path,
        [
            {"agent": "agent-a", "skill": "skill-1"},
            {"agent": "agent-a", "skill": "skill-1", "manual": True},
        ],
    )
    graph = CatalogGraph(catalog, wiring)
    assert len(graph.agent_skills("agent-a")) == 1