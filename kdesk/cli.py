"""kdesk CLI - Universal Agent/Skill/Workflow registry orchestration.

Exit codes: 0 = success, 1 = fatal error, 2 = usage error,
3 = problems found (validation, drift, doctor, audits).

Command implementations live in kdesk/cli_commands/, grouped by domain:
- catalog_cmds: stats, registry, graph, capabilities, workflow, adapters
- lifecycle_cmds: install, uninstall, drift, status, rollback
- quality_cmds: doctor modes, security, audits, policy, verify, schema, wiring
- runtime_cmds: engine resolve/plan/run, approvals, skill marketplace,
  delegation, versioning, telemetry

All handler names are re-imported here so existing imports of
``kdesk.cli._cmd_*`` keep working.
"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from kdesk import __version__
from kdesk.registry import CatalogError

from kdesk.cli_commands.helpers import _out, _catalog, _subprocess_ok  # noqa: F401
from kdesk.cli_commands.catalog_cmds import (
    _cmd_stats, _cmd_registry, _cmd_graph, _cmd_capabilities,
    _cmd_workflow, _cmd_adapters,
)
from kdesk.cli_commands.lifecycle_cmds import (
    _cmd_install, _cmd_uninstall, _cmd_drift, _cmd_status, _cmd_rollback,
)
from kdesk.cli_commands.quality_cmds import (
    _cmd_doctor, _cmd_doctor_check, _cmd_doctor_diagnose, _cmd_doctor_ci,
    _cmd_doctor_fix, _cmd_doctor_scan,
    _cmd_security, _cmd_provenance, _cmd_quality, _cmd_license,
    _cmd_duplicates, _cmd_policy, _cmd_verify, _cmd_schema, _cmd_wiring,
)
from kdesk.cli_commands.runtime_cmds import (
    _cmd_resolve, _cmd_why, _cmd_plan, _cmd_run, _cmd_history,
    _cmd_inspect, _cmd_approve,
    _cmd_skill, _cmd_skill_publish, _cmd_skill_install, _cmd_skill_search,
    _cmd_skill_list, _cmd_delegate, _cmd_version_resolve, _cmd_telemetry,
    _cmd_serve, _cmd_trust,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kdesk", description="Universal AI Agent + Skill + Workflow Registry")
    p.add_argument("--version", action="version", version=f"kdesk {__version__}")
    p.add_argument("--root", default=None, help="repository root (default: derived from package location)")
    sub = p.add_subparsers(dest="command")

    root_parent = argparse.ArgumentParser(add_help=False)
    root_parent.add_argument("--root", default=None, help="repository root (default: derived from package location)")

    st = sub.add_parser("stats", parents=[root_parent], help="authoritative catalog statistics")
    st.add_argument("--format", choices=["json", "table"], default="json")
    st.add_argument("--baseline", action="store_true", help="write reports/baseline-stats.json")
    st.add_argument("--fast", action="store_true", help="skip slow platform output file count")

    r = sub.add_parser("registry", parents=[root_parent], help="catalog queries and stats")
    r.add_argument("--search", default=None, help="text search over names/descriptions/tags")
    r.add_argument("--errors", action="store_true", help="print load errors")

    g = sub.add_parser("graph", parents=[root_parent], help="agent->skill wiring graph")
    g.add_argument("--agent", default=None, help="show skills for an agent")

    c = sub.add_parser("capabilities", parents=[root_parent], help="capability/tool index")
    c.add_argument("--tool", default=None, help="capabilities invoking a tool")

    w = sub.add_parser("workflow", parents=[root_parent], help="workflow engine")
    w.add_argument("--validate", metavar="ID", help="validate a workflow")
    w.add_argument("--run", metavar="ID", help="run a workflow (dry-run by default)")
    w.add_argument("--execute", action="store_true", help="actually run capability commands")

    a = sub.add_parser("adapters", parents=[root_parent], help="platform adapter matrix")
    a.add_argument("--platform", default=None, help="single platform")
    a.add_argument("--format", choices=["json", "table"], default="json")

    i = sub.add_parser("install", parents=[root_parent], help="install platform artifacts")
    i.add_argument("platform")
    i.add_argument("--target", choices=["project", "home"], default="project")
    i.add_argument("--base", default=None, help="install base dir")
    i.add_argument("--home", default=None, help="home dir for ~-prefixed targets")
    i.add_argument("--scope", choices=None, default=None,
                   help="restrict install to one definition kind (agents|skills)")
    i.add_argument("--tool", default=None,
                   help="restrict install to definitions invoking a tool")
    i.add_argument("--agents", default=None,
                   help="restrict install to comma-separated definition ids")
    i.add_argument("--category", default=None,
                   help="restrict install to comma-separated categories")
    i.add_argument("--link", action="store_true",
                   help="create symlinks instead of copying")
    i.add_argument("--dry-run", action="store_true")

    u = sub.add_parser("uninstall", parents=[root_parent], help="remove installed artifacts")
    u.add_argument("platform")
    u.add_argument("--base", default=None, help="install base dir")
    u.add_argument("--dry-run", action="store_true")

    dr = sub.add_parser("drift", parents=[root_parent], help="detect modified/missing installs")
    dr.add_argument("--platform", default=None, help="single platform (default: all)")
    dr.add_argument("--base", default=None, help="install base dir")

    stt = sub.add_parser("status", parents=[root_parent], help="show installation manifest")
    stt.add_argument("--base", default=None, help="install base dir")

    rb = sub.add_parser("rollback", parents=[root_parent], help="restore from backup")
    rb.add_argument("platform")
    rb.add_argument("--base", default=None, help="install base dir")
    rb.add_argument("--dry-run", action="store_true")

    d = sub.add_parser("doctor", parents=[root_parent], help="verify installations + project diagnostics")
    d.add_argument("--platform", default=None, help="target platform (e.g., claude_code, opencode, codex_cli)")
    d.add_argument("--base", default=None, help="base directory for install check")
    d.add_argument("--format", choices=["json", "table"], default="json")
    d.add_argument("--mode", choices=["check", "diagnose", "fix", "scan"], default="check",
                   help="doctor mode: check (install verification), diagnose (full pipeline), fix (apply fixes), scan (scan project)")
    d.add_argument("--project-root", default=None, help="project directory to scan")
    d.add_argument("--fix", action="store_true", help="automatically fix fixable issues (diagnose mode)")
    d.add_argument("--dry-run", action="store_true", help="preview fixes without applying")
    d.add_argument("--json", action="store_true", help="output JSON")
    d.add_argument("--verbose", action="store_true", help="show detailed issue explanations")
    # CI mode
    d.add_argument("--ci", action="store_true", help="CI mode: exit with non-zero code if health below threshold")
    d.add_argument("--threshold", type=int, default=90, help="CI health threshold (0-100), exit non-zero if below")

    s = sub.add_parser("security", parents=[root_parent], help="secret scan")
    s.add_argument("--json", action="store_true")

    pv = sub.add_parser("provenance", parents=[root_parent], help="JSON->YAML traceability")
    pv.add_argument("--wiring", action="store_true", help="verify wiring evidence instead")

    q = sub.add_parser("quality", parents=[root_parent], help="content quality report")
    q.add_argument("--format", choices=["json", "table"], default="json")

    l = sub.add_parser("license", parents=[root_parent], help="license audit")
    l.add_argument("--format", choices=["json", "table"], default="json")

    pl = sub.add_parser("policy", parents=[root_parent], help="policy-as-code engine")
    pl.add_argument("--format", choices=["json", "table"], default="json")
    pl.add_argument("--policy-file", default=None, help="custom policy file (JSON/YAML)")

    du = sub.add_parser("duplicates", parents=[root_parent], help="duplicate family detection")
    du.add_argument("--format", choices=["json", "table"], default="json")

    rv = sub.add_parser("resolve", parents=[root_parent],
                        help="classify intent and find candidate definitions")
    rv.add_argument("request")
    rv.add_argument("--top", type=int, default=8)
    rv.add_argument("--no-env-probe", action="store_true")
    rv.add_argument("--json", action="store_true")

    wh = sub.add_parser("why", parents=[root_parent],
                        help="explain why a definition matched a request")
    wh.add_argument("request")
    wh.add_argument("target")

    pn = sub.add_parser("plan", parents=[root_parent],
                        help="build and evaluate an execution plan")
    pn.add_argument("request")
    pn.add_argument("--json", action="store_true")

    rn = sub.add_parser("run", parents=[root_parent],
                        help="run the full orchestration pipeline")
    rn.add_argument("request")
    rn.add_argument("--base", default=None, help="project base dir (default: cwd)")
    rn.add_argument("--auto-approve", action="store_true")
    rn.add_argument("--timeout", type=float, default=120.0)
    rn.add_argument("--execution-id", default=None)
    rn.add_argument("--dry-run", action="store_true")
    rn.add_argument("--json", action="store_true")

    h = sub.add_parser("history", parents=[root_parent],
                       help="list past executions")
    h.add_argument("--limit", type=int, default=20)

    ins = sub.add_parser("inspect", parents=[root_parent],
                         help="show execution record, events, artifacts, approvals")
    ins.add_argument("execution_id")

    ap = sub.add_parser("approve", parents=[root_parent],
                        help="approve or reject a pending step")
    ap.add_argument("execution_id")
    ap.add_argument("step", type=int)
    ap.add_argument("decision", choices=["yes", "no"])
    ap.add_argument("--note", default="")
    ap.add_argument("--by", default="kdesk")

    vf = sub.add_parser("verify", parents=[root_parent],
                        help="run the platform verification gate")
    vf.add_argument("--fast", action="store_true", help="skip slow checks")
    vf.add_argument("--skip", default=None, help="comma-separated check names to skip")
    vf.add_argument("--json", action="store_true")

    sc = sub.add_parser("schema", parents=[root_parent],
                        help="run the source schema check")
    sc.add_argument("--json", action="store_true")

    wg = sub.add_parser("wiring", parents=[root_parent],
                        help="verify agent->skill wiring evidence")
    wg.add_argument("--json", action="store_true")

    # Skill marketplace commands
    sk = sub.add_parser("skill", parents=[root_parent],
                        help="skill marketplace (publish, install, search, list)")
    sk_sub = sk.add_subparsers(dest="skill_command")

    sk_pub = sk_sub.add_parser("publish", help="publish a skill to the local registry")
    sk_pub.add_argument("skill_id", help="skill ID to publish")
    sk_pub.add_argument("--force", action="store_true", help="overwrite existing version")

    sk_inst = sk_sub.add_parser("install", help="resolve a skill spec (name@semver)")
    sk_inst.add_argument("skill_spec", help="skill@version or skill_id")

    sk_search = sk_sub.add_parser("search", help="search the registry")
    sk_search.add_argument("query", nargs="?", default="", help="search query")
    sk_search.add_argument("--limit", type=int, default=20)

    sk_list = sk_sub.add_parser("list", help="list available skills")

    dg = sub.add_parser("delegate", parents=[root_parent],
                        help="resolve sub-agent delegation for an agent")
    dg.add_argument("agent", help="agent name with sub_agents")

    vr = sub.add_parser("resolve-version", parents=[root_parent],
                        help="resolve a name@semver spec against the catalog")
    vr.add_argument("spec", help="e.g. my-agent@^2.0 or terraform-infrastructure")

    tl = sub.add_parser("telemetry", parents=[root_parent],
                        help="show anonymous usage stats")

    tr = sub.add_parser("trust", parents=[root_parent],
                        help="calculate trust score for a definition")
    tr.add_argument("name", help="definition name")
    tr.add_argument("--platform", default=None, help="target platform")
    tr.add_argument("--json", action="store_true", help="output as JSON")

    sv = sub.add_parser("serve", parents=[root_parent],
                        help="launch the local web dashboard")
    sv.add_argument("--host", default="127.0.0.1")
    sv.add_argument("--port", type=int, default=8000)
    sv.add_argument("--no-browser", action="store_true",
                    help="do not auto-open the browser")

    return p


def main(argv: Optional[List[str]] = None) -> int:
    # Windows consoles default to cp1252, which crashes on the box-drawing
    # characters used in doctor/fix reports. Force UTF-8 with replacement.
    for _stream in (sys.stdout, sys.stderr):
        try:
            enc = getattr(_stream, "encoding", "") or ""
            if enc.lower().replace("-", "") != "utf8":
                _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    handlers = {
        "stats": _cmd_stats,
        "registry": _cmd_registry,
        "graph": _cmd_graph,
        "capabilities": _cmd_capabilities,
        "workflow": _cmd_workflow,
        "adapters": _cmd_adapters,
        "install": _cmd_install,
        "uninstall": _cmd_uninstall,
        "drift": _cmd_drift,
        "status": _cmd_status,
        "rollback": _cmd_rollback,
        "doctor": _cmd_doctor,
        "security": _cmd_security,
        "provenance": _cmd_provenance,
        "quality": _cmd_quality,
        "license": _cmd_license,
        "duplicates": _cmd_duplicates,
        "policy": _cmd_policy,
        "resolve": _cmd_resolve,
        "why": _cmd_why,
        "plan": _cmd_plan,
        "run": _cmd_run,
        "history": _cmd_history,
        "inspect": _cmd_inspect,
        "approve": _cmd_approve,
        "verify": _cmd_verify,
        "schema": _cmd_schema,
        "wiring": _cmd_wiring,
        "skill": _cmd_skill,
        "delegate": _cmd_delegate,
        "resolve-version": _cmd_version_resolve,
        "telemetry": _cmd_telemetry,
        "trust": _cmd_trust,
        "serve": _cmd_serve,
    }
    handler = handlers.get(args.command)
    if handler is None:
        build_parser().print_help()
        return 2
    try:
        return handler(args)
    except CatalogError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
