"""FastAPI application factory for the Kdesk dashboard."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

STATIC_DIR = Path(__file__).resolve().parent / "static"

_state = None


def get_state():
    """Return the active AppState (set by create_app)."""
    assert _state is not None, "app not initialized"
    return _state


def set_root(root) -> None:
    """Point the dashboard at a different repository root (setup flow)."""
    from kdesk.web.state import AppState

    global _state
    _state = AppState(root)


def create_app(root: Optional[Path] = None):
    from fastapi import FastAPI
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles

    from kdesk.web.routers import catalog, ops, quality
    from kdesk.web.state import AppState

    global _state
    _state = AppState(root)

    app = FastAPI(title="Kdesk Dashboard", version="1.1.0")
    app.include_router(catalog.router)
    app.include_router(quality.router)
    app.include_router(ops.router)

    @app.get("/api/health")
    def health():
        if _state.catalog_loaded:
            try:
                n = len(_state.catalog.agents) + len(_state.catalog.skills)
                return {"status": "ok", "root": str(_state.root),
                        "catalog_ok": True, "detail": f"{n} definitions loaded"}
            except Exception as exc:
                return {"status": "ok", "root": str(_state.root),
                        "catalog_ok": False, "detail": str(exc)[:300]}
        loaded, warming = _state.ensure_catalog()
        if warming:
            return {"status": "warming", "root": str(_state.root),
                    "catalog_ok": False,
                    "detail": "catalog is loading — first run takes ~1 min"}
        try:
            n = len(_state.catalog.agents) + len(_state.catalog.skills)
            return {"status": "ok", "root": str(_state.root),
                    "catalog_ok": True, "detail": f"{n} definitions loaded"}
        except Exception as exc:
            return {"status": "ok", "root": str(_state.root),
                    "catalog_ok": False, "detail": str(exc)[:300]}

    @app.post("/api/refresh")
    def refresh():
        _state.refresh()
        return {"status": "reloaded"}

    @app.post("/api/set-root")
    def set_root_ep(payload: dict):
        from fastapi.responses import JSONResponse

        path = (payload or {}).get("path", "")
        if not path:
            return JSONResponse({"error": "path is required"}, status_code=400)
        set_root(path)
        try:
            n = len(_state.catalog.agents) + len(_state.catalog.skills)
        except Exception as exc:
            return JSONResponse({"error": str(exc)[:300]}, status_code=400)
        return {"status": "ok", "root": str(_state.root),
                "definitions": n}

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

        @app.get("/")
        def index():
            return FileResponse(str(STATIC_DIR / "index.html"))

    return app


def _boot_poc(root) -> bool:
    """Beginner-friendly proof panel printed at startup (fast checks only)."""
    from pathlib import Path

    root = Path(root)
    checks = [
        ("Web pages", (STATIC_DIR / "index.html").is_file()
         and (STATIC_DIR / "app.js").is_file()
         and (STATIC_DIR / "styles.css").is_file()
         and (STATIC_DIR / "logo.svg").is_file(),
         "the dashboard you are about to open"),
        ("File uploads", _has_multipart(), "for your own agents and projects"),
        ("Catalog", (root / "universal-agents").is_dir(),
         "1,858 agents + 1,235 skills live here"),
        ("Marketplace", (root / "marketplace-registry.json").is_file(),
         "publishable skills"),
        ("Features", _route_count() >= 30, "everything clickable in the UI"),
    ]
    print("")
    print("  Kdesk is starting...")
    print("")
    ok_all = True
    for name, ok, hint in checks:
        ok_all = ok_all and ok
        mark = "ok  " if ok else "FAIL"
        print(f"  [{mark}] {name} — {hint}")
    print("")
    if not ok_all:
        return False
    print("  What now?")
    print("    1. Your browser opens by itself in a second.")
    print("    2. If it does not, copy the address below into Chrome or Edge.")
    print("    3. First screen asks your name — type it, press Enter.")
    print("    4. Click around: Catalog, Converter, Doctor. Nothing can break.")
    print("    5. To stop Kdesk, come back to this window and press Ctrl+C.")
    print("")
    return True


def _has_multipart() -> bool:
    try:
        import multipart  # noqa: F401
        return True
    except ImportError:
        return False


def _route_count() -> int:
    try:
        from kdesk.web.routers import catalog, ops, quality
        return (len(catalog.router.routes) + len(ops.router.routes)
                + len(quality.router.routes))
    except Exception:
        return 0


def _default_root() -> Path:
    from kdesk.registry import default_repo_root
    return default_repo_root()


def run(root: Optional[Path] = None, host: str = "127.0.0.1",
        port: int = 8000, open_browser: bool = True):
    """Launch the dashboard with uvicorn."""
    import threading
    import time
    import webbrowser

    try:
        import uvicorn
    except ImportError:
        print("The dashboard needs the 'web' extra: pip install -e \".[web]\"")
        raise SystemExit(2)
    if not _boot_poc(root or _default_root()):
        print("POC FAILED — fix the items above, then restart.")
        raise SystemExit(1)
    app = create_app(root)
    url = f"http://{host}:{port}"
    print(f"Kdesk dashboard at {url}")

    def _preload():
        try:
            _state.catalog  # warm the cache while the user reads onboarding
        except Exception:
            pass
    threading.Thread(target=_preload, daemon=True).start()
    if open_browser:
        def _open():
            time.sleep(1.2)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        threading.Thread(target=_open, daemon=True).start()
    uvicorn.run(app, host=host, port=port, log_level="warning")
