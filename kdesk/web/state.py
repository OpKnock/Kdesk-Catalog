"""Shared server state: single Catalog load reused across requests."""
from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from kdesk.registry import Catalog, default_repo_root

STATS_TTL_S = 120.0


class AppState:
    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root) if root else default_repo_root()
        self._catalog: Optional[Catalog] = None
        self._stats_cache: Dict[bool, Tuple[float, Dict[str, Any]]] = {}
        # Guards lazy loads: without this, N concurrent first-requests
        # each trigger a full 3093-file parse (thundering herd).
        self._lock = threading.Lock()

    @property
    def catalog(self) -> Catalog:
        if self._catalog is None:
            with self._lock:
                if self._catalog is None:
                    self._catalog = Catalog.from_repo(self.root)
        return self._catalog

    @property
    def catalog_loaded(self) -> bool:
        return self._catalog is not None

    def ensure_catalog(self):
        """Load the catalog unless another thread already is.

        Returns (loaded: bool, warming: bool). Never blocks on another
        loader — callers seeing warming=True should retry shortly.
        """
        if self._catalog is not None:
            return True, False
        if not self._lock.acquire(blocking=False):
            return False, True
        try:
            if self._catalog is None:
                self._catalog = Catalog.from_repo(self.root)
            return True, False
        finally:
            self._lock.release()

    def refresh(self) -> Catalog:
        with self._lock:
            self._catalog = Catalog.from_repo(self.root)
            self._stats_cache.clear()
            return self._catalog

    def stats(self, fast: bool = True):
        """Cached compute_stats; refresh() or TTL expiry invalidates."""
        from kdesk.stats import compute as compute_stats

        now = time.monotonic()
        hit = self._stats_cache.get(fast)
        if hit and now - hit[0] < STATS_TTL_S:
            return hit[1]
        with self._lock:
            hit = self._stats_cache.get(fast)
            if hit and time.monotonic() - hit[0] < STATS_TTL_S:
                return hit[1]
            payload = compute_stats(self.root, fast=fast, catalog=self.catalog)
            self._stats_cache[fast] = (time.monotonic(), payload)
            return payload
