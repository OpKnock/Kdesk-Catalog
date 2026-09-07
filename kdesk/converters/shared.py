"""Shared loader/markdown helpers for converters."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from kdesk.converters.constants import (
    ALL_PLATFORMS,
    DEPRECATED_SINGLE_FILE_PLATFORMS,
    TOOLS_MANIFEST_PATH,
)
from kdesk.converters import constants as cfg


def load_tools_manifest(path: Path = TOOLS_MANIFEST_PATH) -> Dict[str, Any]:
    """Load the tools manifest (tools.json) describing every platform."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_tools_manifest(manifest: Optional[Dict[str, Any]] = None) -> List[str]:
    """Cross-check tools.json against ALL_PLATFORMS and the deprecated set.

    Returns a list of error strings (empty when the manifest is valid).
    """
    if manifest is None:
        manifest = load_tools_manifest()
    errors: List[str] = []
    tools = manifest.get("tools", {})
    expected = set(ALL_PLATFORMS) | set(DEPRECATED_SINGLE_FILE_PLATFORMS)
    missing = sorted(expected - set(tools))
    extra = sorted(set(tools) - expected)
    if missing:
        errors.append(f"tools.json missing platform entries: {', '.join(missing)}")
    if extra:
        errors.append(f"tools.json has unknown platform entries: {', '.join(extra)}")
    required = (
        "id", "label", "kebab", "accent", "icon", "order",
        "scope", "detect", "version", "format",
        "installKind", "slugFrom", "slugPrefix", "dest",
    )
    for key, entry in tools.items():
        if entry.get("id") != key:
            errors.append(f"{key}: id != manifest key")
        if entry.get("kebab") != key:
            errors.append(f"{key}: kebab != manifest key")
        for field in required:
            if field not in entry:
                errors.append(f"{key}: missing field '{field}'")
        dest = entry.get("dest", {})
        if "user" not in dest or "project" not in dest:
            errors.append(f"{key}: dest must have 'user' and 'project'")
        detect = entry.get("detect", {})
        if "dirs" not in detect or "agentsDir" not in detect:
            errors.append(f"{key}: detect must have 'dirs' and 'agentsDir'")
    return errors


def load_universal_agent(path: Path) -> Dict[str, Any]:
    """Load and validate a universal agent YAML"""
    with open(path, 'r', encoding='utf-8') as f:
        agent = yaml.safe_load(f)

    # Compute checksum
    content = path.read_bytes()
    agent['checksum'] = hashlib.sha256(content).hexdigest()[:16]
    agent['file_path'] = str(path)

    return agent


def get_all_universal_agents() -> List[Dict[str, Any]]:
    """Load all universal agents from directory"""
    agents = []
    for yaml_file in cfg.UNIVERSAL_DIR.rglob("*.yaml"):
        if yaml_file.name == "registry.yaml":
            continue
        try:
            agent = load_universal_agent(yaml_file)
            agents.append(agent)
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")
    return agents


def slugify(name: str) -> str:
    """Lowercase alphanumeric + single hyphens, max 64 chars (SKILL.md spec)."""
    slug = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    return (slug[:64]).rstrip("-") or "skill"


def desc_safe(agent: Dict[str, Any]) -> str:
    """Flatten + truncate description for YAML frontmatter (max 1024 chars).

    Official SKILL.md spec requires description to contain BOTH what it does
    AND when to use it with trigger keywords. We auto-append 'Use when'
    triggers from capabilities/tags if not already present.
    """
    d = " ".join(str(agent.get("description", "")).split())
    # Ensure trigger phrasing for Agent Skills activation
    lower = d.lower()
    if "use when" not in lower and "when to use" not in lower:
        # Build trigger from capabilities and tags
        triggers = []
        for cap in agent.get("capabilities", []) or []:
            if isinstance(cap, dict) and cap.get("name"):
                triggers.append(cap["name"].replace("-", " "))
        for tag in agent.get("tags", [])[:3]:
            if tag.lower() not in " ".join(triggers).lower():
                triggers.append(tag.replace("-", " "))
        if triggers:
            trigger_phrase = ", ".join(triggers[:4])
            suffix = f" Use when working with {trigger_phrase} or when the user mentions {trigger_phrase}."
            # Ensure we stay within 1024
            if len(d) + len(suffix) <= 1024:
                d = d.rstrip(".") + "." + suffix
            else:
                d = (d[:1024 - len(suffix) - 3].rstrip(":- ") + "..." + suffix)[:1024]
    return d[:1024].rstrip(":- ")


def _tool_binaries(agent: Dict[str, Any]) -> list:
    """Derive tool binaries from capabilities[].commands (first token of each command)."""
    bins = []
    for cap in agent.get("capabilities", []) or []:
        for cmd in cap.get("commands", []) or []:
            if not isinstance(cmd, str):
                continue
            parts = cmd.strip().split()
            if not parts:
                continue
            first = parts[0].lstrip("$").rstrip(":")
            # Map common binaries to Claude Code tool names
            mapping = {
                "curl": "Bash", "kubectl": "Bash", "helm": "Bash", "git": "Bash",
                "docker": "Bash", "npm": "Bash", "yarn": "Bash", "pip": "Bash",
                "python": "Bash", "node": "Bash", "go": "Bash", "cargo": "Bash",
                "promtool": "Bash", "jq": "Bash", "yq": "Bash", "psql": "Bash",
            }
            tool = mapping.get(first, "Bash") if first in mapping else first.capitalize() if first.islower() else first
            # Keep Bash for shell commands, Read/Grep/Glob for file ops
            if first in ("read", "grep", "glob", "write", "edit"):
                tool = first.capitalize()
            if tool not in bins:
                bins.append(tool)
    # Always include core read tools for Read phase
    for core in ["Read", "Grep", "Glob"]:
        if core not in bins:
            bins.insert(0, core)
    return bins[:12]


def _allowed_tools_str(agent: Dict[str, Any]) -> str:
    """Build Agent Skills allowed-tools string: Bash(cmd:*) patterns."""
    bins = set()
    for cap in agent.get("capabilities", []) or []:
        for cmd in cap.get("commands", []) or []:
            if isinstance(cmd, str) and cmd.strip():
                bins.add(cmd.strip().split()[0].lstrip("$"))
    if not bins:
        return "Read Grep Glob"
    # Map to Bash(pattern:*) for shell tools, keep Read/Grep/Glob as is
    parts = []
    for b in sorted(bins):
        if b.lower() in ("read", "grep", "glob", "write", "edit"):
            parts.append(b.capitalize())
        else:
            parts.append(f"Bash({b}:*)")
    # Add core read tools
    for core in ["Read", "Grep", "Glob"]:
        if core not in parts:
            parts.insert(0, core)
    return " ".join(parts[:10])


def _compatibility_str(agent: Dict[str, Any]) -> str:
    """Build SKILL.md compatibility string from prerequisites/tools."""
    prereqs = agent.get("prerequisites") or []
    tools = agent.get("tools") or []
    combined = prereqs + [t for t in tools if t not in prereqs]
    if combined:
        base = f"Requires {', '.join(combined[:6])}."
        # Add network note if commands use curl/kubectl
        has_network = any("curl" in str(c.get("commands", [])) or "kubectl" in str(c.get("commands", [])) for c in agent.get("capabilities", []) or [])
        if has_network:
            base += " Needs network access for API calls."
        return base[:500]
    return ""


def _metadata_dict(agent: Dict[str, Any]) -> dict:
    """Build SKILL.md metadata map."""
    return {
        "author": str(agent.get("author", "Kdesk")),
        "version": str(agent.get("version", "1.0.0")),
        "category": str(agent.get("category", "general")),
    }


def build_markdown(agent: Dict[str, Any]) -> str:
    """Shared agent/skill body with Read-Reason-Act loop for agentic behavior.

    All agents/skills follow: Read -> Reason -> Act. Sub-agents are documented
    with Task tool delegation. This matches msitarzewski/agency-agents style
    (personality + workflow + deliverables) and google/skills progressive disclosure.
    """
    # Avoid duplicate title if instructions already starts with markdown heading
    title = agent.get('display_name', agent['name'])
    desc = str(agent.get("description", "")).strip()
    instructions = str(agent.get("instructions", "")).strip()
    # Check if instructions already contains a top-level heading
    has_heading = instructions.lstrip().startswith("#")

    parts = []
    if not has_heading:
        parts += [f"# {title}", "", desc]
    else:
        parts += [desc]

    # Core Read-Reason-Act loop — every agent/skill is an agentic loop, not static prompt
    sub_agents = agent.get("sub_agents") or []
    delegation = agent.get("delegation_pattern")
    caps = agent.get("capabilities") or []

    # Add agentic workflow section if not already in instructions (check for marker, not substring "## Read" which matches "## Reading")
    if "Agentic Workflow" not in instructions:
        parts += ["", "## Agentic Workflow: Read -> Reason -> Act", "",
                  "You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:"]
        parts += ["", "### 1. Read", "Gather context before acting:"]
        parts += ["- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)"]
        if caps:
            # Infer read commands
            read_hints = []
            for cap in caps[:2]:
                if isinstance(cap, dict) and cap.get("commands"):
                    read_hints.append(f"`{cap['commands'][0][:60]}`")
            if read_hints:
                parts += [f"- Domain context: {', '.join(read_hints)}"]
        parts += ["- Check `knowledge` references and prerequisites before proceeding"]

        parts += ["", "### 2. Reason", "Analyze and plan:"]
        parts += ["- Compare current state vs desired state (drift, checksums, policy)"]
        parts += ["- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns"]
        parts += ["- Decide: which capabilities/tools are needed, which can be skipped"]

        parts += ["", "### 3. Act", "Execute with guards:"]
        parts += ["- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes"]
        parts += ["- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell"]
        parts += ["- Record evidence: file paths, checksums, and tool outputs for verification"]

        if sub_agents:
            parts += ["", "### Delegation (Sub-Agents)"]
            if delegation == "parallel":
                parts += [f"- **Parallel**: Delegate to `{', '.join(sub_agents)}` concurrently via `Task` tool with `subagent_type`."]
                parts += ["- Each sub-agent reads its own domain, reasons independently, then reports back."]
                parts += ["- You (orchestrator) merge results and act on combined evidence."]
            elif delegation == "sequential":
                parts += [f"- **Sequential**: Delegate to `{', '.join(sub_agents)}` in order; next starts after previous completes."]
            elif delegation == "conditional":
                parts += [f"- **Conditional**: Delegate based on reasoning outcome — choose sub-agent dynamically."]
            else:
                parts += [f"- Delegate to sub-agents `{', '.join(sub_agents)}` via `Task` tool (subagent_type) when their domain is needed."]
            parts += ["- Sub-agents are files in `.claude/agents/*.md` — invoke with `Task` or `claude -p --agent <name>` if CLI is available; otherwise use kdesk orchestrator."]

    if instructions:
        # Avoid duplicating title
        if has_heading:
            parts += ["", instructions]
        else:
            parts += ["", "## Instructions", "", instructions]

    if caps:
        parts += ["", "## Capabilities"]
        for cap in caps:
            if not isinstance(cap, dict):
                continue
            parts += ["", f"### {cap.get('name', '')}", str(cap.get("description", "")).strip()]
            # Parameters (for skill arguments)
            params = cap.get("parameters") or []
            if params:
                parts += ["", "**Parameters:**"]
                for p in params:
                    if isinstance(p, dict):
                        parts += [f"- `{p.get('name')}` ({p.get('type','string')}): {p.get('description','')}"]
            cmds = cap.get("commands") or []
            if cmds:
                parts += ["", "**Commands:**"] + [f"- `{c}`" for c in cmds]
            exs = cap.get("examples") or []
            if exs:
                parts += ["", "**Examples:**"] + [f"- {e}" for e in exs]

    # Knowledge and guardrails
    knowledge = agent.get("knowledge") or []
    if knowledge:
        parts += ["", "## References"]
        for k in knowledge:
            if isinstance(k, dict):
                title = k.get("title", "")
                src = k.get("source", k.get("url", ""))
                if src:
                    parts += [f"- [{title}]({src})"]
                elif title:
                    parts += [f"- {title}"]

    # Progressive disclosure hint for large skills
    if len(caps) > 3:
        parts += ["", "## Progressive Disclosure",
                  "This skill has many capabilities. For detailed reference:",
                  "- `references/REFERENCE.md` — full capability docs and edge cases",
                  "- `scripts/` — executable helpers (see `allowed-tools`)",
                  "- `assets/` — templates and data files",
                  "Load references on demand via relative paths, not at startup."]

    return "\n".join(parts)


def infer_globs(agent: Dict[str, Any]) -> List[str]:
    """Infer file globs from agent's capabilities and tags."""
    globs = set()
    text = " ".join([
        str(agent.get("description", "")),
        str(agent.get("instructions", "")),
        " ".join(cap.get("name", "") + " " + " ".join(cap.get("commands", []))
                 for cap in agent.get("capabilities", []))
    ]).lower()

    lang_globs = {
        "python": "**/*.py",
        "javascript": "**/*.{js,ts,jsx,tsx}",
        "typescript": "**/*.{ts,tsx}",
        "go": "**/*.go",
        "rust": "**/*.rs",
        "java": "**/*.java",
        "c++": "**/*.{cpp,cc,h,hpp}",
        "c#": "**/*.cs",
        "ruby": "**/*.rb",
        "php": "**/*.php",
        "swift": "**/*.swift",
        "kotlin": "**/*.kt",
        "scala": "**/*.scala",
        "r": "**/*.r",
        "julia": "**/*.jl",
        "shell": "**/*.sh",
        "bash": "**/*.sh",
        "dockerfile": "**/Dockerfile*",
        "terraform": "**/*.tf",
        "yaml": "**/*.{yaml,yml}",
        "json": "**/*.json",
        "sql": "**/*.sql",
        "html": "**/*.html",
        "css": "**/*.css",
    }

    for lang, glob in lang_globs.items():
        if lang in text:
            globs.add(glob)

    # Also check tags
    for tag in agent.get("tags", []):
        tag_lower = tag.lower()
        if tag_lower in lang_globs:
            globs.add(lang_globs[tag_lower])

    return sorted(globs)
