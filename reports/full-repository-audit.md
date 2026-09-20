# Kdesk-Catalog Full Repository Audit

**Generated:** 2026-08-13 · **Method:** manual forensic audit (PowerShell inventory + source inspection)

> **Note:** This is a historical audit report from the initial pipeline setup. Metrics (e.g., "608 agents wired", "4,237 links") reflect the state at that time and may not match the current catalog. For current metrics, see `reports/catalog-stats.json` and `README.md`.

## 1. Repository State

- **Git:** branch `main`, **0 commits**, **0 tracked files** — everything is untracked. `platform-agents/`, `agents/`, `skills/*`, `workflows/` are gitignored (regenerable artifacts).
- **CI:** none. `.github/` contains only `ISSUE_TEMPLATE` — a `.github/workflows/ci.yml` must be created.
- **No `docs/` directory exists yet** — required for architecture/matrix/support docs.

## 2. File Inventory (excluding `.git`)

| Directory | Files | Contents |
|-----------|-------|----------|
| `universal-agents/` | 5,818 | 2,909 YAML + 2,909 JSON (source of truth) |
| `agents/` | 3,532 | 1,766 YAML + 1,766 JSON (byte-identical copies) |
| `skills/` | 2,288 | 1,144 YAML + 1,144 JSON (incl. `wiring-overrides.yaml`, `wiring.json`) |
| `workflows/` | 1,766 | 1,766 `*.workflow.json` (one per agent) |
| `platform-agents/` | 130,955 | 45 platform dirs × ~2,909–2,911 files |
| `scripts/` | 42 | 36 `.py` + `__pycache__` |
| `tests/` | 14 | 4 test files + `__init__.py` + `__pycache__` |
| `archive/` | 38 | Collapsed shells (git-tracked, recoverable) |
| `reports/` | 3 | `merge-candidates.md`, `merge-candidates-v2.md`, `SUBAGENT-VERIFICATION-REPORT.md` |
| `schemas/` | 1 | `universal-agent.schema.json` |
| `.github/` | 0 | `ISSUE_TEMPLATE` only |
| **Total** | **144,426** | |

**Extensions:** `.md` 119,318 · `.json` 10,495 · `.yaml` 8,775 · `.mdc` 5,818 · `.py` 40 · `.pyc` 16 · `.gitignore` 2 · no-ext 2 · `.TAG` 1 (`.pytest_cache/CACHEDIR.TAG`).

## 3. Source of Truth (universal-agents/)

- **2,909 YAML definitions: 1,766 agents + 1,143 skills** (schema: 0 violations; names unique).
- Two coexisting layouts:
  - Nested: `universal-agents/<family>/agent|skill/<name>.yaml` — 831 agents + 278 skills (1,109 files).
  - Flat: `universal-agents/<family>/*.yaml` — 1,800 files; skills identified by `*-skill.yaml` suffix (est. 935 agents + 865 skills).
- JSON mirrors (2,909) are lossless `definition-v1` with `conversion` provenance blocks.

## 4. Platforms (45)

Six legacy formats (`claude_code`, `cursor`, `github_copilot`, `windsurf`, `opencode`, `generic`) plus 39 new-ecosystem platforms in five families:

- **Agent Skills `SKILL.md` (23):** codex_cli, gemini_cli, antigravity, devin, zed, cline, roo_code, kilo_code, trae, qwen_code, kiro, junie, zencoder, amp, factory_droid, crush, mcpjam, mux, pi, qoder, codebuddy, commandcode, neovate
- **Rules `.md`/`.mdc` (7):** grok_build, amazon_q, augment, firebase_studio, continue, tabnine, supermaven
- **Special (3):** goose (recipes), aider (conventions), openhands (microagents)
- **Single-file (5):** google_jules, warp, codegpt, cody, firebender
- **Deprecated (1):** void (fragments only, no native file)

## 5. Pipeline

`universal-agents/` YAML → (L1 renames, L3 collapse) → `yaml-to-json.py` → `agents/` + `skills/` JSON → `workflows/` → `wire-skills.py` (wiring.json) → `universal-converter.py` → `platform-agents/`.

Verified state (CONVERSION-REPORT.md, 2026-08-11): 0 conversion errors, 0 schema violations, 4,234 converter warnings (down from 5,564).

## 6. Skills Wiring

- **608 agents wired → 470 skills via 4,237 links** (4,231 evidence + 6 manual overrides).
- 1,090/1,143 skills carry tool evidence; 53 skill families lack evidence (conceptual); 1,158 unwired agents use only generic CLIs.

## 7. Tests

- `pytest tests`: **115 passed, 3 skipped** (~1–8 min depending on cache/warmth; the platform-spec suite dominates). Skips: codegpt/cody/firebender native-file tests (not assembled yet).
- Test files: `test_converter_cli.py`, `test_platform_spec.py`, `test_wire_skills.py`, `test_yaml_to_json.py`, `test_kdesk_*.py`.

## 8. Stale Documentation (fixed 2026-08-13)

All stale numbers refreshed: README platform-files 158,313→130,954; wiring counts
verified against `skills/wiring.json`; AGENTS.md 46→45 platforms; schema description
1,804→1,766 agents; `scripts/validate-conversion.py` header 1,804→1,766.
Remaining: none.

## 9. Portability Issues (fixed)

- All hard-coded `<repo-root>\...` paths removed from `scripts/` (grep = 0 matches); root is derived from `__file__`/`Path(__file__).resolve().parents[1]`.
- `verify-install.py` dead placeholder logic removed.
- Report generators guard zero-file false-success (`guard_zero` in `scripts/generate-reports.py`).

## 10. Known Content Limits (honest, measured)

- No agent declares `skills` references in source YAML — wiring is evidence-derived and provenance-marked.
- 1,267 items have no capability parameters; 1,866 have no prerequisites/dependencies; no `outputs` anywhere; 62 skills have no commands.
- Content ~95% template-generated; curation (L1–L3) is evidence-gated, not human-perfect. 204 near-duplicate families (≥85% similar descriptions) remain cleanup candidates (see `reports/duplicate-report.json`).

## 11. Next Steps

1. ~~Fix stale docs (README, AGENTS.md, schema description).~~ DONE
2. ~~Fix hard-coded paths; add zero-file false-success guard.~~ DONE
3. ~~Create `docs/ARCHITECTURE.md`, `docs/platform-matrix.md`, authoring/support docs.~~ DONE
4. ~~Create `.github/workflows/ci.yml`.~~ DONE
5. ~~Implement `kdesk` package (models, registry, capability model, adapters, graph, workflow engine, installer, doctor, security, provenance, license, quality, duplicates).~~ DONE
6. ~~Generate the remaining required reports and final implementation summary.~~ DONE