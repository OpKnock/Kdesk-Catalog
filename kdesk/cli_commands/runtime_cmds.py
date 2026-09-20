"""Runtime commands: engine resolve/plan/run, skill marketplace, delegation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from kdesk.delegation import SubAgentResolver
from kdesk.engine import (STATUS_BLOCKED, STATUS_CANCELLED, STATUS_FAILED,
                          STATUS_TIMEOUT, STATUS_WAITING_APPROVAL, Engine)
from kdesk.marketplace import Marketplace
from kdesk.registry import Catalog, default_repo_root
from kdesk.telemetry import summary as telemetry_summary
from kdesk.versioning import VersionResolver, build_available_versions

from kdesk.cli_commands.helpers import _catalog


def _cmd_resolve(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    result = engine.resolve(args.request, top=args.top,
                            probe_environment=not args.no_env_probe)
    data = result.to_dict()
    if not args.json:
        print(f"intent: {data.get('intent', {}).get('intent', 'unknown')}")
        for i, cand in enumerate(data.get("candidates", []), 1):
            print(f"  {i}. {cand.get('name')} [{cand.get('definition_type')}] "
                  f"score={cand.get('score')} risk={cand.get('risk')}")
        if data.get("missing_requirements"):
            print("missing requirements:")
            for name, info in data["missing_requirements"].items():
                print(f"  - {name}: {info}")
    else:
        print(json.dumps(data, indent=2, default=str))
    return 0 if data.get("candidates") else 3


def _cmd_why(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    data = engine.why(args.request, args.target)
    if data is None:
        print(f"UNKNOWN target: {args.target}")
        return 1
    print(json.dumps(data, indent=2, default=str))
    return 0


def _cmd_plan(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    plan = engine.plan(args.request)
    data = plan.to_dict()
    if not args.json:
        print(f"steps: {len(data.get('steps', []))}")
        for step in data.get("steps", []):
            decision = step.get("decision", "allowed")
            print(f"  {step.get('index')}. [{decision}] {step.get('description')}")
    else:
        print(json.dumps(data, indent=2, default=str))
    return 0


def _cmd_run(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    base = Path(args.base) if args.base else Path.cwd()
    if args.execution_id:
        existing = engine.inspect(args.execution_id)
        if existing is not None and existing["execution"]["status"] == STATUS_WAITING_APPROVAL:
            step = int(existing["execution"].get("approval_step", -1))
            approvals = [a for a in existing["approvals"] if a.get("step") == step]
            if any(a.get("state") in ("approved", "auto_approved") for a in approvals):
                result = engine.resume(args.execution_id, base=base,
                                       timeout_s=args.timeout,
                                       auto_approve=args.auto_approve)
            else:
                state = approvals[-1]["state"] if approvals else "pending"
                print(f"execution {args.execution_id} is waiting at step {step} "
                      f"(state={state}); approve it first", file=sys.stderr)
                return 3
        else:
            result = engine.run(args.request, base=base,
                                auto_approve=args.auto_approve,
                                timeout_s=args.timeout,
                                execution_id=args.execution_id)
    else:
        result = engine.run(args.request, base=base,
                            auto_approve=args.auto_approve,
                            timeout_s=args.timeout,
                            execution_id=args.execution_id,
                            dry_run=args.dry_run)
    data = result.to_dict()
    if not args.json:
        print(f"execution: {data['execution_id']} status={data['status']} "
              f"steps={len(data.get('steps', []))} artifacts={len(data.get('artifacts', []))}")
        if data.get("error"):
            print(f"error: {data['error']}")
    else:
        print(json.dumps(data, indent=2, default=str))
    if data["status"] == STATUS_BLOCKED:
        return 3
    if data["status"] in (STATUS_FAILED, STATUS_TIMEOUT, STATUS_CANCELLED):
        return 1
    return 0


def _cmd_history(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    print(json.dumps(engine.history(limit=args.limit), indent=2, default=str))
    return 0


def _cmd_inspect(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    data = engine.inspect(args.execution_id)
    if data is None:
        print(f"UNKNOWN execution: {args.execution_id}")
        return 1
    print(json.dumps(data, indent=2, default=str))
    return 0


def _cmd_approve(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    engine = Engine(root)
    updated = engine.approve(args.execution_id, args.step, args.decision == "yes",
                             note=args.note, decided_by=args.by)
    if updated is None:
        print(f"UNKNOWN execution: {args.execution_id}")
        return 1
    print(json.dumps(updated, indent=2, default=str))
    return 0


def _cmd_skill_publish(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    catalog = Catalog.from_repo(root)
    skill = catalog.get_skill(args.skill_id)
    if not skill:
        print(f"ERROR: Skill '{args.skill_id}' not found in catalog", file=sys.stderr)
        return 1
    mp = Marketplace(root)
    try:
        result = mp.publish(skill.source_path, force=args.force)
        print(json.dumps(result, indent=2, default=str))
        return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def _cmd_skill_install(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    mp = Marketplace(root)
    entry = mp.resolve(args.skill_spec)
    if entry is None:
        print(f"NOT FOUND: {args.skill_spec} (no version matches)", file=sys.stderr)
        return 1
    print(json.dumps({"status": "resolved", "name": entry.name, "version": entry.version,
                       "checksum": entry.checksum, "dependencies": entry.dependencies}, indent=2))
    return 0


def _cmd_skill_search(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    mp = Marketplace(root)
    results = mp.search(args.query, limit=args.limit)
    if not results:
        print("No results found.")
        return 0
    for e in results:
        print(f"  {e.name}@{e.version}  [{e.category}]  {e.description[:60]}")
    return 0


def _cmd_skill_list(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    mp = Marketplace(root)
    entries = mp.list_all()
    stats = mp.stats()
    print(f"Registry: {mp.registry_path} ({stats['unique_skills']} skills, {stats['total_versions']} versions)")
    for e in entries:
        print(f"  {e.name}@{e.version}  [{e.category}]")
    return 0


def _cmd_skill(args) -> int:
    if args.skill_command == "publish":
        return _cmd_skill_publish(args)
    elif args.skill_command == "install":
        return _cmd_skill_install(args)
    elif args.skill_command == "search":
        return _cmd_skill_search(args)
    elif args.skill_command == "list":
        return _cmd_skill_list(args)
    else:
        print("Usage: kdesk skill {publish|install|search|list} ...")
        return 2


def _cmd_delegate(args) -> int:
    catalog = _catalog(args)
    resolver = SubAgentResolver(catalog)
    plan = resolver.resolve(args.agent, input_data={})
    if plan is None:
        agent = catalog.get_agent(args.agent)
        if not agent:
            print(f"ERROR: Agent '{args.agent}' not found", file=sys.stderr)
            return 1
        print(f"Agent '{args.agent}' has no sub_agents declared.")
        return 0
    data = plan.summary()
    print(json.dumps(data, indent=2, default=str))
    return 0 if plan.all_succeeded else 3


def _cmd_version_resolve(args) -> int:
    catalog = _catalog(args)
    all_names = list(catalog.agents.keys()) + list(catalog.skills.keys())
    available = build_available_versions({n: True for n in all_names})
    resolver = VersionResolver()
    result = resolver.resolve(args.spec, available)
    if result is None:
        print(f"NO MATCH: {args.spec}", file=sys.stderr)
        return 1
    # Check for breaking change if we have a current version
    spec_parts = result.split("@")
    if len(spec_parts) == 2:
        check = resolver.check_breaking_change("1.0.0", spec_parts[1])
        print(json.dumps({"resolved": result, **({"breaking_change_check": check})}, indent=2))
    else:
        print(result)
    return 0


def _cmd_telemetry(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    stats = telemetry_summary(root)
    print(json.dumps(stats, indent=2))
    return 0
