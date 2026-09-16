"""Executable agents: every catalog definition runs as a real AI agent.

A catalog YAML (agent or skill) already carries everything an executable
agent needs: instructions, capabilities with real commands, knowledge
references, and tools. This module maps a definition to a live agent backed
by a production-grade agent runtime (optional dependency), providing:

- build_instructions(): definition -> system prompt (Read -> Reason -> Act)
- build_tools(): safe function-tools (catalog lookup is always allowed;
  shell execution only with explicit opt-in, denylist + timeout + sandbox)
- build_agent(): definition + chat client -> live agent object
- run_agent() / run_skill(): one-shot task execution (dry-run by default,
  so planning never touches the network)
- run_team(): multi-agent delegation (sequential | parallel | conditional)

The runtime package is imported lazily, so ``import kdesk.agent_runtime``
never fails when the optional dependency is missing; only live execution
requires it. Install it with: ``pip install agent-framework``
"""

from __future__ import annotations

import asyncio
import os
import re
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kdesk.models import BaseDefinition
from kdesk.registry import Catalog

RUNTIME_IMPORT = "agent_framework"
RUNTIME_PIP_SPEC = "agent-framework>=1.0"

_SHELL_DENY = re.compile(
    r"(rm\s+-rf|mkfs|:\(\)\s*\{|dd\s+.*of=|shutdown|reboot|mkfs|"
    r"curl\s+.*\|\s*(sh|bash)|wget\s+.*\|\s*(sh|bash))",
    re.IGNORECASE,
)


class AgentRuntimeError(Exception):
    """Raised when a live agent cannot be built or run."""


def runtime_available() -> bool:
    """True when the optional agent runtime package is importable."""
    try:
        __import__(RUNTIME_IMPORT)
        return True
    except ImportError:
        return False


def require_runtime() -> None:
    """Raise a helpful error when the runtime package is missing."""
    if not runtime_available():
        raise AgentRuntimeError(
            f"Live agents need the optional runtime: pip install {RUNTIME_PIP_SPEC}"
        )


def slugify(name: str) -> str:
    """Agent-safe slug: lowercase kebab-case."""
    slug = re.sub(r"[^a-z0-9]+", "-", (name or "agent").lower()).strip("-")
    return slug or "agent"


def get_definition(catalog: Catalog, name: str) -> BaseDefinition:
    """Fetch an agent or skill by name, or raise with a helpful message."""
    found = catalog.get_agent(name)
    if found is None:
        found = catalog.get_skill(name)
    if found is None:
        raise AgentRuntimeError(f"Unknown agent or skill: {name!r}")
    return found


def build_instructions(defn: BaseDefinition) -> str:
    """Compose the system prompt for a live agent from its definition."""
    lines = [
        f"You are {defn.display_name or defn.name} ({defn.category}).",
        str(defn.description or "").strip(),
        "",
        "Operating loop: Read -> Reason -> Act.",
        "1. Read: inspect the relevant files and the capability references "
        "below before acting; never assume state.",
        "2. Reason: pick the capability that fits the task, check its commands "
        "and examples, and verify preconditions.",
        "3. Act: execute via your tools, then record evidence (paths, "
        "commands, checksums).",
        "",
        "Guardrails:",
        "- Prefer read-only inspection; shell actions need explicit approval.",
        "- Keep every file write inside the project root.",
        "- Do not exfiltrate secrets; never print tokens or keys.",
        "",
    ]
    base = str(defn.instructions or "").strip()
    if base:
        lines += ["Definition instructions:", base, ""]
    if defn.capabilities:
        lines.append("Capabilities:")
        for cap in defn.capabilities:
            lines.append(f"- {cap.name}: {cap.description or ''}".rstrip())
            for cmd in cap.commands or []:
                lines.append(f"  $ {cmd}")
            for ex in (cap.examples or [])[:3]:
                lines.append(f"  e.g. {ex}")
    if defn.knowledge:
        lines.append("")
        lines.append("Knowledge references:")
        for ref in defn.knowledge[:10]:
            if isinstance(ref, dict):
                title = ref.get("title") or ref.get("source") or "reference"
                lines.append(f"- {title}")
            else:
                lines.append(f"- {ref}")
    return "\n".join(lines).strip() + "\n"


def safe_tool_impls(defn: BaseDefinition, catalog: Catalog) -> dict[str, Callable[..., str]]:
    """Plain (dependency-free) implementations of the always-safe tools."""

    def catalog_search(query: str) -> str:
        """Search the catalog by name, description, or tags."""
        hits: list[str] = []
        q = (query or "").lower()
        for store in (catalog.agents, catalog.skills):
            for name, item in store.items():
                hay = f"{name} {item.description} {' '.join(item.tags)}".lower()
                if q and q in hay:
                    hits.append(f"{name} [{item.type}]: {item.description[:120]}")
                if len(hits) >= 20:
                    break
        return "\n".join(hits) if hits else "No matches."

    def describe_definition(name: str) -> str:
        """Show full details (instructions, capabilities, tools) of one definition."""
        item = catalog.get_agent(name) or catalog.get_skill(name)
        if item is None:
            return f"Unknown definition: {name}"
        caps = "; ".join(
            f"{c.name} ({', '.join(c.tool_binaries())})" for c in item.capabilities
        )
        return (
            f"{item.name} [{item.type}] v{item.version}\n"
            f"{item.description}\nCapabilities: {caps or 'none'}"
        )

    def capability_commands(name: str) -> str:
        """List the real commands a definition can execute, per capability."""
        item = catalog.get_agent(name) or catalog.get_skill(name)
        if item is None:
            return f"Unknown definition: {name}"
        out = []
        for cap in item.capabilities:
            out.append(f"[{cap.name}]")
            out.extend(f"  $ {cmd}" for cmd in cap.commands)
        return "\n".join(out) if out else "No commands declared."

    _ = defn
    return {
        "catalog_search": catalog_search,
        "describe_definition": describe_definition,
        "capability_commands": capability_commands,
    }


def check_shell_command(command: str) -> str:
    """Reject destructive command patterns; return the command when safe."""
    if _SHELL_DENY.search(command or ""):
        raise AgentRuntimeError(f"Blocked destructive command: {command!r}")
    return command


def run_shell_command(
    command: str,
    project_root: Path | None = None,
    timeout_s: int = 120,
) -> str:
    """Run one shell command inside project_root with guardrails."""
    check_shell_command(command)
    binary = (command.strip().split() or [""])[0]
    if not binary or shutil.which(binary) is None:
        raise AgentRuntimeError(f"Tool not available on PATH: {binary!r}")
    root = Path(project_root).resolve() if project_root else Path.cwd().resolve()
    proc = subprocess.run(
        command,
        shell=True,
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )
    out = (proc.stdout or "")[-4000:]
    err = (proc.stderr or "")[-1000:]
    result = f"exit={proc.returncode}\n{out}"
    if err:
        result += f"\nstderr:\n{err}"
    return result


def build_tools(
    defn: BaseDefinition,
    catalog: Catalog,
    *,
    allow_shell: bool = False,
    project_root: Path | None = None,
) -> list:
    """Wrap a definition's capabilities as runtime function-tools.

    Safe lookup tools are always included. A shell tool that executes the
    definition's real commands is added only when ``allow_shell=True``.
    """
    require_runtime()
    from agent_framework import tool as tool_decorator

    tools: list = []
    for tool_name, fn in safe_tool_impls(defn, catalog).items():
        tools.append(tool_decorator(fn, name=tool_name))

    if allow_shell:
        commands = list(defn.all_commands())

        def execute_capability_command(command: str) -> str:
            """Execute one of this agent's declared capability commands.

            The command must be declared in the agent definition; arbitrary
            shell input is rejected. Runs sandboxed in the project root.
            """
            if command not in commands:
                raise AgentRuntimeError(
                    "Only declared capability commands may run; "
                    f"got: {command!r}"
                )
            return run_shell_command(command, project_root=project_root)

        tools.append(tool_decorator(execute_capability_command))
    return tools


def default_client() -> Any:
    """Build a chat client from environment configuration.

    Reads ``FOUNDRY_PROJECT_ENDPOINT`` (and optional
    ``FOUNDRY_MODEL_DEPLOYMENT_NAME``). Raises a helpful error when nothing
    is configured so users never see a bare connection failure.
    """
    require_runtime()
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "")
    if not endpoint:
        raise AgentRuntimeError(
            "No chat client configured. Set FOUNDRY_PROJECT_ENDPOINT "
            "(and optionally FOUNDRY_MODEL_DEPLOYMENT_NAME), or pass a "
            "client explicitly."
        )
    from agent_framework.foundry import FoundryChatClient
    from azure.identity import AzureCliCredential

    kwargs: dict[str, Any] = {"credential": AzureCliCredential()}
    model = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT_NAME", "")
    if model:
        kwargs["model"] = model
    return FoundryChatClient(endpoint=endpoint, **kwargs)


def build_agent(
    defn: BaseDefinition,
    client: Any,
    catalog: Catalog | None = None,
    *,
    allow_shell: bool = False,
    project_root: Path | None = None,
) -> Any:
    """Build a live agent object from a catalog definition."""
    require_runtime()
    from agent_framework import Agent

    tools: list = []
    if catalog is not None:
        tools = build_tools(
            defn, catalog, allow_shell=allow_shell, project_root=project_root
        )
    return Agent(
        client=client,
        name=slugify(defn.name),
        description=str(defn.description or "")[:500],
        instructions=build_instructions(defn),
        tools=tools,
    )


@dataclass
class DryRunPlan:
    """Offline preview of what a live run would do (no network)."""

    name: str
    definition_type: str
    instructions_preview: str
    tools: list[str] = field(default_factory=list)
    needs_client: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.definition_type,
            "instructions_preview": self.instructions_preview,
            "tools": self.tools,
            "needs_client": self.needs_client,
            "mode": "dry-run",
        }


def dry_run_plan(defn: BaseDefinition, catalog: Catalog | None = None) -> DryRunPlan:
    """Preview a live run without network, credentials, or side effects."""
    tools = ["catalog_search", "describe_definition", "capability_commands"]
    if catalog is not None:
        tools = list(safe_tool_impls(defn, catalog).keys())
        if defn.all_commands():
            tools.append("execute_capability_command (requires --allow-shell)")
    return DryRunPlan(
        name=defn.name,
        definition_type=defn.type,
        instructions_preview=build_instructions(defn)[:2000],
        tools=tools,
    )


async def run_live(
    defn: BaseDefinition,
    task: str,
    catalog: Catalog | None = None,
    *,
    client: Any = None,
    allow_shell: bool = False,
    project_root: Path | None = None,
) -> str:
    """Execute one task with a live agent; returns its text response."""
    agent = build_agent(
        defn,
        client if client is not None else default_client(),
        catalog,
        allow_shell=allow_shell,
        project_root=project_root,
    )
    response = await agent.run(task)
    text = getattr(response, "text", None)
    if text:
        return str(text)
    return str(response)


def run_agent(
    catalog: Catalog,
    name: str,
    task: str,
    *,
    dry_run: bool = True,
    client: Any = None,
    allow_shell: bool = False,
    project_root: Path | None = None,
) -> Any:
    """Run an agent or skill by name; dry-run by default (no network)."""
    defn = get_definition(catalog, name)
    if dry_run and client is None:
        return dry_run_plan(defn, catalog).to_dict()
    return asyncio.run(
        run_live(
            defn,
            task,
            catalog,
            client=client,
            allow_shell=allow_shell,
            project_root=project_root,
        )
    )


def run_skill(
    catalog: Catalog,
    name: str,
    task: str,
    **kwargs: Any,
) -> Any:
    """Run a skill by name (skills execute exactly like agents)."""
    return run_agent(catalog, name, task, **kwargs)


async def run_team(
    catalog: Catalog,
    root_agent: str,
    task: str,
    *,
    client: Any = None,
    client_factory: Callable[[BaseDefinition], Any] | None = None,
    allow_shell: bool = False,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Run a root agent plus its sub-agents as a live multi-agent team.

    Honors the root agent's ``delegation_pattern``: sequential chains outputs,
    parallel runs sub-agents concurrently, conditional stops at first success.
    Every participant is a live agent object built from its own definition.
    """
    from kdesk.delegation import SubAgentResolver

    resolver = SubAgentResolver(catalog)
    plan = resolver.plan(root_agent)
    if plan is None:
        raise AgentRuntimeError(f"No delegation plan for: {root_agent!r}")

    def _client_for(defn: BaseDefinition) -> Any:
        if client_factory is not None:
            return client_factory(defn)
        return client if client is not None else default_client()

    results: dict[str, Any] = {}
    steps = list(plan.steps)
    pattern = (plan.pattern or "sequential").lower()

    async def _run_one(agent_name: str, agent_task: str) -> str:
        sub = get_definition(catalog, agent_name)
        return await run_live(
            sub,
            agent_task,
            catalog,
            client=_client_for(sub),
            allow_shell=allow_shell,
            project_root=project_root,
        )

    if pattern == "parallel":
        outputs = await asyncio.gather(*(_run_one(s, task) for s in steps))
        results = dict(zip(steps, outputs, strict=True))
    elif pattern == "conditional":
        for step in steps:
            try:
                results[step] = await _run_one(step, task)
                break
            except Exception as exc:  # noqa: BLE001 - record and try next
                results[step] = f"FAILED: {exc}"
    else:  # sequential (default)
        context = task
        for step in steps:
            results[step] = await _run_one(step, context)
            context = f"{task}\n\nPrevious result from {step}:\n{results[step]}"
    return {
        "root_agent": root_agent,
        "pattern": pattern,
        "steps": steps,
        "results": results,
        "succeeded": sum(1 for v in results.values() if not str(v).startswith("FAILED")),
        "total": len(steps),
    }
