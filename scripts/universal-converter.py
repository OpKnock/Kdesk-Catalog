#!/usr/bin/env python3
"""
Universal Agent Converter (thin CLI shim).

Implementation lives in kdesk/converters/:
- constants: platform schemas/families
- shared: loaders + markdown builders
- native: claude_code/cursor/copilot/windsurf/opencode/generic
- standard: SKILL.md/rules/goose/aider/openhands/singlefile
- writer: save/prune/meta writers
- pipeline: convert_all + CLI entry

This shim re-exports every public name so the script remains importable as a
module (importlib) with the same attribute surface as before, and runnable
via `python scripts/universal-converter.py`.
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kdesk.converters import (  # noqa: E402,F401
    ALL_PLATFORMS,
    DEPRECATED_SINGLE_FILE_PLATFORMS,
    NEW_PLATFORMS,
    NEW_RULES_PLATFORMS,
    NEW_SKILL_PLATFORMS,
    OUTPUT_DIR,
    PLATFORM_INFO,
    PLATFORM_SCHEMAS,
    SINGLE_FILE_PLATFORMS,
    SPECIAL_PLATFORMS,
    TOOLS_MANIFEST_PATH,
    build_markdown,
    convert_all,
    convert_new_platform,
    convert_to_aider_convention,
    convert_to_claude_code,
    convert_to_copilot,
    convert_to_cursor,
    convert_to_generic,
    convert_to_goose_recipe,
    convert_to_openhands_microagent,
    convert_to_opencode,
    convert_to_rules_md,
    convert_to_singlefile,
    convert_to_skill_md,
    convert_to_windsurf,
    create_registry,
    desc_safe,
    get_all_universal_agents,
    infer_globs,
    load_tools_manifest,
    load_universal_agent,
    main,
    openhands_triggers,
    parse_platforms,
    prune_platform_dir,
    save_agent,
    slugify,
    validate_agents,
    validate_tools_manifest,
    write_copilot_index,
    write_platform_meta,
)

# Module-level aliases kept for backward compatibility with consumers that
# read these attributes after importlib-loading this file.
UNIVERSAL_DIR = Path("universal-agents")
QUIET = False


if __name__ == "__main__":
    sys.exit(main() or 0)
