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
        return {"status": "ok", "root": str(_state.root)}

    @app.post("/api/refresh")
    def refresh():
        _state.refresh()
        return {"status": "reloaded"}

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

        @app.get("/")
        def index():
            return FileResponse(str(STATIC_DIR / "index.html"))

    return app


def run(root: Optional[Path] = None, host: str = "127.0.0.1", port: int = 8000):
    """Launch the dashboard with uvicorn."""
    try:
        import uvicorn
    except ImportError:
        print("The dashboard needs the 'web' extra: pip install -e \".[web]\"")
        raise SystemExit(2)
    app = create_app(root)
    print(f"Kdesk dashboard at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="warning")
