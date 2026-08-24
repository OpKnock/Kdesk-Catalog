"""Install lifecycle commands: install, uninstall, drift, status, rollback."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from kdesk.adapters import AdapterRegistry
from kdesk.installer import Installer, InstallError
from kdesk.registry import default_repo_root


def _cmd_install(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters, dry_run=args.dry_run,
                          home_dir=Path(args.home) if args.home else None)
    try:
        result = installer.install(
            args.platform, target=args.target,
            base=Path(args.base) if args.base else None,
            scope=args.scope, tool=args.tool,
            agents=set(args.agents.split(",")) if args.agents else None,
            category=set(args.category.split(",")) if args.category else None,
            link=args.link)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        if str(exc).startswith(("unknown scope", "unknown tool",
                                "filter (scope", "filter (tool",
                                "filter (agents", "filter (category")):
            return 2
        return 1
    total = sum(r.get("files", 0) for r in result.get("results", []))
    if args.platform == "opencode" and total > 119:
        print(f"WARNING: opencode supports ~119 subagents upstream; "
              f"{total} definitions selected, excess will not be usable",
              file=sys.stderr)
    print(json.dumps(result, indent=2, default=str))
    return 0


def _cmd_uninstall(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters, dry_run=args.dry_run)
    try:
        result = installer.uninstall(args.platform,
                                     base=Path(args.base) if args.base else None)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, indent=2, default=str))
    return 0


def _cmd_drift(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters)
    try:
        report = installer.drift(args.platform,
                                 base=Path(args.base) if args.base else None)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["clean"] else 3


def _cmd_status(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters)
    print(json.dumps(installer.status(base=Path(args.base) if args.base else None),
                     indent=2, default=str))
    return 0


def _cmd_rollback(args) -> int:
    adapters = AdapterRegistry(Path(args.root) if args.root else default_repo_root())
    installer = Installer(adapters, dry_run=args.dry_run)
    try:
        result = installer.rollback(args.platform,
                                    base=Path(args.base) if args.base else None)
    except InstallError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, indent=2, default=str))
    return 0
