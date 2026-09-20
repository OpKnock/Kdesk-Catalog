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
def search(q: str = Query("", min_length=1, max_length=200),
           limit: int = Query(30, ge=1, le=100),
           type: str = "all", category: str = Query("", max_length=80)) -> JSONResponse:
    from kdesk.web.app import get_state

    kind = type if type in ("agent", "skill") else "all"
    catalog = get_state().catalog
    hits = catalog.search(q)[: limit * 5]
    if kind != "all":
        hits = [h for h in hits if h.type == kind]
    if category:
        hits = [h for h in hits if (h.category or "") == category]
    return _json([
        {"type": h.type, "name": h.name, "category": h.category}
        for h in hits[:limit]
    ])


@router.get("/categories")
def categories() -> JSONResponse:
    from collections import Counter

    from kdesk.web.app import get_state

    catalog = get_state().catalog
    agents = Counter((a.category or "other") for a in catalog.agents.values())
    skills = Counter((s.category or "other") for s in catalog.skills.values())
    return _json({
        "agent": dict(sorted(agents.items(), key=lambda kv: -kv[1])),
        "skill": dict(sorted(skills.items(), key=lambda kv: -kv[1])),
    })


@router.get("/browse")
def browse(type: str = "all", category: str = Query("", max_length=80),
           q: str = Query("", max_length=200),
           limit: int = Query(60, ge=1, le=200),
           offset: int = Query(0, ge=0)) -> JSONResponse:
    from kdesk.web.app import get_state

    catalog = get_state().catalog
    pools = []
    if type in ("all", "agent"):
        pools += [("agent", d) for d in catalog.agents.values()]
    if type in ("all", "skill"):
        pools += [("skill", d) for d in catalog.skills.values()]
    if category:
        pools = [(k, d) for k, d in pools if (d.category or "") == category]
    if q:
        needle = q.lower()
        pools = [(k, d) for k, d in pools
                 if needle in d.name.lower()
                 or needle in (d.description or "").lower()]
    pools.sort(key=lambda kd: kd[1].name)
    total = len(pools)
    page = pools[offset: offset + limit]
    return _json({
        "total": total, "offset": offset, "limit": limit,
        "items": [{"type": k, "name": d.name, "category": d.category,
                   "description": (d.description or "")[:140]}
                  for k, d in page],
    })


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


@router.get("/official")
def official() -> JSONResponse:
    """Hand-written runnable Kdesk agent implementations (*.sh/*.py)."""
    from kdesk.web.app import get_state

    base = get_state().root / "agents"
    items = []
    if base.is_dir():
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in (".sh", ".py"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            desc = ""
            for line in text.splitlines()[:15]:
                s = line.strip().lstrip("#").strip()
                if s and not s.startswith("!") and len(s) > 12:
                    desc = s[:160]
                    break
            rel = str(path.relative_to(base)).replace("\\", "/")
            items.append({
                "name": path.stem, "path": f"agents/{rel}",
                "language": "bash" if path.suffix == ".sh" else "python",
                "size": path.stat().st_size, "description": desc,
            })
    return _json({"total": len(items), "items": items})


@router.get("/official/file")
def official_file(path: str = "") -> JSONResponse:
    """Read one official implementation (constrained under agents/)."""
    from kdesk.web.app import get_state

    base = (get_state().root / "agents").resolve()
    target = (base / path.replace("\\", "/")).resolve()
    if base not in target.parents and target != base:
        return JSONResponse({"error": "path escapes agents/"}, status_code=400)
    if target.suffix not in (".sh", ".py") or not target.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)
    try:
        content = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return JSONResponse({"error": str(exc)[:200]}, status_code=500)
    if len(content) > 60000:
        content = content[:60000] + "\n…[truncated]"
    return _json({"path": str(target.relative_to(base)).replace("\\", "/"),
                  "content": content})
