"""Smoke-test kdesk.mcp_server via JSON-RPC stdio."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv-clean" / "Scripts" / "python.exe"

msgs = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize",
     "params": {"clientInfo": {"name": "test"}, "protocolVersion": "2024-11-05"}},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
     "params": {"name": "get_stats", "arguments": {}}},
    {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
     "params": {"name": "search_definitions",
                "arguments": {"query": "kubernetes", "limit": 3}}},
    {"jsonrpc": "2.0", "id": 5, "method": "shutdown"},
]

proc = subprocess.Popen(
    [str(PY), "-m", "kdesk.mcp_server", "--root", str(ROOT)],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, encoding="utf-8",
)
out, err = proc.communicate("\n".join(json.dumps(m) for m in msgs) + "\n", timeout=120)

lines = [json.loads(l) for l in out.splitlines() if l.strip()]
by_id = {}
for l in lines:
    if isinstance(l.get("id"), int):
        by_id[l["id"]] = l

ok = True

r1 = by_id.get(1, {})
if r1.get("result", {}).get("serverInfo", {}).get("name") == "kdesk-catalog":
    print("[PASS] initialize -> serverInfo")
else:
    print(f"[FAIL] initialize: {r1}"); ok = False

tools = by_id.get(2, {}).get("result", {}).get("tools", [])
names = [t["name"] for t in tools]
if len(names) == 5:
    print(f"[PASS] tools/list -> {len(names)} tools: {', '.join(names)}")
else:
    print(f"[FAIL] tools/list: {names}"); ok = False

stats_text = by_id.get(3, {}).get("result", {}).get("content", [{}])[0].get("text", "")
stats = json.loads(stats_text)
if stats.get("total_definitions", 0) > 1000:
    print(f"[PASS] get_stats -> {stats['total_definitions']} defs "
          f"({stats['agents']} agents + {stats['skills']} skills)")
else:
    print(f"[FAIL] get_stats: {stats}"); ok = False

search_text = by_id.get(4, {}).get("result", {}).get("content", [{}])[0].get("text", "")
hits = json.loads(search_text)
if isinstance(hits, list) and len(hits) > 0:
    first = hits[0]
    print(f"[PASS] search 'kubernetes' -> {len(hits)} hits, top: {first['name']}")
else:
    print(f"[FAIL] search: {search_text[:200]}"); ok = False

if proc.returncode is not None:
    print(f"[INFO] exit code: {proc.returncode}")

sys.exit(0 if ok else 1)
