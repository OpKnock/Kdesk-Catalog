#!/usr/bin/env python3
"""Universal live-agent runner: any catalog definition, one entry point.

Every catalog YAML (all 3094 agents/skills) is already a runnable agent:
this script materializes it as a live framework Agent and runs it.

Usage:
  python scripts/live_agent.py run <name> ["task"] [--execute] [--allow-shell]
  python scripts/live_agent.py team <root-agent> ["task"] [--execute]
  python scripts/live_agent.py prompts --out live-tests/prompts.json
  python scripts/live_agent.py test-all [--prompts live-tests/prompts.json]
                         [--out reports/live-prompt-test.json] [--live]

- `run` without --execute prints the dry-run plan (no network, no creds).
- `run --execute` calls the model (needs OPENAI_API_KEY or Foundry config).
- `test-all` runs EVERY definition with its own test prompt through the
  full offline loop (Read definition -> Reason route capability ->
  Act invoke the agent's real tools). With --live it additionally calls
  the model once per definition (needs valid credentials; slow + billed).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kdesk import agent_runtime as ar  # noqa: E402
from kdesk.registry import Catalog  # noqa: E402


def cmd_run(args) -> int:
    catalog = Catalog.from_repo(ROOT)
    try:
        if not args.execute:
            out = ar.run_agent(catalog, args.name, args.task or "", dry_run=True)
            print(json.dumps(out, indent=2, default=str)[:4000])
            return 0
        out = ar.run_agent(
            catalog, args.name, args.task or "", dry_run=False,
            allow_shell=args.allow_shell,
        )
        print(out if isinstance(out, str) else json.dumps(out, indent=2, default=str))
        return 0
    except ar.AgentRuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_team(args) -> int:
    catalog = Catalog.from_repo(ROOT)
    try:
        if not args.execute:
            from kdesk.delegation import SubAgentResolver
            plan = SubAgentResolver(catalog).plan(args.name)
            if plan is None:
                print(f"No delegation plan for: {args.name}")
                return 1
            print(json.dumps(plan.summary(), indent=2, default=str))
            return 0
        out = asyncio.run(ar.run_team(catalog, args.name, args.task or ""))
        print(json.dumps(out, indent=2, default=str)[:6000])
        return 0
    except ar.AgentRuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_prompts(args) -> int:
    catalog = Catalog.from_repo(ROOT)
    prompts = {}
    for store in (catalog.agents, catalog.skills):
        for name, defn in store.items():
            prompts[name] = ar.make_test_prompt(defn)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(prompts, indent=1), encoding="utf-8")
    print(f"Wrote {len(prompts)} test prompts -> {out}")
    return 0


def _test_one(catalog, kind, name, defn, prompt, live: bool) -> dict:
    """Full per-agent test: Read -> Reason -> Act (+ live model when asked)."""
    started = time.time()
    evidence: dict = {"name": name, "type": kind}
    try:
        # READ: instructions compose from the definition itself.
        instructions = ar.build_instructions(defn)
        assert "Read -> Reason -> Act" in instructions
        evidence["instructions_chars"] = len(instructions)
        # REASON: route the prompt to the agent's own capability.
        cap = ar.route_capability(defn, prompt)
        evidence["routed_capability"] = cap.name if cap else None
        # ACT: build the real framework Agent + invoke its real tools.
        tools = ar.build_tools(defn, catalog)
        evidence["framework_tools"] = len(tools)

        class _Stub:
            pass

        agent = ar.build_agent(defn, _Stub(), catalog)
        evidence["framework_agent"] = getattr(agent, "name", "?")
        impls = ar.safe_tool_impls(defn, catalog)
        keyword = (cap.name if cap else defn.category).replace("-", " ")
        search_out = impls["catalog_search"](keyword.split()[0] if keyword else defn.category)
        evidence["tool_catalog_search_hits"] = search_out.count("\n") + 1 if search_out != "No matches." else 0
        evidence["tool_describe_ok"] = defn.name in impls["describe_definition"](defn.name)
        evidence["tool_commands_lines"] = impls["capability_commands"](defn.name).count("\n") + 1
        if live:
            text = asyncio.run(ar.run_live(defn, prompt, catalog))
            evidence["live_chars"] = len(text)
            evidence["live_head"] = text[:200]
        evidence["status"] = "PASS"
    except Exception as exc:  # noqa: BLE001 - per-agent record, never abort the sweep
        evidence["status"] = "FAIL"
        evidence["error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
    evidence["seconds"] = round(time.time() - started, 2)
    return evidence


def cmd_test_all(args) -> int:
    catalog = Catalog.from_repo(ROOT)
    if args.prompts and Path(args.prompts).exists():
        prompts = json.loads(Path(args.prompts).read_text(encoding="utf-8"))
    else:
        prompts = {}
    items = ([("agent", n, o) for n, o in catalog.agents.items()]
             + [("skill", n, o) for n, o in catalog.skills.items()])
    results = []
    npass = nfail = 0
    t0 = time.time()
    for i, (kind, name, defn) in enumerate(items, 1):
        prompt = prompts.get(name) or ar.make_test_prompt(defn)
        rec = _test_one(catalog, kind, name, defn, prompt, live=args.live)
        results.append(rec)
        if rec["status"] == "PASS":
            npass += 1
        else:
            nfail += 1
        if i % 500 == 0:
            print(f"... {i}/{len(items)} pass={npass} fail={nfail} "
                  f"t={time.time() - t0:.0f}s", flush=True)
    summary = {
        "total": len(results),
        "pass": npass,
        "fail": nfail,
        "live_model_calls": args.live,
        "seconds": round(time.time() - t0, 1),
        "failures": [r for r in results if r["status"] == "FAIL"][:30],
        "results": results,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"DONE total={len(results)} pass={npass} fail={nfail} "
          f"t={summary['seconds']}s -> {out}")
    return 0 if nfail == 0 else 3


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="live_agent", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("run", help="run one agent/skill")
    r.add_argument("name")
    r.add_argument("task", nargs="?", default="")
    r.add_argument("--execute", action="store_true")
    r.add_argument("--allow-shell", action="store_true")
    r.set_defaults(func=cmd_run)

    t = sub.add_parser("team", help="run a root agent + sub-agents")
    t.add_argument("name")
    t.add_argument("task", nargs="?", default="")
    t.add_argument("--execute", action="store_true")
    t.set_defaults(func=cmd_team)

    pr = sub.add_parser("prompts", help="generate test prompts for all defs")
    pr.add_argument("--out", default="live-tests/prompts.json")
    pr.set_defaults(func=cmd_prompts)

    ta = sub.add_parser("test-all", help="test every definition with its prompt")
    ta.add_argument("--prompts", default="live-tests/prompts.json")
    ta.add_argument("--out", default="reports/live-prompt-test.json")
    ta.add_argument("--live", action="store_true",
                    help="also call the model per definition (billed)")
    ta.set_defaults(func=cmd_test_all)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
