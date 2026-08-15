"""
fix-stale-model-ids.py

Purge stale / deprecated model IDs from universal-agents source YAMLs
(Fix Prompt 7). Converts hardcoded model pins to the portable 'inherit'
default and drops the Cursor 'model' key entirely (Cursor .mdc has no
real model field to begin with).

Behavior per platform:
  * claude_code.model / windsurf.model -> 'inherit' (was claude-3-5-sonnet-20241022,
    claude-3.5-sonnet, or any hardcoded model pin)
  * cursor.model -> dropped entirely
  * All other platforms are left untouched.

Keeps legit content references (e.g. 'garak --model_name gpt-4o-mini'
in a system prompt) intact - only model keys under 'platforms' are touched.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent / "universal-agents"

STALE_MODELS = {"claude-3-5-sonnet-20241022", "claude-3.5-sonnet", "gpt-4", "gpt-4o"}


def load_yaml(path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def dump_yaml(path, data):
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, default_flow_style=False, sort_keys=False,
                       allow_unicode=True, width=100)


def fix_file(path, dry_run=False):
    """Return (inherited, dropped) counts of model fields changed in one file."""
    data = load_yaml(path)
    platforms = data.get("platforms") or {}
    if not isinstance(platforms, dict):
        return (0, 0)

    inherited = 0
    dropped = 0
    changed = False

    for platform, config in platforms.items():
        if not isinstance(config, dict) or "model" not in config:
            continue
        model = str(config["model"])
        if model == "inherit":
            continue

        if platform == "cursor":
            # Cursor .mdc frontmatter has no real model field - drop it.
            del config["model"]
            dropped += 1
            changed = True
        elif model in STALE_MODELS or model.startswith("claude-"):
            # Any hardcoded Claude pin collapses to the portable default.
            config["model"] = "inherit"
            inherited += 1
            changed = True

    if changed and not dry_run:
        dump_yaml(path, data)
    return (inherited, dropped)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would change without writing")
    args = parser.parse_args()

    files = [p for p in ROOT.rglob("*.yaml") if p.name != "registry.yaml"]
    if not files:
        sys.exit(f"No YAML files found under {ROOT}")

    total_i = total_d = fixed = 0
    for path in files:
        try:
            i, d = fix_file(path, dry_run=args.dry_run)
        except Exception as exc:  # malformed file: report, don't crash
            print(f"SKIP {path}: {exc}", file=sys.stderr)
            continue
        if i or d:
            fixed += 1
            total_i += i
            total_d += d
            verb = "WOULD FIX" if args.dry_run else "fixed"
            print(f"{verb} {path} (inherit x{i}, dropped x{d})")

    mode = "dry run" if args.dry_run else "done"
    print(f"\n{mode}: {fixed} files, {total_i} models -> inherit, "
          f"{total_d} cursor model fields dropped")
    if args.dry_run:
        print("Re-run without --dry-run to apply.")


if __name__ == "__main__":
    main()
