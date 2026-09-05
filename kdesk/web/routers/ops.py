"""Action endpoints: converter, doctor, engine, marketplace, installs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, File, Form, Query, UploadFile
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
    samples = {}
    for p in platforms:
        files = [f for f in (out / p).rglob("*") if f.is_file()
                 and f.name not in ("README.md", "manifest.yaml")]
        counts[p] = len(files)
        samples[p] = sorted(
            str(f.relative_to(out / p)).replace("\\", "/") for f in files
        )[:100]
    return _json({"status": "ok", "platforms": platforms, "files": counts,
                  "sample_paths": samples})


@router.post("/validate")
def validate() -> JSONResponse:
    from kdesk.converters.pipeline import validate_agents

    ok = validate_agents()
    return _json({"valid": ok})


MAX_UPLOAD_FILES = 20
MAX_UPLOAD_BYTES = 200 * 1024


def _read_uploads(files) -> list:
    """Read+parse uploaded YAML files. Returns [(filename, agent_dict)]."""
    import yaml

    if len(files) > MAX_UPLOAD_FILES:
        raise ValueError(f"max {MAX_UPLOAD_FILES} files per upload")
    out = []
    for f in files:
        raw = f.file.read()
        if len(raw) > MAX_UPLOAD_BYTES:
            raise ValueError(f"{f.filename}: over {MAX_UPLOAD_BYTES // 1024}KB limit")
        try:
            doc = yaml.safe_load(raw.decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"{f.filename}: invalid YAML ({exc})")
        if not isinstance(doc, dict) or not doc.get("name"):
            raise ValueError(f"{f.filename}: missing required 'name' field")
        doc = dict(doc)
        doc["file_path"] = f.filename or "upload.yaml"
        out.append((f.filename or "upload.yaml", doc))
    if not out:
        raise ValueError("no files uploaded")
    return out


@router.post("/convert-upload")
async def convert_upload(files: List[UploadFile] = File(...),
                         platforms: str = Form("cursor")):
    return await _convert_upload_impl(files, platforms)


async def _convert_upload_impl(files, platforms):
    if not files:
        return JSONResponse({"error": "no files uploaded"}, status_code=400)
    try:
        docs = _read_uploads(files)
    except ValueError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return _convert_docs(docs, platforms)


def _convert_docs(docs, platforms):
    """Convert [(source_name, agent_dict)] to platform artifacts (shared)."""
    from kdesk.converters.native import (
        convert_to_claude_code,
        convert_to_copilot,
        convert_to_cursor,
        convert_to_generic,
        convert_to_opencode,
        convert_to_windsurf,
    )
    from kdesk.converters.pipeline import parse_platforms
    from kdesk.converters.standard import convert_new_platform

    try:
        if isinstance(platforms, str):
            platforms = [p.strip() for p in platforms.split(",") if p.strip()]
        wanted = parse_platforms(platforms)
    except ValueError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)

    native = {
        "claude_code": convert_to_claude_code,
        "cursor": convert_to_cursor,
        "github_copilot": convert_to_copilot,
        "windsurf": convert_to_windsurf,
        "opencode": convert_to_opencode,
        "generic": convert_to_generic,
    }
    from kdesk.converters.constants import NEW_PLATFORMS

    artifacts = []
    for filename, agent in docs:
        for platform in wanted:
            try:
                if platform in native:
                    out = native[platform](agent)
                elif platform in NEW_PLATFORMS:
                    out = convert_new_platform(platform, agent)
                else:
                    continue
                artifacts.append({"source": filename, "platform": platform,
                                  "path": out.get("rel_path", ""),
                                  "content": out.get("content", "")})
            except Exception as exc:
                artifacts.append({"source": filename, "platform": platform,
                                  "error": str(exc)[:300]})
    return _json({"status": "ok", "files": len(docs),
                  "platforms": wanted, "artifacts": artifacts})


class ConvertSelectedRequest(BaseModel):
    names: List[str] = []
    platforms: List[str] = ["cursor"]


@router.post("/convert-selected")
def convert_selected(req: ConvertSelectedRequest):
    """Convert named catalog definitions (max 25) with full contents back."""
    if not req.names:
        return JSONResponse({"error": "no definitions selected"}, status_code=400)
    if len(req.names) > 25:
        return JSONResponse({"error": "max 25 definitions per conversion"},
                            status_code=400)
    catalog = _state().catalog
    docs = []
    missing = []
    for name in req.names:
        item = catalog.agents.get(name) or catalog.skills.get(name)
        if item is None:
            missing.append(name)
            continue
        doc = dict(item.raw or {})
        doc["file_path"] = str(getattr(item, "source_path", "") or name)
        docs.append((name, doc))
    if missing:
        return JSONResponse({"error": f"unknown definitions: {', '.join(missing[:8])}"},
                            status_code=404)
    return _convert_docs(docs, req.platforms)


@router.get("/convert/file")
def convert_file(platform: str = "", path: str = "") -> JSONResponse:
    """Download one generated file (constrained under platform-agents/)."""
    from fastapi.responses import PlainTextResponse

    root = _state().root
    base = (root / "platform-agents").resolve()
    if not platform or not path:
        return JSONResponse({"error": "platform and path required"}, status_code=400)
    target = (base / platform / path.replace("\\", "/")).resolve()
    if base not in target.parents:
        return JSONResponse({"error": "path escapes platform-agents/"},
                            status_code=400)
    if not target.is_file() or target.stat().st_size > 2 * 1024 * 1024:
        return JSONResponse({"error": "not found or too large"}, status_code=404)
    try:
        content = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return JSONResponse({"error": str(exc)[:200]}, status_code=500)
    return PlainTextResponse(content)


@router.post("/doctor-upload")
async def doctor_upload(files: List[UploadFile] = File(...),
                        platform: str = Form("generic"),
                        mode: str = Form("diagnose")):
    return await _doctor_upload_impl(files, platform, mode)


async def _doctor_upload_impl(files, platform, mode):
    import shutil
    import tempfile

    from kdesk.adapters import AdapterRegistry
    from kdesk.doctor import Doctor

    if not files:
        return JSONResponse({"error": "no files uploaded"}, status_code=400)
    if mode not in ("scan", "diagnose"):
        return JSONResponse({"error": "mode must be scan or diagnose"},
                            status_code=400)
    tmp = Path(tempfile.mkdtemp(prefix="kdesk_upload_"))
    try:
        for f in files[:MAX_UPLOAD_FILES]:
            raw = f.file.read()
            if len(raw) > MAX_UPLOAD_BYTES:
                return JSONResponse(
                    {"error": f"{f.filename}: over size limit"}, status_code=400)
            name = Path(f.filename or "file.md").name
            (tmp / name).write_bytes(raw)
        state = _state()
        doc = Doctor(AdapterRegistry(state.root), base=tmp,
                     registry_root=state.root, catalog=state.catalog)
        if mode == "scan":
            return _json(doc.scan_project(tmp).to_dict())
        result = doc.diagnose(platform=platform, project_root=tmp,
                              fix=False, dry_run=True)
        out: Dict[str, Any] = {"report": result["report"].to_dict()}
        if result["fix_report"]:
            out["fix_report"] = result["fix_report"].to_dict()
        return _json(out)
    except Exception as exc:
        return JSONResponse({"error": str(exc)[:300]}, status_code=500)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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
    doc = Doctor(registry, base=base, registry_root=state.root,
                 catalog=state.catalog)

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

    engine = Engine(_state().root, catalog=_state().catalog)
    return _json(engine.resolve(req.request, top=req.top).to_dict())


class WhyRequest(BaseModel):
    request: str
    target: str


@router.post("/why")
def why(req: WhyRequest) -> JSONResponse:
    from kdesk.engine import Engine

    data = Engine(_state().root, catalog=_state().catalog).why(req.request, req.target)
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

    return _json(Engine(_state().root, catalog=_state().catalog).plan(req.request).to_dict())


@router.post("/run")
def run(req: RunRequest) -> JSONResponse:
    from kdesk.engine import Engine

    base = Path(req.base) if req.base else Path.cwd()
    result = Engine(_state().root, catalog=_state().catalog).run(
        req.request, base=base, auto_approve=req.auto_approve,
        timeout_s=req.timeout, dry_run=req.dry_run)
    return _json(result.to_dict())


@router.get("/history")
def history(limit: int = Query(20, ge=1, le=100)) -> JSONResponse:
    from kdesk.engine import Engine

    return _json(Engine(_state().root, catalog=_state().catalog).history(limit=limit))


@router.get("/inspect/{execution_id}")
def inspect_execution(execution_id: str) -> JSONResponse:
    from kdesk.engine import Engine

    data = Engine(_state().root, catalog=_state().catalog).inspect(execution_id)
    if data is None:
        return JSONResponse({"error": "unknown execution"}, status_code=404)
    return _json(data)


class ApproveRequest(BaseModel):
    execution_id: str
    step: int
    approve: bool = True
    note: str = ""
    by: str = "dashboard"


@router.post("/approve")
def approve(req: ApproveRequest) -> JSONResponse:
    from kdesk.engine import Engine

    updated = Engine(_state().root, catalog=_state().catalog).approve(
        req.execution_id, req.step, req.approve,
        note=req.note, decided_by=req.by)
    if updated is None:
        return JSONResponse({"error": "unknown execution"}, status_code=404)
    return _json(updated)


class ResumeRequest(BaseModel):
    execution_id: str
    base: Optional[str] = None
    auto_approve: bool = False
    timeout: float = 120.0


@router.post("/resume")
def resume(req: ResumeRequest) -> JSONResponse:
    from kdesk.engine import Engine

    base = Path(req.base) if req.base else Path.cwd()
    result = Engine(_state().root, catalog=_state().catalog).resume(
        req.execution_id, base=base,
        timeout_s=req.timeout, auto_approve=req.auto_approve)
    return _json(result.to_dict())


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
def skills_search(q: str = Query("", max_length=200),
                  limit: int = Query(20, ge=1, le=100)) -> JSONResponse:
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


class PublishRequest(BaseModel):
    skill_id: str
    force: bool = False


@router.post("/skills/publish")
def skills_publish(req: PublishRequest) -> JSONResponse:
    from kdesk.marketplace import Marketplace

    root = _state().root
    skill = _state().catalog.get_skill(req.skill_id)
    if skill is None:
        return JSONResponse({"error": f"unknown skill: {req.skill_id}"},
                            status_code=404)
    try:
        result = Marketplace(root).publish(skill.source_path, force=req.force)
    except ValueError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return _json(result)


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


@router.post("/uninstall")
def uninstall(req: InstallRequest) -> JSONResponse:
    from kdesk.adapters import AdapterRegistry
    from kdesk.installer import Installer, InstallError

    installer = Installer(AdapterRegistry(_state().root), dry_run=req.dry_run)
    try:
        result = installer.uninstall(
            req.platform, base=Path(req.base) if req.base else None)
    except InstallError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return _json(result)


@router.post("/rollback")
def rollback(req: InstallRequest) -> JSONResponse:
    from kdesk.adapters import AdapterRegistry
    from kdesk.installer import Installer, InstallError

    installer = Installer(AdapterRegistry(_state().root), dry_run=req.dry_run)
    try:
        result = installer.rollback(
            req.platform, base=Path(req.base) if req.base else None)
    except InstallError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return _json(result)


@router.get("/install-status")
def install_status() -> JSONResponse:
    from kdesk.adapters import AdapterRegistry
    from kdesk.installer import Installer

    return _json(Installer(AdapterRegistry(_state().root)).status())


# ----------------------------------------------------------------- workflows

class WorkflowAction(BaseModel):
    workflow_id: str
    execute: bool = False


@router.post("/workflows/validate")
def workflow_validate(req: WorkflowAction) -> JSONResponse:
    from kdesk.workflow import WorkflowEngine, WorkflowError

    state = _state()
    engine = WorkflowEngine(state.catalog, workflows_dir=state.root / "workflows")
    try:
        wf = engine.load(req.workflow_id)
    except WorkflowError as exc:
        return JSONResponse({"error": str(exc)}, status_code=404)
    problems = engine.validate(wf)
    return _json({"id": wf.id, "steps": len(wf.steps),
                  "problems": problems, "valid": not problems})


@router.post("/workflows/run")
def workflow_run(req: WorkflowAction) -> JSONResponse:
    from kdesk.workflow import WorkflowEngine, WorkflowError

    state = _state()
    engine = WorkflowEngine(state.catalog, workflows_dir=state.root / "workflows")
    try:
        wf = engine.load(req.workflow_id)
        result = engine.run(wf, dry_run=not req.execute)
    except WorkflowError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return _json(result)
