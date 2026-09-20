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


def get(path, timeout=120):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=timeout) as r:
        return r.status, r.read().decode("utf-8")


def post(path, body, timeout=240):
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, json.loads(r.read().decode("utf-8"))


def post_status(path, body, timeout=120):
    """POST returning (status, body-or-error) without raising on 4xx."""
    import urllib.error
    try:
        return post(path, body, timeout)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")[:200]


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
    # Warm-up: first catalog load on cold Windows FS can take minutes.
    # Real browsers wait; so do we (generous one-time budget).
    check("warmup-catalog", lambda: f"ok={json.loads(get('/api/health', timeout=300)[1])['catalog_ok']}")
    check("stats", lambda: f"defs={json.loads(get('/api/stats?fast=true')[1])['definitions_total']}")
    check("search", lambda: f"hits={len(json.loads(get('/api/search?q=kubernetes')[1]))}")
    check("policy", lambda: f"rules={json.loads(get('/api/policy')[1])['total_rules']}")
    check("skills", lambda: f"skills={json.loads(get('/api/skills')[1])['stats']['unique_skills']}")
    check("resolve", lambda: f"cands={len(post('/api/resolve', {'request': 'lint terraform'})[1]['candidates'])}")
    check("definition", lambda: f"{json.loads(get('/api/definition/skill/kubernetes')[1])['name']}")
    check("health-catalog", lambda: f"ok={json.loads(get('/api/health')[1])['catalog_ok']}")
    check("publish-unknown", lambda: f"st={post_status('/api/skills/publish', {'skill_id': 'nope-not-real'})[0]} (want 404)")
    check("approve-unknown", lambda: f"st={post_status('/api/approve', {'execution_id': 'zzz', 'step': 0})[0]} (want 404)")
    check("uninstall-dryrun", lambda: f"st={post_status('/api/uninstall', {'platform': 'cursor', 'dry_run': True})[0]} (want 400 not-installed)")
    check("install-status", lambda: f"keys={sorted(json.loads(get('/api/install-status')[1]).keys())}")
    check("wf-validate-unknown", lambda: f"st={post_status('/api/workflows/validate', {'workflow_id': 'nope'})[0]} (want 404)")
    check("delegate-plain", lambda: f"delegated={post('/api/delegate?agent=auto-scaling-engineer', {})[1]['delegated']}")
    check("resolve-version", lambda: f"{json.loads(get('/api/resolve-version?spec=terraform-infrastructure@%5E1.0')[1])['resolved']}")
    check("telemetry", lambda: f"total={json.loads(get('/api/telemetry')[1])['total']}")
    check("history", lambda: f"entries={len(json.loads(get('/api/history?limit=3')[1]))}")
    check("set-root-bad", lambda: f"st={post_status('/api/set-root', {'path': 'C:/definitely/not/here'})[0]} (want 400)")
    check("set-root-restore", lambda: f"defs={post('/api/set-root', {'path': str(ROOT)}, timeout=300)[1]['definitions']}")
    check("categories", lambda: f"agent-cats={len(json.loads(get('/api/categories')[1])['agent'])}")
    check("official", lambda: f"total={json.loads(get('/api/official')[1])['total']}")
    check("official-file", lambda: f"{json.loads(get('/api/official/file?path=' + json.loads(get('/api/official')[1])['items'][0]['path'].replace('agents/', ''))[1])['path']}")
    check("browse", lambda: f"total={json.loads(get('/api/browse?type=skill&category=api&limit=5')[1])['total']}")
    check("browse-q", lambda: f"hits={json.loads(get('/api/browse?q=kubernetes&limit=5')[1])['total']}")

    # upload: tiny synthetic agent yaml, multipart
    import urllib.error
    boundary = "----kdesktest1234"
    yaml_body = ("name: e2e-probe-agent\ndisplay_name: E2E Probe\ncategory: testing\n"
                 "description: probe agent for e2e upload test\nversion: 1.0.0\n"
                 "instructions: do nothing\n")
    mp = ("\r\n".join([
        f"--{boundary}",
        'Content-Disposition: form-data; name="files"; filename="probe-agent.yaml"',
        "Content-Type: text/yaml", "",
        yaml_body,
        f"--{boundary}",
        'Content-Disposition: form-data; name="platforms"', "",
        "cursor,claude_code",
        f"--{boundary}--", ""]) + "\r\n")

    def upload_convert():
        req = urllib.request.Request(
            f"http://127.0.0.1:{PORT}/api/convert-upload", data=mp.encode(),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST")
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8"))
        arts = [a for a in d["artifacts"] if not a.get("error")]
        return f"artifacts={len(arts)}/{len(d['artifacts'])}"
    check("convert-upload", upload_convert)
    check("convert-selected", lambda: f"arts={len(post('/api/convert-selected', {'names': ['kubernetes', 'terraform-infrastructure'], 'platforms': ['cursor', 'claude_code']})[1]['artifacts'])}")
    check("convert-file", lambda: f"{get('/api/convert/file?platform=cursor&path=kubernetes.mdc'.replace(' ', '%20'))[0]}")

    def upload_doctor():
        req = urllib.request.Request(
            f"http://127.0.0.1:{PORT}/api/doctor-upload", data=mp.replace(
                'name="platforms"', 'name="FAKE"').encode(),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST")
        # rebuild with proper doctor fields
        mp2 = ("\r\n".join([
            f"--{boundary}",
            'Content-Disposition: form-data; name="files"; filename="AGENTS.md"',
            "Content-Type: text/markdown", "",
            "# rules\nBe kind.\n",
            f"--{boundary}",
            'Content-Disposition: form-data; name="platform"',
            "", "generic",
            f"--{boundary}",
            'Content-Disposition: form-data; name="mode"',
            "", "diagnose",
            f"--{boundary}--", ""]) + "\r\n")
        req2 = urllib.request.Request(
            f"http://127.0.0.1:{PORT}/api/doctor-upload", data=mp2.encode(),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST")
        with urllib.request.urlopen(req2, timeout=180) as r:
            d = json.loads(r.read().decode("utf-8"))
        rep = d.get("report", d)
        return f"score={rep.get('score')}% issues={len(rep.get('issues', []))}"
    check("doctor-upload", upload_doctor)
finally:
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except Exception:
        proc.kill()

sys.exit(0 if ok else 1)
