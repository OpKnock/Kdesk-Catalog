"""Interactive MCP test: send one message, read one response."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv-clean" / "Scripts" / "python.exe"

proc = subprocess.Popen(
    [str(PY), "-u", "-m", "kdesk.mcp_server", "--root", str(ROOT)],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, encoding="utf-8", bufsize=0,
)

def send(msg):
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()

def recv():
    line = proc.stdout.readline()
    return json.loads(line) if line.strip() else None

send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      "params": {"clientInfo": {"name": "t"}, "protocolVersion": "2024-11-05"}})
print("initialize ->", json.dumps(recv())[:200])

send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
r = recv()
print(f"tools/list -> {len(r['result']['tools'])} tools")

send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
      "params": {"name": "get_stats"}})
r = recv()
text = r["result"]["content"][0]["text"]
stats = json.loads(text)
print(f"get_stats -> total={stats.get('total_definitions')}, "
      f"agents={stats.get('agents')}, skills={stats.get('skills')}")

proc.terminate()
