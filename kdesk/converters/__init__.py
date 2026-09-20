"""kdesk.converters — modular universal agent converter.

Split out of scripts/universal-converter.py:
- constants: platform schemas/families/paths
- shared: loaders, slugify, markdown builders
- native: claude_code/cursor/copilot/windsurf/opencode/generic
- standard: SKILL.md/rules/goose/aider/openhands/singlefile emitters
- writer: save/prune/meta writers
- pipeline: convert_all + CLI entry (main)
"""
from kdesk.converters.constants import (
    ALL_PLATFORMS,
    DEPRECATED_SINGLE_FILE_PLATFORMS,
    NEW_PLATFORMS,
    NEW_RULES_PLATFORMS,
    NEW_SKILL_PLATFORMS,
    OUTPUT_DIR,
    PLATFORM_INFO,
    PLATFORM_SCHEMAS,
    REPO_ROOT,
    SINGLE_FILE_PLATFORMS,
    SPECIAL_PLATFORMS,
    TOOLS_MANIFEST_PATH,
)
from kdesk.converters.shared import (
    build_markdown,
    desc_safe,
    get_all_universal_agents,
    infer_globs,
    load_tools_manifest,
    load_universal_agent,
    slugify,
    validate_tools_manifest,
)
from kdesk.converters.native import (
    convert_to_claude_code,
    convert_to_copilot,
    convert_to_cursor,
    convert_to_generic,
    convert_to_opencode,
    convert_to_windsurf,
)
from kdesk.converters.standard import (
    convert_new_platform,
    convert_to_aider_convention,
    convert_to_goose_recipe,
    convert_to_openhands_microagent,
    convert_to_rules_md,
    convert_to_singlefile,
    convert_to_skill_md,
    openhands_triggers,
)
from kdesk.converters.writer import (
    prune_platform_dir,
    save_agent,
    write_copilot_index,
    write_platform_meta,
)
from kdesk.converters.pipeline import (
    convert_all,
    create_registry,
    main,
    parse_platforms,
    validate_agents,
)

__all__ = [
    "ALL_PLATFORMS", "DEPRECATED_SINGLE_FILE_PLATFORMS", "NEW_PLATFORMS",
    "NEW_RULES_PLATFORMS", "NEW_SKILL_PLATFORMS", "OUTPUT_DIR", "PLATFORM_INFO",
    "PLATFORM_SCHEMAS", "REPO_ROOT", "SINGLE_FILE_PLATFORMS", "SPECIAL_PLATFORMS",
    "TOOLS_MANIFEST_PATH",
    "build_markdown", "desc_safe", "get_all_universal_agents", "infer_globs",
    "load_tools_manifest", "load_universal_agent", "slugify",
    "validate_tools_manifest",
    "convert_to_claude_code", "convert_to_copilot", "convert_to_cursor",
    "convert_to_generic", "convert_to_opencode", "convert_to_windsurf",
    "convert_new_platform", "convert_to_aider_convention",
    "convert_to_goose_recipe", "convert_to_openhands_microagent",
    "convert_to_rules_md", "convert_to_singlefile", "convert_to_skill_md",
    "openhands_triggers",
    "prune_platform_dir", "save_agent", "write_copilot_index",
    "write_platform_meta",
    "convert_all", "create_registry", "main", "parse_platforms",
    "validate_agents",
]
