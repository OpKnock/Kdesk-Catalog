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
    """Flatten + truncate description for YAML frontmatter (max 1024 chars)."""
    d = " ".join(str(agent.get("description", "")).split())
    return d[:1024].rstrip(":- ")


def build_markdown(agent: Dict[str, Any]) -> str:
    """Shared agent/skill body: description + instructions + capabilities."""
    parts = [f"# {agent.get('display_name', agent['name'])}", "", str(agent.get("description", "")).strip()]
    instructions = str(agent.get("instructions", "")).strip()
    if instructions:
        parts += ["", "## Instructions", "", instructions]
    caps = agent.get("capabilities") or []
    if caps:
        parts += ["", "## Capabilities"]
        for cap in caps:
            if not isinstance(cap, dict):
                continue
            parts += ["", f"### {cap.get('name', '')}", str(cap.get("description", "")).strip()]
            cmds = cap.get("commands") or []
            if cmds:
                parts += ["", "**Commands:**"] + [f"- `{c}`" for c in cmds]
            exs = cap.get("examples") or []
            if exs:
                parts += ["", "**Examples:**"] + [f"- {e}" for e in exs]
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
