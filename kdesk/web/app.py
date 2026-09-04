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
        try:
            n = len(_state.catalog.agents) + len(_state.catalog.skills)
            ok, detail = True, f"{n} definitions loaded"
        except Exception as exc:
            ok, detail = False, str(exc)[:300]
        return {"status": "ok", "root": str(_state.root),
                "catalog_ok": ok, "detail": detail}

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
    app = create_app(root)
    url = f"http://{host}:{port}"
    print(f"Kdesk dashboard at {url}")
    if open_browser:
        def _open():
            time.sleep(1.2)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        threading.Thread(target=_open, daemon=True).start()
    uvicorn.run(app, host=host, port=port, log_level="warning")
