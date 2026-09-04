"""kdesk.web — local premium dashboard (FastAPI + static SPA).

Run with:  kdesk serve [--port 8000]
Requires the 'web' extra:  pip install -e ".[web]"
"""
from kdesk.web.app import create_app, get_state, run

__all__ = ["create_app", "get_state", "run"]
