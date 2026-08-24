"""Catalog inspection commands: stats, registry, graph, capabilities, workflow, adapters."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from kdesk.adapters import AdapterRegistry
from kdesk.capabilities import CapabilityIndex
from kdesk.graph import CatalogGraph
from kdesk.registry import default_repo_root
from kdesk.stats import StatsError, compute as compute_stats, format_table, write_baseline
from kdesk.workflow import WorkflowEngine, WorkflowError

from kdesk.cli_commands.helpers import _catalog, _out


def _cmd_stats(args) -> int:
    root = Path(args.root) if args.root else default_repo_root()
    try:
        stats = compute_stats(root, fast=args.fast)
    except StatsError as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 1
    if args.baseline:
        path = write_baseline(root)
        print(f"baseline written: {path}", flush=True)
        return 0
    if args.format == "table":
        print(format_table(stats))
        return 0
    print(json.dumps(stats, indent=2, default=str))
    return 0


def _cmd_registry(args) -> int:
    catalog = _catalog(args)
    if args.search:
        hits = catalog.search(args.search)
        for h in hits:
            print(f"{h.type:6s} {h.name:40s} {h.category}")
        return 0
    stats = catalog.stats()
    if args.errors and catalog.errors:
        for e in catalog.errors[:50]:
            print(f"ERROR: {e}")
    print(json.dumps(stats, indent=2, default=str))
    return 1 if catalog.errors else 0


def _cmd_graph(args) -> int:
    catalog = _catalog(args)
    root = Path(args.root) if args.root else default_repo_root()
    graph = CatalogGraph(catalog, wiring_path=root / "skills" / "wiring.json")
    if args.agent:
        for link in graph.agent_skills(args.agent):
            print(f"{args.agent} -> {link['skill']}  [evidence={link['evidence']}, manual={link['manual']}]")
        return 0
    print(json.dumps(graph.summary(), indent=2, default=str))
    return 0


def _cmd_capabilities(args) -> int:
    catalog = _catalog(args)
    idx = CapabilityIndex(list(catalog.agents.values()) + list(catalog.skills.values()))
    if args.tool:
        for defn, cap in idx.capabilities_for_tool(args.tool):
            print(f"{defn} :: {cap}")
        return 0
    print(json.dumps(idx.summary(), indent=2, default=str))
    return 0


def _cmd_workflow(args) -> int:
    catalog = _catalog(args)
    root = Path(args.root) if args.root else default_repo_root()
    engine = WorkflowEngine(catalog, workflows_dir=root / "workflows")
    if args.validate:
        wf = engine.load(args.validate)
        problems = engine.validate(wf)
        if problems:
            for p in problems:
                print(f"PROBLEM: {p}")
            return 3
        print(f"OK: {wf.id} ({len(wf.steps)} steps)")
        return 0
    if args.run:
        wf = engine.load(args.run)
        try:
            result = engine.run(wf, dry_run=not args.execute)
        except WorkflowError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(json.dumps(result, indent=2, default=str))
        return 0
    print(json.dumps(engine.summary(), indent=2, default=str))
    return 0


def _cmd_adapters(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    summary = adapters.summary()
    if args.platform:
        a = adapters.get(args.platform)
        if a is None:
            print(f"UNKNOWN platform: {args.platform}")
            return 1
        print(json.dumps(a.verify(), indent=2, default=str))
        return 0
    _out(summary, args.format)
    return 0
