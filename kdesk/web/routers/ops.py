"""Action endpoints: converter, doctor, engine, marketplace, installs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["ops"])


def _json(data: Any) -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(data, default=str)))


def _state():
    from kdesk.web.app import get_state
    return get_state()


# ---------------------------------------------------------------- converter

class ConvertRequest(BaseModel):
    platforms: List[str] = ["cursor"]
    output: Optional[str] = None


@router.post("/convert")
def convert(req: ConvertRequest) -> JSONResponse:
    from kdesk.converters import constants as cfg
    from kdesk.converters.pipeline import convert_all, parse_platforms

    state = _state()
    try:
        platforms = parse_platforms(req.platforms)
    except ValueError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    out = Path(req.output) if req.output else state.root / "platform-agents"
    prev_quiet, prev_dir = cfg.QUIET, cfg.UNIVERSAL_DIR
    cfg.QUIET = True
    try:
        convert_all(platforms, out)
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)
    finally:
        cfg.QUIET, cfg.UNIVERSAL_DIR = prev_quiet, prev_dir
    counts = {}
    for p in platforms:
        files = [f for f in (out / p).rglob("*") if f.is_file()
                 and f.name not in ("README.md", "manifest.yaml")]
        counts[p] = len(files)
    return _json({"status": "ok", "platforms": platforms, "files": counts})


@router.post("/validate")
def validate() -> JSONResponse:
    from kdesk.converters.pipeline import validate_agents

    ok = validate_agents()
    return _json({"valid": ok})


# -------------------------------------------------------------------- doctor

class DoctorRequest(BaseModel):
    platform: Optional[str] = None
    project_root: Optional[str] = None
    mode: str = "check"
    fix: bool = False
    dry_run: bool = True
    threshold: int = 90


@router.post("/doctor")
def doctor(req: DoctorRequest) -> JSONResponse:
    from kdesk.adapters import AdapterRegistry
    from kdesk.doctor import Doctor

    state = _state()
    registry = AdapterRegistry(state.root)
    base = Path(req.project_root).resolve() if req.project_root else Path.cwd()
    doc = Doctor(registry, base=base, registry_root=state.root)

    if req.mode == "check":
        if req.platform:
            return _json(doc.check(req.platform))
        return _json(doc.summary())
    if req.mode == "scan":
        return _json(doc.scan_project(base).to_dict())
    if req.mode in ("diagnose", "fix"):
        result = doc.diagnose(
            platform=req.platform or "generic",
            project_root=base,
            fix=(req.mode == "fix" or req.fix),
            dry_run=req.dry_run,
        )
        out: Dict[str, Any] = {"report": result["report"].to_dict()}
        if result["fix_report"]:
            out["fix_report"] = result["fix_report"].to_dict()
        return _json(out)
    return JSONResponse({"error": f"unknown mode: {req.mode}"}, status_code=400)


# -------------------------------------------------------------------- engine

class EngineRequest(BaseModel):
    request: str
    top: int = 8
    json_output: bool = True


@router.post("/resolve")
def resolve(req: EngineRequest) -> JSONResponse:
    from kdesk.engine import Engine

    engine = Engine(_state().root)
    return _json(engine.resolve(req.request, top=req.top).to_dict())


class WhyRequest(BaseModel):
    request: str
    target: str


@router.post("/why")
def why(req: WhyRequest) -> JSONResponse:
    from kdesk.engine import Engine

    data = Engine(_state().root).why(req.request, req.target)
    if data is None:
        return JSONResponse({"error": f"unknown target: {req.target}"},
                            status_code=404)
    return _json(data)


class RunRequest(BaseModel):
    request: str
    base: Optional[str] = None
    auto_approve: bool = False
    dry_run: bool = True
    timeout: float = 120.0


@router.post("/plan")
def plan(req: RunRequest) -> JSONResponse:
    from kdesk.engine import Engine

    return _json(Engine(_state().root).plan(req.request).to_dict())


@router.post("/run")
def run(req: RunRequest) -> JSONResponse:
    from kdesk.engine import Engine

    base = Path(req.base) if req.base else Path.cwd()
    result = Engine(_state().root).run(
        req.request, base=base, auto_approve=req.auto_approve,
        timeout_s=req.timeout, dry_run=req.dry_run)
    return _json(result.to_dict())


@router.get("/history")
def history(limit: int = 20) -> JSONResponse:
    from kdesk.engine import Engine

    return _json(Engine(_state().root).history(limit=limit))


@router.get("/inspect/{execution_id}")
def inspect_execution(execution_id: str) -> JSONResponse:
    from kdesk.engine import Engine

    data = Engine(_state().root).inspect(execution_id)
    if data is None:
        return JSONResponse({"error": "unknown execution"}, status_code=404)
    return _json(data)


# --------------------------------------------------------------- marketplace

@router.get("/skills")
def skills() -> JSONResponse:
    from kdesk.marketplace import Marketplace

    mp = Marketplace(_state().root)
    return _json({
        "stats": mp.stats(),
        "entries": [
            {"name": e.name, "version": e.version, "category": e.category,
             "description": e.description}
            for e in mp.list_all()
        ],
    })


@router.get("/skills/search")
def skills_search(q: str = "", limit: int = 20) -> JSONResponse:
    from kdesk.marketplace import Marketplace

    mp = Marketplace(_state().root)
    return _json([
        {"name": e.name, "version": e.version, "category": e.category,
         "description": e.description}
        for e in mp.search(q, limit=limit)
    ])


@router.post("/skills/install")
def skills_install(spec: str) -> JSONResponse:
    from kdesk.marketplace import Marketplace

    entry = Marketplace(_state().root).resolve(spec)
    if entry is None:
        return JSONResponse({"error": f"no match: {spec}"}, status_code=404)
    return _json({"status": "resolved", "name": entry.name,
                  "version": entry.version, "checksum": entry.checksum,
                  "dependencies": entry.dependencies})


# -------------------------------------------------------- delegate / version

@router.post("/delegate")
def delegate(agent: str) -> JSONResponse:
    from kdesk.delegation import SubAgentResolver

    state = _state()
    plan = SubAgentResolver(state.catalog).resolve(agent, input_data={})
    if plan is None:
        return _json({"agent": agent, "delegated": False,
                      "reason": "no sub_agents declared"})
    return _json({"agent": agent, "delegated": True, **plan.summary()})


@router.get("/resolve-version")
def resolve_version(spec: str) -> JSONResponse:
    from kdesk.versioning import VersionResolver, build_available_versions

    catalog = _state().catalog
    available = build_available_versions(
        {n: True for n in list(catalog.agents) + list(catalog.skills)})
    result = VersionResolver().resolve(spec, available)
    if result is None:
        return JSONResponse({"error": f"no match: {spec}"}, status_code=404)
    return _json({"resolved": result})


@router.get("/telemetry")
def telemetry() -> JSONResponse:
    from kdesk.telemetry import summary as telemetry_summary

    return _json(telemetry_summary(_state().root))


# ------------------------------------------------------------------- install

class InstallRequest(BaseModel):
    platform: str
    base: Optional[str] = None
    scope: Optional[str] = None
    tool: Optional[str] = None
    dry_run: bool = True


@router.post("/install")
def install(req: InstallRequest) -> JSONResponse:
    from kdesk.adapters import AdapterRegistry
    from kdesk.installer import Installer, InstallError

    root = _state().root
    installer = Installer(AdapterRegistry(root), dry_run=req.dry_run)
    try:
        result = installer.install(
            req.platform,
            base=Path(req.base) if req.base else None,
            scope=req.scope, tool=req.tool)
    except InstallError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return _json(result)


@router.get("/drift")
def drift(platform: Optional[str] = None) -> JSONResponse:
    from kdesk.adapters import AdapterRegistry
    from kdesk.installer import Installer, InstallError

    try:
        report = Installer(AdapterRegistry(_state().root)).drift(platform)
    except InstallError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return _json(report)
