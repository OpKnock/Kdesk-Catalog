#!/usr/bin/env python3
"""Kdesk Judges PoC — scripted end-to-end proof run.

Boots `kdesk serve`, walks the whole product through its own API
(catalog -> convert with live proof -> doctor diagnose -> marketplace
-> install dry-run), and writes human + machine proof artifacts:

    poc-proof/PROOF.md    human-readable proof transcript
    poc-proof/proof.json  machine-readable results
    poc-proof/artifacts/  real generated files from the run

Usage:
    python scripts/poc-judges.py [--port 8135] [--keep-server]

Exit code 0 only if every proof step passes.
"""
import argparse
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv-clean" / "Scripts" / "python.exe"
if not PY.is_file():
    PY = Path(sys.executable)

STEPS = []


def step(name):
    def deco(fn):
        STEPS.append((name, fn))
        return fn
    return deco


class Ctx:
    def __init__(self, base):
        self.base = base
        self.data = {}

    def get(self, path, timeout=180):
        with urllib.request.urlopen(self.base + path, timeout=timeout) as r:
            assert r.status == 200, f"{path} -> {r.status}"
            return json.loads(r.read().decode("utf-8"))

    def post(self, path, body, timeout=300):
        req = urllib.request.Request(
            self.base + path, data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            assert r.status == 200, f"{path} -> {r.status}"
            return json.loads(r.read().decode("utf-8"))


@step("server boot + health")
def s_health(ctx):
    h = ctx.get("/api/health", timeout=300)
    assert h["catalog_ok"], f"catalog not ok: {h}"
    return f"catalog ready: {h['detail']}"


@step("catalog stats (1,858 agents + 1,235 skills)")
def s_stats(ctx):
    s = ctx.get("/api/stats?fast=true")
    assert s["agents"] == 1858, s
    assert s["skills"] == 1235, s
    return f"{s['agents']} agents, {s['skills']} skills, {s['platforms']} platforms"


@step("catalog browse + categories")
def s_browse(ctx):
    cats = ctx.get("/api/categories")
    assert len(cats["agent"]) == 36, cats
    page = ctx.get("/api/browse?type=skill&category=api&limit=5")
    assert page["total"] > 400, page
    return f"36 agent cats, {len(cats['skill'])} skill cats; api skills: {page['total']}"


@step("official implementations listed")
def s_official(ctx):
    o = ctx.get("/api/official")
    assert o["total"] >= 4, o
    names = sorted(i["name"] for i in o["items"])
    return f"{o['total']} runnable: {', '.join(names)}"


@step("convert selected with live proof")
def s_convert(ctx):
    d = ctx.post("/api/convert-selected",
                 {"names": ["kubernetes", "terraform-infrastructure"],
                  "platforms": ["cursor", "claude_code"]})
    arts = [a for a in d["artifacts"] if not a.get("error")]
    assert len(arts) == 4, d
    ctx.data["artifacts"] = arts
    paths = sorted(f"{a['platform']}/{a['path']}" for a in arts)
    return f"4 artifacts: {', '.join(paths)}"


@step("doctor diagnose with evidence")
def s_doctor(ctx):
    d = ctx.post("/api/doctor",
                 {"platform": "cursor", "mode": "diagnose",
                  "project_root": None, "dry_run": True}, timeout=400)
    rep = d.get("report", d)
    assert "score" in rep and "issues" in rep, rep
    return f"score={rep['score']}% issues={len(rep['issues'])}"


@step("marketplace resolve + version")
def s_market(ctx):
    e = ctx.post("/api/skills/install?spec=terraform-infrastructure", {})
    assert e["status"] == "resolved", e
    v = ctx.get("/api/resolve-version?spec=terraform-infrastructure@%5E1.0")
    assert v["resolved"] == "terraform-infrastructure@1.0.0", v
    return f"skill {e['name']}@{e['version']}; semver {v['resolved']}"


@step("install dry-run (writes nothing)")
def s_install(ctx):
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        r = ctx.post("/api/install",
                     {"platform": "cursor", "base": tmp, "dry_run": True})
    assert r["results"][0]["status"] == "DRY-RUN", r
    return f"dry-run ok, {r['results'][0]['copied']} files would copy"


def main() -> int:
    ap = argparse.ArgumentParser(description="Kdesk judges PoC run")
    ap.add_argument("--port", type=int, default=8135)
    ap.add_argument("--keep-server", action="store_true")
    ns = ap.parse_args()

    out = ROOT / "poc-proof"
    (out / "artifacts").mkdir(parents=True, exist_ok=True)

    proc = subprocess.Popen(
        [str(PY), "-m", "kdesk.cli", "serve", "--port", str(ns.port),
         "--no-browser"],
        cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ctx = Ctx(f"http://127.0.0.1:{ns.port}")
    results = []
    try:
        # wait for boot (generous: cold parse can take minutes)
        t0 = time.time()
        while time.time() - t0 < 600:
            try:
                ctx.get("/api/health", timeout=10)
                break
            except Exception:
                time.sleep(3)
        print("== Kdesk PoC: proof run ==")
        ok_all = True
        for name, fn in STEPS:
            t0 = time.time()
            try:
                detail = fn(ctx)
                dt = time.time() - t0
                print(f"  [PASS] {name} ({dt:.1f}s)\n         {detail}")
                results.append({"step": name, "status": "PASS",
                                "seconds": round(dt, 1), "detail": detail})
            except Exception as exc:
                dt = time.time() - t0
                print(f"  [FAIL] {name}: {exc}")
                results.append({"step": name, "status": "FAIL",
                                "seconds": round(dt, 1), "detail": str(exc)[:300]})
                ok_all = False
        # artifacts to disk
        for a in ctx.data.get("artifacts", []):
            fname = f"{a['platform']}__{a['path'].replace('/', '__')}"
            (out / "artifacts" / fname).write_text(a["content"], encoding="utf-8")
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        md = [f"# Kdesk — Proof of Capability", "",
              f"_Generated {stamp} by `scripts/poc-judges.py`_",
              f"_Catalog: 1,858 agents + 1,235 skills across 45 platforms_", ""]
        for r in results:
            mark = "✅" if r["status"] == "PASS" else "❌"
            md += [f"## {mark} {r['step']} ({r['seconds']}s)", "", f"{r['detail']}", ""]
        md += ["## Artifacts", "",
               "Real converter output from this run lives in `poc-proof/artifacts/` —",
               "open any file to see source definition turned into platform-native format.", ""]
        (out / "PROOF.md").write_text("\n".join(md), encoding="utf-8")
        (out / "proof.json").write_text(
            json.dumps({"generated_at": stamp, "results": results}, indent=2),
            encoding="utf-8")
        print(f"\nproof written to poc-proof/ ({len(results)} steps, "
              f"{sum(1 for r in results if r['status']=='PASS')} passed)")
        return 0 if ok_all else 1
    finally:
        if ns.keep_server:
            print(f"server left running on port {ns.port}")
        else:
            proc.terminate()
            try:
                proc.wait(timeout=15)
            except Exception:
                proc.kill()


if __name__ == "__main__":
    sys.exit(main())
