# Kdesk Support

How to diagnose, verify, and maintain the Kdesk-Catalog platform.

## 1. Health checklist

```bash
python scripts/schema-check.py                                    # schema: 0 violations
python scripts/universal-converter.py --platforms all --validate  # all source YAMLs parse
python scripts/validate-conversion.py                             # 12 conversion checks
pytest -q tests                                 # full suite
kdesk doctor                                                      # per-platform install verification
kdesk provenance verify                                           # every JSON resolves to its YAML
```

## 2. Common problems

### "0 errors" reported on an empty scan

Any checker that scanned 0 files must say so. If a report says 0 errors but also says 0 files scanned, the check is broken — fix the path (see §4), never the report.

### Schema violations after editing YAML

- Run `python scripts/schema-check.py` to see exact file/field.
- Required keys: `name`, `display_name`, `category`, `description`, `version`, `platforms`, `capabilities`, `examples`, `instructions`, `knowledge`.
- Examples are strings or `{input, output}` objects; knowledge items have three observed key shapes — all covered by the schema.

### Wiring manifest errors

- `wire-skills.py` fails loudly on unknown agent/skill ids — run it before `yaml-to-json.py`.
- Manual links must exist in `skills/wiring-overrides.yaml` (`agents: {id: [skill-id...]}`); manual links require no evidence but are provenance-marked.

### Converter warnings (4,234 expected)

Warnings are expected for partially-mapped fields (e.g. platforms without native model fields). Distinguish:

- **Errors (0 allowed):** unparseable YAML, unemittable items.
- **Warnings (expected):** field drops per platform contract (e.g. `model` absent in Cursor `.mdc`).

### Stale model IDs

`python scripts/fix-stale-model-ids.py --dry-run` lists any hardcoded model pins. Portable default is `inherit` (or omit).

## 3. Per-platform verification (doctor)

| Platform | Check |
|----------|-------|
| `claude_code` | `~/.claude/agents/*.md` frontmatter has name/description/tools/model; `~/.claude/skills/*/SKILL.md` has name/description |
| `cursor` | `.cursor/rules/*.mdc` has description/globs/alwaysApply only |
| `github_copilot` | `.github/instructions/*.instructions.md` has applyTo |
| `goose` | `~/.config/goose/recipes/*.yaml` has title/description/instructions |
| `openhands` | `.openhands/microagents/*.md` type repo/knowledge; knowledge has triggers |
| All SKILL.md platforms | `.agents/skills/<name>/SKILL.md` present with frontmatter |

Expected counts per platform: ~2,909 items (+ README/manifest/registry). Doctor reports `OK / MISSING / EXTRA / MALFORMED` with scanned-file counts.

## 4. Portability rules

- **Never hard-code `C:\Users\<user>\...`.** Repo-relative paths: `Path(__file__).resolve().parents[1]`. Home-dir paths: `pathlib.Path.home()` or env var (`KDESK_CLAUDE_DIR`) or `platformdirs`.
- Scripts must run on Windows, macOS, and Linux.
- `platform-agents/`, `agents/`, `skills/*`, `workflows/` are gitignored regenerable artifacts — regenerate, don't commit.

## 5. Regeneration playbook (after curation)

```bash
python scripts/extract-skill-tools.py --apply
python scripts/extract-parameters.py --apply
python scripts/wire-skills.py --agents universal-agents --out skills/wiring.json
python scripts/yaml-to-json.py --agents universal-agents --out . --wiring skills/wiring.json
python scripts/validate-conversion.py
python scripts/schema-check.py
python scripts/universal-converter.py --platforms all --quiet     # ~15 min, 130,955 files
pytest -q tests
```

## 6. Escalation

- Content quality / curation questions: see `reports/merge-candidates*.md` + `CONVERSION-REPORT.md`.
- Pipeline bugs: open an issue with the script name, the failing command, and the full output (never truncated "0 errors" claims).