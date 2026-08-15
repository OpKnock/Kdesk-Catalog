#!/usr/bin/env python3
"""
Assemble single-file platforms from per-item instruction fragments + manifest.

Reads platform-agents/<platform>/manifest.yaml and builds the real native file
each tool expects (schemas verified against each tool's own documentation):
  - google_jules -> AGENTS.md (Markdown, category-grouped, capped ~450 lines)
  - warp -> WARP.md (Markdown, category-grouped, capped ~450 lines)
  - codegpt -> AGENTS.md (Markdown, category-grouped, capped ~450 lines;
                          CodeGPT documents AGENTS.md at repo root - docs.codegpt.co)
  - cody -> .vscode/cody.json (Custom Commands: {"commands": {name: {description, prompt}}})
  - firebender -> .firebender/agents/*.md (YAML frontmatter: name/description) +
                  firebender.json ({"agents": [".firebender/agents/<slug>.md", ...]})
  - void -> NOT assembled: voideditor/void is deprecated and no agent-instructions
            config is documented (.void/config.json is only the CLI OAuth token cache)

The former .tabnine.yaml / .supermaven/config.json / .cody/config.json /
.codegpt/config.json targets were disproven by research:
  - Tabnine reads .tabnine/guidelines/*.md plain markdown (docs.tabnine.com)
  - Supermaven reads .supermaven/rules/*.md plain markdown (docs.supermaven.com)
Those two now live in NEW_RULES_PLATFORMS in universal-converter.py instead.
"""
import json
import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
PLATFORM_AGENTS = ROOT / "platform-agents"
UNIVERSAL_AGENTS = ROOT / "universal-agents"

SINGLE_FILE_PLATFORMS = {
    "google_jules": "AGENTS.md",
    "warp": "WARP.md",
    "codegpt": "AGENTS.md",
    "cody": ".vscode/cody.json",
    "firebender": "firebender.json",
    "void": None,  # deprecated, no documented agent-instructions file
}

# Category order for consistent output
CATEGORY_ORDER = [
    "security", "api", "backend", "devops", "database", "data", "ml",
    "testing", "code-quality", "frontend", "infrastructure", "cloud",
    "monitoring", "mobile", "compliance", "sre", "finops", "patterns",
    "networking", "messaging", "devtools", "infra"
]

MAX_ITEMS_PER_CATEGORY = 30
MAX_TOTAL_ENTRIES_JSON = 500
MAX_LINES_MARKDOWN = 450

def load_universal_catalog():
    """Load all universal agents with their categories and types."""
    catalog = {}
    for yaml_file in UNIVERSAL_AGENTS.rglob("*.yaml"):
        if yaml_file.name == "registry.yaml":
            continue
        try:
            agent = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or {}
            name = agent.get("name")
            if not name:
                continue
            rel = str(yaml_file.relative_to(UNIVERSAL_AGENTS)).replace("\\", "/")
            is_skill = "/skill/" in rel or rel.endswith("-skill.yaml")
            cat = str(agent.get("category", "uncategorized")).lower()
            catalog[name] = {"category": cat, "is_skill": is_skill, "rel": rel}
        except Exception:
            continue
    return catalog

UNIVERSAL_CATALOG = load_universal_catalog()

def load_manifest(platform: str) -> dict:
    """Load manifest.yaml for a platform."""
    manifest_path = PLATFORM_AGENTS / platform / "manifest.yaml"
    if not manifest_path.exists():
        return {}
    return yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

def load_instruction_files(platform: str) -> list:
    """Load all instruction fragment files for a platform in manifest order."""
    manifest = load_manifest(platform)
    files = manifest.get("instruction_files", [])
    if not files:
        # Fallback: glob instructions/*.md
        files = sorted(
            f.name for f in (PLATFORM_AGENTS / platform / "instructions").glob("*.md")
        )
    items = []
    for rel in files:
        fpath = PLATFORM_AGENTS / platform / rel
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        name = fpath.stem
        # Get category from catalog
        cat_info = UNIVERSAL_CATALOG.get(name, {})
        category = cat_info.get("category", "uncategorized")
        is_skill = cat_info.get("is_skill", False)
        items.append((name, content, category, is_skill))
    return items

def group_by_category(items: list) -> dict:
    """Group items by category."""
    groups = defaultdict(list)
    for name, content, category, is_skill in items:
        groups[category].append((name, content, is_skill))
    return groups

def truncate_for_budget(text: str, max_lines: int = MAX_LINES_MARKDOWN) -> str:
    """Truncate to line budget, keeping complete sections."""
    lines = text.split("\n")
    if len(lines) <= max_lines:
        return text
    kept = []
    current = 0
    for line in lines:
        if current + 1 > max_lines:
            break
        kept.append(line)
        current += 1
    kept.append("\n... (truncated for size budget — see per-category SKILL.md files for full detail)")
    return "\n".join(kept)

def first_desc_line(content: str) -> str:
    """One-line summary: first non-heading, non-frontmatter line."""
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
            return stripped[:120]
    return ""

def build_markdown_assembly(platform: str, items: list) -> str:
    """Build category-grouped Markdown for AGENTS.md / WARP.md."""
    groups = group_by_category(items)
    
    parts = []
    platform_title = platform.replace("_", " ").title()
    parts.append(f"# {platform_title} — Agent & Skill Catalog")
    parts.append("")
    parts.append(f"> Generated from Kdesk-Catalog universal source. See `platform-agents/{platform}/instructions/` for per-item files.")
    parts.append("")
    
    # Commands section
    parts.append("## Quick Commands")
    parts.append("")
    parts.append("```bash")
    parts.append("# Regenerate all platforms")
    parts.append("python scripts/universal-converter.py --platforms all")
    parts.append("")
    parts.append("# Run tests")
    parts.append("python -m pytest tests/")
    parts.append("```")
    parts.append("")
    
    # Categories in order
    total_shown = 0
    for cat in CATEGORY_ORDER:
        if cat not in groups or not groups[cat]:
            continue
        items_cat = groups[cat]
        parts.append(f"## {cat.title()}")
        parts.append("")
        parts.append(f"*{len(items_cat)} agents/skills available — see SKILL.md files for full detail*")
        parts.append("")
        for name, content, is_skill in sorted(items_cat)[:MAX_ITEMS_PER_CATEGORY]:
            desc_line = first_desc_line(content)
            kind = "skill" if is_skill else "agent"
            parts.append(f"- **{name}** ({kind}): {desc_line}")
            total_shown += 1
        if len(items_cat) > MAX_ITEMS_PER_CATEGORY:
            parts.append(f"- … and {len(items_cat) - MAX_ITEMS_PER_CATEGORY} more")
        parts.append("")
    
    return truncate_for_budget("\n".join(parts))

def build_cody_commands(items: list) -> dict:
    """Build Cody Custom Commands (.vscode/cody.json) - capped at MAX_TOTAL_ENTRIES_JSON.

    Verified shape (docs.sourcegraph.com/cody/custom-commands):
    {"commands": {<name>: {"description": <text>, "prompt": <text>}}}.
    """
    commands = {}
    for name, content, category, is_skill in items:
        if len(commands) >= MAX_TOTAL_ENTRIES_JSON:
            break
        commands[name] = {
            "description": first_desc_line(content),
            "prompt": content.strip(),
        }
    return {"commands": commands}

def write_firebender_agents(platform: str, items: list) -> list:
    """Write .firebender/agents/<slug>.md files with YAML frontmatter.

    Verified spec (docs.firebender.com/api-reference/syntax): agent files under
    .firebender/agents/*.md with frontmatter name/description (color/icon/tools/
    model/callable optional), indexed by firebender.json {agents: [...]}.
    """
    agents_dir = PLATFORM_AGENTS / platform / ".firebender" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, content, category, is_skill in items:
        body = content.strip()
        head = f"---\nname: {json.dumps(name)}\ndescription: {json.dumps(first_desc_line(content))}\n---\n\n"
        (agents_dir / f"{name}.md").write_text(head + body + "\n", encoding="utf-8")
        written.append(f".firebender/agents/{name}.md")
    return written

def assemble_platform(platform: str):
    """Assemble the native file(s) for one platform."""
    native_file = SINGLE_FILE_PLATFORMS[platform]
    out_dir = PLATFORM_AGENTS / platform
    
    items = load_instruction_files(platform)
    if not items:
        print(f"  [WARN] {platform}: no instruction files found")
        return
    
    if native_file is None:
        print(f"  [SKIP] {platform}: deprecated / no documented agent-instructions file — fragments kept for reference only")
        return
    
    out_path = out_dir / native_file
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Assembling {platform} -> {native_file} ({len(items)} items)")
    
    if platform in ("google_jules", "warp", "codegpt"):
        content = build_markdown_assembly(platform, items)
        out_path.write_text(content, encoding="utf-8")
    elif platform == "cody":
        commands = build_cody_commands(items)
        out_path.write_text(json.dumps(commands, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif platform == "firebender":
        written = write_firebender_agents(platform, items)
        index = {"agents": written}
        out_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    
    size_kb = out_path.stat().st_size / 1024
    if size_kb > 50:
        print(f"  [WARN] {platform}: {native_file} is {size_kb:.1f}KB (>50KB budget)")
    else:
        print(f"  [OK] {platform}: {native_file} ({size_kb:.1f}KB)")

def main():
    print("Assembling single-file platform native files...")
    for platform in SINGLE_FILE_PLATFORMS:
        try:
            assemble_platform(platform)
        except Exception as e:
            print(f"  [ERR] {platform}: {e}")
    print("Done.")

if __name__ == "__main__":
    main()