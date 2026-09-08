#!/usr/bin/env python3
"""Regenerate platform-agents files for a single universal-agents YAML.

Usage: python scripts/regen-one.py universal-agents/governance/catalog-auditor.yaml
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kdesk.converters.constants import ALL_PLATFORMS, NEW_PLATFORMS
from kdesk.converters.native import (
    convert_to_claude_code, convert_to_copilot, convert_to_cursor,
    convert_to_generic, convert_to_opencode, convert_to_windsurf,
)
from kdesk.converters.shared import load_universal_agent
from kdesk.converters.standard import convert_new_platform
from kdesk.converters.writer import save_agent

CONVERTERS = {
    "claude_code": convert_to_claude_code,
    "cursor": convert_to_cursor,
    "github_copilot": convert_to_copilot,
    "windsurf": convert_to_windsurf,
    "opencode": convert_to_opencode,
    "generic": convert_to_generic,
}

seen, unique = set(), []
for p in ALL_PLATFORMS:
    if p not in seen:
        seen.add(p)
        unique.append(p)

agent = load_universal_agent(Path(sys.argv[1]))
out = ROOT / "platform-agents"
n = 0
for platform in unique:
    if platform == "void":
        continue
    try:
        if platform in CONVERTERS:
            converted = CONVERTERS[platform](agent)
        elif platform in NEW_PLATFORMS:
            converted = convert_new_platform(platform, agent)
        else:
            continue
        if save_agent(converted, platform, out):
            n += 1
    except Exception as e:
        print(f"  [ERR] {platform}: {e}")
print(f"regenerated {n} files for {agent['name']}")
