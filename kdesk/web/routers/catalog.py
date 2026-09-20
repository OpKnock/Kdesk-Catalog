"""Catalog inspection endpoints: stats, search, graph, capabilities, adapters."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from kdesk.adapters import AdapterRegistry
from kdesk.capabilities import CapabilityIndex
from kdesk.graph import CatalogGraph
from kdesk.stats import StatsError

router = APIRouter(prefix="/api", tags=["catalog"])


def _json(data: Any) -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(data, default=str)))


@router.get("/stats")
def stats(fast: bool = True) -> JSONResponse:
    from kdesk.web.app import get_state

    try:
        return _json(get_state().stats(fast=fast))
    except StatsError as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)


@router.get("/search")
def search(q: str = Query("", min_length=1), limit: int = 30) -> JSONResponse:
    from kdesk.web.app import get_state

    catalog = get_state().catalog
    hits = catalog.search(q)[:limit]
    return _json([
        {"type": h.type, "name": h.name, "category": h.category}
        for h in hits
    ])


@router.get("/definition/{kind}/{name}")
def definition(kind: str, name: str) -> JSONResponse:
    import dataclasses

    from kdesk.web.app import get_state

    catalog = get_state().catalog
    store = catalog.agents if kind == "agent" else catalog.skills
    item = store.get(name)
    if item is None:
        return JSONResponse({"error": "not found"}, status_code=404)
    if hasattr(item, "to_dict"):
        d = item.to_dict()
    elif dataclasses.is_dataclass(item):
        d = dataclasses.asdict(item)
    elif isinstance(item, dict):
        d = dict(item)
    else:
        d = {"repr": repr(item)}
    return _json({"type": kind, **d})


@router.get("/graph")
def graph(agent: Optional[str] = None) -> JSONResponse:
    from kdesk.web.app import get_state

    state = get_state()
    g = CatalogGraph(state.catalog,
                     wiring_path=state.root / "skills" / "wiring.json")
    if agent:
        return _json(g.agent_skills(agent))
    return _json(g.summary())


@router.get("/capabilities")
def capabilities(tool: Optional[str] = None) -> JSONResponse:
    from kdesk.web.app import get_state

    catalog = get_state().catalog
    idx = CapabilityIndex(list(catalog.agents.values()) + list(catalog.skills.values()))
    if tool:
        return _json([
            {"definition": d, "capability": c}
            for d, c in idx.capabilities_for_tool(tool)
        ])
    return _json(idx.summary())


@router.get("/adapters")
def adapters(platform: Optional[str] = None) -> JSONResponse:
    from kdesk.web.app import get_state

    root = get_state().root
    registry = AdapterRegistry(root)
    if platform:
        a = registry.get(platform)
        if a is None:
            return JSONResponse({"error": f"unknown platform: {platform}"},
                                status_code=404)
        return _json(a.verify())
    return _json(registry.summary())


@router.get("/workflows")
def workflows() -> JSONResponse:
    from kdesk.web.app import get_state

    from kdesk.workflow import WorkflowEngine

    state = get_state()
    engine = WorkflowEngine(state.catalog, workflows_dir=state.root / "workflows")
    return _json(engine.summary())


@router.get("/platforms")
def platforms() -> JSONResponse:
    from kdesk.platforms import get_registry

    reg = get_registry()
    return _json([
        {"id": p.id, "name": p.display_name,
         "support": (p.support_level.value
                     if hasattr(p.support_level, "value") else str(p.support_level))}
        for p in reg.all()
    ])
