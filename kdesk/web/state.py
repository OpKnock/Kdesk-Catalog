"""Shared server state: single Catalog load reused across requests."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from kdesk.registry import Catalog, default_repo_root


class AppState:
    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root) if root else default_repo_root()
        self._catalog: Optional[Catalog] = None

    @property
    def catalog(self) -> Catalog:
        if self._catalog is None:
            self._catalog = Catalog.from_repo(self.root)
        return self._catalog

    def refresh(self) -> Catalog:
        self._catalog = Catalog.from_repo(self.root)
        return self._catalog
