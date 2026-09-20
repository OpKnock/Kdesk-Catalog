"""Conversion pipeline: convert_all, registry, validation, CLI entry point."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

from kdesk.converters import constants as cfg
from kdesk.converters.constants import ALL_PLATFORMS, NEW_PLATFORMS
from kdesk.converters.native import (
    convert_to_claude_code,
    convert_to_copilot,
    convert_to_cursor,
    convert_to_generic,
    convert_to_opencode,
    convert_to_windsurf,
)
from kdesk.converters.shared import (
    get_all_universal_agents,
    validate_tools_manifest,
)
from kdesk.converters.standard import convert_new_platform
from kdesk.converters.writer import (
    prune_platform_dir,
    save_agent,
    write_platform_meta,
)


def convert_all(platforms: List[str], output_dir: Path):
    """Convert all universal agents to specified platforms"""
    agents = get_all_universal_agents()
    print(f"Found {len(agents)} universal agents")

    converters = {
        "claude_code": convert_to_claude_code,
        "cursor": convert_to_cursor,
        "github_copilot": convert_to_copilot,
        "windsurf": convert_to_windsurf,
        "opencode": convert_to_opencode,
        "generic": convert_to_generic
    }

    for platform in platforms:
        print(f"\nConverting to {platform}...")
        counts = {"agents": 0, "skills": 0, "errors": 0}
        written: set = set()

        for agent in agents:
            try:
                if platform in converters:
                    converted = converters[platform](agent)
                elif platform in NEW_PLATFORMS:
                    converted = convert_new_platform(platform, agent)
                else:
                    print(f"Unknown platform: {platform}")
                    break
                path = save_agent(converted, platform, output_dir)
                if path:
                    written.add(path.resolve().as_posix())
                rel = str(agent.get('file_path', '')).replace('\\', '/')
                if "/skill/" in rel or rel.endswith("-skill.yaml"):
                    counts['skills'] += 1
                else:
                    counts['agents'] += 1
            except Exception as e:
                counts['errors'] += 1
                print(f"  [ERR] {agent['name']}: {e}")

        pruned = prune_platform_dir(platform, output_dir, written)
        write_platform_meta(platform, output_dir, counts)
        print(f"  Done: {counts['agents']} agents, {counts['skills']} skills, "
              f"{counts['errors']} errors, {pruned} orphan files pruned")


def create_registry(agents: List[Dict[str, Any]], output_dir: Path):
    """Create registry.yaml for all agents"""
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat() + "Z",
        "total_agents": len(agents),
        "agents": []
    }

    for agent in agents:
        registry['agents'].append({
            "name": agent['name'],
            "display_name": agent.get('display_name', agent['name']),
            "category": agent.get('category', 'uncategorized'),
            "subcategory": agent.get('subcategory', ''),
            "description": agent['description'],
            "version": agent.get('version', '1.0.0'),
            "tags": agent.get('tags', []),
            "platforms": list(agent.get('platforms', {}).keys()),
            "checksum": agent.get('checksum', ''),
            "file_path": agent.get('file_path', '')
        })

    registry_path = output_dir / "registry.yaml"
    with open(registry_path, 'w', encoding='utf-8') as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)
    print(f"\nRegistry created: {registry_path}")


def validate_agents():
    """Validate all universal agents against schema"""
    agents = get_all_universal_agents()
    errors = []

    required_fields = ['name', 'display_name', 'category', 'description', 'version']

    for agent in agents:
        for field in required_fields:
            if field not in agent:
                errors.append(f"{agent.get('name', 'unknown')}: missing required field '{field}'")

        # Validate capabilities
        for i, cap in enumerate(agent.get('capabilities', [])):
            if 'name' not in cap:
                errors.append(f"{agent['name']}: capability {i} missing 'name'")
            if 'description' not in cap:
                errors.append(f"{agent['name']}: capability {cap.get('name', i)} missing 'description'")

    if errors:
        print("Validation errors:")
        for err in errors:
            print(f"  [ERR] {err}")
        return False

    print(f"[OK] All {len(agents)} agents validated successfully")
    return True


def parse_platforms(values) -> List[str]:
    """Split and validate --platforms values: comma- and/or space-separated, or 'all'.

    Returns the platform list; 'all' expands to every platform. Raises ValueError
    on unknown platform names.
    """
    platforms: List[str] = []
    for value in values:
        platforms.extend(p.strip() for p in value.split(",") if p.strip())
    unknown = [p for p in platforms if p not in ALL_PLATFORMS and p != "all"]
    if unknown:
        raise ValueError(f"unknown platform(s): {', '.join(unknown)}")
    if "all" in platforms:
        return list(ALL_PLATFORMS)
    return platforms


def main():
    parser = argparse.ArgumentParser(description="Universal Agent Converter")
    parser.add_argument("--platforms", "-p", nargs="+",
                        default=["all"],
                        help="Target platforms: comma-separated, space-separated, or 'all' "
                             "(e.g. --platforms claude_code,cursor,opencode)")
    parser.add_argument("--output", "-o", default="platform-agents", help="Output directory")
    parser.add_argument("--validate", action="store_true", help="Only validate agents")
    parser.add_argument("--registry", action="store_true", help="Generate registry")
    parser.add_argument("--universal-dir", default="universal-agents", help="Universal agents directory")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-file output")

    args = parser.parse_args()

    cfg.UNIVERSAL_DIR = Path(args.universal_dir)
    cfg.QUIET = args.quiet
    output_dir = Path(args.output)

    if args.validate:
        validate_agents()
        return

    try:
        platforms = parse_platforms(args.platforms)
    except ValueError as e:
        parser.error(f"{e} (choices: {', '.join(ALL_PLATFORMS + ['all'])})")

    manifest_errors = validate_tools_manifest()
    if manifest_errors:
        print("tools.json validation failed:")
        for err in manifest_errors:
            print(f"  [ERR] {err}")
        sys.exit(2)

    agents = get_all_universal_agents()
    print(f"Loaded {len(agents)} universal agents")

    if args.registry:
        create_registry(agents, Path(args.output))

    convert_all(platforms, output_dir)

    print(f"\n[OK] Conversion complete! Output: {output_dir}")
