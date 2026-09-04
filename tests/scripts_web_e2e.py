"""End-to-end dashboard test: boot server, hit endpoints, shut down."""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv-clean" / "Scripts" / "python.exe"
PORT = 8125


def get(path, timeout=60):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=timeout) as r:
        return r.status, r.read().decode("utf-8")


def post(path, body, timeout=120):
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, json.loads(r.read().decode("utf-8"))


proc = subprocess.Popen(
    [str(PY), "-m", "kdesk.cli", "serve", "--port", str(PORT)],
    cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

ok = True
try:
    for _ in range(40):
        time.sleep(3)
        try:
            st, _ = get("/api/health", timeout=5)
            if st == 200:
                break
        except Exception:
            pass
    else:
        print("[FAIL] server did not start"); ok = False

    def check(name, fn):
        global ok
        try:
            out = fn()
            print(f"[PASS] {name} -> {out}")
        except Exception as e:
            ok = False
            print(f"[FAIL] {name}: {e}")

    check("index.html", lambda: f"{get('/')[0]} len={len(get('/')[1])}")
    check("styles.css", lambda: f"{get('/static/styles.css')[0]}")
    check("app.js", lambda: f"{get('/static/app.js')[0]}")
    check("stats", lambda: f"defs={json.loads(get('/api/stats?fast=true')[1])['definitions_total']}")
    check("search", lambda: f"hits={len(json.loads(get('/api/search?q=kubernetes')[1]))}")
    check("policy", lambda: f"rules={json.loads(get('/api/policy')[1])['total_rules']}")
    check("skills", lambda: f"skills={json.loads(get('/api/skills')[1])['stats']['unique_skills']}")
    check("resolve", lambda: f"cands={len(post('/api/resolve', {'request': 'lint terraform'})[1]['candidates'])}")
    check("definition", lambda: f"{json.loads(get('/api/definition/skill/kubernetes')[1])['name']}")
finally:
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except Exception:
        proc.kill()

sys.exit(0 if ok else 1)
