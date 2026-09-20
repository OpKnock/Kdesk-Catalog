"""Quality-gate endpoints: verify, policy, security, audits, schema."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from kdesk.duplicates import DuplicateDetector, DuplicatePolicy
from kdesk.license import LicenseAudit, LicensePolicy
from kdesk.policy import PolicyEngineV2
from kdesk.provenance import Provenance, verify_wiring
from kdesk.quality import QualityReport
from kdesk.security import scan_repo
from kdesk.verify import run_verify

router = APIRouter(prefix="/api", tags=["quality"])


def _json(data: Any) -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(data, default=str)))


def _state():
    from kdesk.web.app import get_state
    return get_state()


@router.get("/verify")
def verify(fast: bool = True, skip: Optional[str] = None) -> JSONResponse:
    state = _state()
    summary = run_verify(state.root, fast=fast, skip=skip)
    return _json(summary)


@router.get("/policy")
def policy() -> JSONResponse:
    state = _state()
    result = PolicyEngineV2().evaluate(state.catalog)
    return _json(result)


@router.get("/security")
def security() -> JSONResponse:
    state = _state()
    report = scan_repo(state.root, state.root / "reports" / "security-exceptions.json")
    return _json(report)


@router.get("/quality")
def quality() -> JSONResponse:
    state = _state()
    return _json(QualityReport(state.catalog).score())


@router.get("/duplicates")
def duplicates() -> JSONResponse:
    state = _state()
    pol = DuplicatePolicy.load(state.root / "reports" / "duplicate-classifications.json")
    return _json(DuplicateDetector(state.catalog).detect(policy=pol))


@router.get("/license")
def license_audit() -> JSONResponse:
    state = _state()
    pol = LicensePolicy.load(state.root / "reports" / "license-policy.json")
    return _json(LicenseAudit(state.catalog).audit(policy=pol))


@router.get("/provenance")
def provenance() -> JSONResponse:
    state = _state()
    return _json(Provenance(state.root).verify())


@router.get("/wiring")
def wiring() -> JSONResponse:
    state = _state()
    return _json(verify_wiring(state.root))


@router.get("/schema")
def schema() -> JSONResponse:
    import subprocess

    state = _state()
    proc = subprocess.run(
        [sys.executable, "scripts/schema-check.py"],
        capture_output=True, text=True, cwd=str(state.root),
        timeout=600, encoding="utf-8", errors="replace")
    return _json({"exit_code": proc.returncode,
                  "output": (proc.stdout or "")[-4000:]})
