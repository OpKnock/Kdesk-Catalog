# AGENTS.md

Guidance for AI agents working in this repository.

## What this repo is

A conversion catalog: `universal-agents/` holds platform-neutral YAML definitions
(agents and skills, 2,900+ files) that are converted into per-platform artifacts
under `platform-agents/` (45 platforms: Claude Code, Cursor, GitHub Copilot,
Windsurf, OpenCode, Goose, OpenHands, single-file rule platforms, and more).

## Key commands

```bash
# Convert all platforms (slow: ~15 min, ~130k output files)
python scripts/universal-converter.py --platforms all --quiet

# Convert a single platform (fast)
python scripts/universal-converter.py --platforms windsurf --quiet

# Validate all source YAMLs without writing output
python scripts/universal-converter.py --platforms all --validate

# Schema-check source YAMLs (0 violations required)
python scripts/schema-check.py

# Regenerate JSON definitions (agents/, skills/, workflows/) from YAML
python scripts/yaml-to-json.py

# Regenerate per-platform marketplace manifests + report
python scripts/generate-marketplaces.py

# Validate marketplaces are in sync with the definitions
python scripts/generate-marketplaces.py --validate

# Full test suite (platform-spec, converter CLI, yaml-to-json, wire-skills)
pytest -q tests
```

## Conventions that must not be violated

- **No stale model IDs.** Never write hardcoded models like
  `claude-3-5-sonnet-20241022`, `claude-3.5-sonnet`, or `gpt-4` into platform
  configs. The portable default is `inherit` (or omit the `model` key, as in
  Cursor `.mdc`, which has no real model field). Run
  `python scripts/fix-stale-model-ids.py --dry-run` to verify.
- **No orphan outputs.** `universal-converter.py` prunes files in
  `platform-agents/` that no longer map to a source YAML; keep it that way.
- **Marketplaces mirror the definitions.** `marketplaces/*.marketplace.json`
  list the full catalog (every definition converts to every platform);
  `generate-marketplaces.py` output is deterministic and validated with
  `--validate`. Workflows are platform-neutral and not listed.
- **Agent format**: YAML with `name`, `display_name`, `description`, `platforms`
  map. Skills live under `universal-agents/<category>/skill/<name>.yaml`.
- **Frontmatter contracts** (enforced by `tests/test_platform_spec.py`):
  - Claude Code: `.md` agents with `model: inherit`; skills in
    `.claude/skills/<name>/SKILL.md`.
  - Cursor/Firebase Studio: `.mdc` with `description`, `globs`, `alwaysApply`
    only — no `model`, no `rule_type`.
  - GitHub Copilot: `.github/instructions/*.instructions.md` with `applyTo`.
  - Goose: `recipes/*.yaml` (title/description/instructions).
  - OpenHands: `microagents/*.md` with `type: repo` (or `knowledge` — knowledge
    agents must carry non-empty `triggers`).
- File naming: lowercase with hyphens (e.g. `python-reviewer.yaml`).
- No code comments unless asked.

## Testing

- `tests/test_platform_spec.py` — per-platform output format contract + orphan
  and stale-model sweeps. Slow (~2 min); the full-catalog sweeps skip unless
  `KDESK_FULL=1` is set; do not add full-catalog scans.
- `tests/test_converter_cli.py` — platform parsing.
- `tests/test_yaml_to_json.py` — definition generation.
- `tests/test_wire_skills.py` — skill wiring.
- `tests/test_marketplaces.py` — marketplace manifests (fast structural checks).
- `tests/test_divisions.py` — divisions manifest + check-catalog gate.

## Editing emitters

All emitters live in `scripts/universal-converter.py` (`convert_to_*` /
`convert_new_platform`). After changing an emitter, regenerate that platform
with `--platforms <name>` and run `pytest tests/test_platform_spec.py -v`.
