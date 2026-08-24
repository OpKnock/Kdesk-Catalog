"""MCP server exposing Kdesk-Catalog to AI agents.

Implements the Model Context Protocol (stdio transport) so any MCP-compatible
client (Claude Desktop, Cursor, etc.) can query the catalog.

Usage:
    python -m kdesk.mcp_server --root C:\\path\\to\\catalog

Protocol: JSON-RPC 2.0 over stdin/stdout, one message per line.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SERVER_NAME = "kdesk-catalog"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"

# Tools exposed via MCP
TOOLS = [
    {
        "name": "list_platforms",
        "description": "List all supported conversion platforms with their support level.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "search_definitions",
        "description": "Search agents and skills by name/description keyword.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term"},
                "type": {"type": "string", "enum": ["agent", "skill", "all"], "default": "all"},
                "limit": {"type": "integer", "default": 20},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_definition",
        "description": "Get the full definition of a single agent or skill.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Definition name"},
            },
            "required": ["id"],
        },
    },
    {
        "name": "get_compatibility",
        "description": "Get compatibility info for a definition across platforms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
            },
            "required": ["id"],
        },
    },
    {
        "name": "get_stats",
        "description": "Catalog statistics: total definitions, per-type counts, platforms.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


class CatalogIndex:
    """In-memory index of catalog definitions."""

    def __init__(self, root: Path):
        self.root = root
        self._agents: Dict[str, Dict[str, Any]] = {}
        self._skills: Dict[str, Dict[str, Any]] = {}

    CACHE_NAME = ".kdesk-mcp-cache.json"

    def _cache_path(self) -> Path:
        return self.root / self.CACHE_NAME

    def _newest_mtime(self, base: Path) -> float:
        newest = 0.0
        for p in base.rglob("*"):
            if p.suffix in (".yaml", ".yml"):
                try:
                    m = p.stat().st_mtime
                    if m > newest:
                        newest = m
                except OSError:
                    pass
        return newest

    def load(self) -> None:
        """Load definitions: fast path via JSON cache, slow path rebuild."""
        cache = self._cache_path()
        agents_base = self.root / "agents"
        skills_base = self.root / "skills"

        if not (agents_base.exists() or skills_base.exists()):
            return

        try:
            newest = max(
                self._newest_mtime(agents_base) if agents_base.exists() else 0,
                self._newest_mtime(skills_base) if skills_base.exists() else 0,
            )
            if cache.exists() and cache.stat().st_mtime >= newest:
                raw = json.loads(cache.read_text(encoding="utf-8"))
                self._agents = raw.get("agents", {})
                self._skills = raw.get("skills", {})
                if self._agents or self._skills:
                    return
        except Exception:
            pass  # fall through to rebuild

        # Rebuild from YAML
        try:
            import yaml
        except ImportError:
            raise RuntimeError("PyYAML required for MCP server")
        from concurrent.futures import ThreadPoolExecutor

        def _load_one(path: Path):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                return data if isinstance(data, dict) and data.get("name") else None
            except Exception:
                return None

        for kind, attr in (("agents", self._agents), ("skills", self._skills)):
            base = self.root / kind
            if not base.exists():
                continue
            paths = sorted(base.rglob("*.yaml")) + sorted(base.rglob("*.yml"))
            with ThreadPoolExecutor(max_workers=16) as pool:
                for data in pool.map(_load_one, paths):
                    if data:
                        attr[data["name"]] = data

        # Write cache
        try:
            cache.write_text(json.dumps({
                "agents": {k: v for k, v in list(self._agents.items())[:5000]},
                "skills": {k: v for k, v in list(self._skills.items())[:5000]},
            }, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass  # cache write failure is non-fatal

    @property
    def total(self) -> int:
        return len(self._agents) + len(self._skills)

    def search(self, query: str, def_type: str = "all",
               limit: int = 20) -> List[Dict[str, Any]]:
        q = query.lower()
        results = []
        sources = []
        if def_type in ("all", "agent"):
            sources.extend(("agent", d) for d in self._agents.values())
        if def_type in ("all", "skill"):
            sources.extend(("skill", d) for d in self._skills.values())
        for kind, d in sources:
            name = str(d.get("name", ""))
            desc = str(d.get("description", ""))
            tags = " ".join(d.get("tags", []) or [])
            hay = f"{name} {desc} {tags}".lower()
            if q in hay:
                results.append({
                    "type": kind,
                    "name": d.get("name"),
                    "description": (desc or "")[:200],
                    "division": d.get("division"),
                    "platforms": d.get("platforms"),
                })
                if len(results) >= limit:
                    break
        return results

    def get(self, def_id: str) -> Optional[Dict[str, Any]]:
        if def_id in self._agents:
            d = dict(self._agents[def_id])
            d["_type"] = "agent"
            return d
        if def_id in self._skills:
            d = dict(self._skills[def_id])
            d["_type"] = "skill"
            return d
        return None


class MCPServer:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.index = CatalogIndex(self.root)
        self._running = True

    # ---- JSON-RPC plumbing -------------------------------------------------

    def _send(self, payload: Dict[str, Any]) -> None:
        sys.stdout.write(json.dumps(payload) + "\n")
        sys.stdout.flush()

    def _result(self, req_id: Any, result: Any) -> None:
        self._send({"jsonrpc": "2.0", "id": req_id, "result": result})

    def _error(self, req_id: Any, code: int, message: str) -> None:
        self._send({"jsonrpc": "2.0", "id": req_id,
                    "error": {"code": code, "message": message}})

    # ---- Tool handlers -----------------------------------------------------

    def _tool_list_platforms(self, _: Dict[str, Any]) -> Dict[str, Any]:
        from kdesk.platforms import get_registry
        reg = get_registry()
        platforms = [
            {"id": p.id, "name": p.display_name,
             "support": p.support_level.value if hasattr(p.support_level, "value") else str(p.support_level)}
            for p in reg.all()
        ]
        return {"content": [{"type": "text", "text": json.dumps(platforms, indent=2)}]}

    def _tool_search_definitions(self, args: Dict[str, Any]) -> Dict[str, Any]:
        query = args.get("query", "")
        dtype = args.get("type", "all")
        limit = int(args.get("limit", 20))
        hits = self.index.search(query, dtype, limit)
        return {"content": [{"type": "text", "text": json.dumps(hits, indent=2)}]}

    def _tool_get_definition(self, args: Dict[str, Any]) -> Dict[str, Any]:
        d = self.index.get(args.get("id", ""))
        if not d:
            raise KeyError(f"definition '{args.get('id')}' not found")
        return {"content": [{"type": "text", "text": json.dumps(d, indent=2)}]}

    def _tool_get_compatibility(self, args: Dict[str, Any]) -> Dict[str, Any]:
        d = self.index.get(args.get("id", ""))
        if not d:
            raise KeyError(f"definition '{args.get('id')}' not found")
        compat = d.get("platforms") or {}
        return {"content": [{"type": "text", "text": json.dumps(compat, indent=2)}]}

    def _tool_get_stats(self, _: Dict[str, Any]) -> Dict[str, Any]:
        stats = {
            "total_definitions": self.index.total,
            "agents": len(self.index._agents),
            "skills": len(self.index._skills),
            "root": str(self.root),
        }
        return {"content": [{"type": "text", "text": json.dumps(stats, indent=2)}]}

    # ---- Request dispatch --------------------------------------------------

    def _handle_request(self, msg: Dict[str, Any]) -> None:
        method = msg.get("method", "")
        req_id = msg.get("id")

        if method == "initialize":
            self._result(req_id, {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            })
        elif method == "notifications/initialized":
            pass  # notification, no response
        elif method == "ping":
            self._result(req_id, {})
        elif method == "tools/list":
            self._result(req_id, {"tools": TOOLS})
        elif method == "tools/call":
            params = msg.get("params", {})
            tool = params.get("name", "")
            handler = getattr(self, f"_tool_{tool}", None)
            if not callable(handler):
                self._error(req_id, -32601, f"Unknown tool: {tool}")
                return
            try:
                self._result(req_id, handler(params.get("arguments", {})))
            except KeyError as e:
                self._error(req_id, -32602, str(e))
            except Exception as e:
                self._error(req_id, -32603, f"Internal error: {e}")
        elif method == "shutdown":
            self._result(req_id, {})
            self._running = False
        else:
            if req_id is not None:
                self._error(req_id, -32601, f"Method not found: {method}")

    # ---- Main loop ---------------------------------------------------------

    def serve(self) -> None:
        self.index.load()
        for line in sys.stdin:
            if not self._running:
                break
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                self._error(None, -32700, "Parse error")
                continue
            self._handle_request(msg)


def main() -> None:
    parser = argparse.ArgumentParser(description="Kdesk-Catalog MCP server")
    parser.add_argument("--root", default=str(Path.cwd()),
                        help="Path to Kdesk-Catalog repository root")
    ns = parser.parse_args()

    root = Path(ns.root).resolve()
    if not (root / "agents").exists():
        print(f"error: no 'agents/' dir under {root}", file=sys.stderr)
        sys.exit(1)

    server = MCPServer(root)
    server.serve()


if __name__ == "__main__":
    main()
