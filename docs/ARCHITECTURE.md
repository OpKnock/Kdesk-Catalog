# Kdesk-Catalog Architecture

**Version:** 1.1.0 · **Status:** Design baseline for the `kdesk` orchestration layer

## 1. System Overview

Kdesk-Catalog is a **Universal AI Agent + Skill + Workflow Registry and Orchestration Platform**. One canonical source of truth (`universal-agents/`, 2,909 YAML definitions) is validated against a machine-checkable schema, converted losslessly to JSON definitions and workflows, wired into an evidence-backed agent→skill graph, and emitted into **45 platform formats** (Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, generic, plus 39 new-ecosystem platforms).

The new `kdesk` package adds the orchestration layer on top of the existing pipeline: registry querying, capability resolution, graph navigation, workflow execution, installation, and health checks — without touching or duplicating the curated content.

## 2. Architectural Principles

1. **One source of truth.** `universal-agents/` YAML is canonical. `agents/`, `skills/`, `workflows/`, `platform-agents/` are regenerable artifacts (gitignored). Never edit generated output directly.
2. **No invention.** Every derived field carries a `conversion` provenance block tracing it to its source (real CLI commands, declared tools, explicit references). Wiring links exist only when tool-evidence aligns.
3. **Honest support claims.** Platform adapters declare `SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | EMULATED | UNKNOWN` — never claim unverified support.
4. **Concept separation.** Agent, subagent, skill, workflow, tool, MCP, hook, rule, memory, and model are distinct concepts connected only through the capability model.
5. **Everything testable.** Every pipeline stage has unit tests; CI (`.github/workflows/ci.yml`) runs schema check, wiring, conversion validation, and the full test suite.
6. **Portable.** No hard-coded `C:\Users\...` paths; paths derive from the repo (`Path(__file__).resolve().parents[1]`), environment variables, or `platformdirs`.
7. **Never fake success.** A check that scanned 0 files reports 0 files scanned, not "0 errors".

## 3. Data Flow

```
universal-agents/<family>/agent|skill/<name>.yaml     (2,909 source files)
        │  schema-check.py (0 violations)
        ▼
extract-skill-tools.py ──► prerequisites from real command binaries
extract-parameters.py ───► parameters from real CLI flags
wire-skills.py ──────────► skills/wiring.json  (631 agents, 4,534 links)
yaml-to-json.py ─────────► agents/ (1,766) + skills/ (1,143) JSON definitions
        │                  workflows/ (1,766 *.workflow.json)
        ▼
universal-converter.py ──► platform-agents/ (45 platforms, 130,955 files)
        ▼
kdesk registry ──────────► queries, graph, capabilities
kdesk installer ─────────► ~/.claude, ~/.config/goose, .cursor/rules, ...
kdesk doctor ────────────► per-platform install verification
```

## 4. Component Map

| Component | Path | Responsibility |
|-----------|------|----------------|
| Schema | `schemas/universal-agent.schema.json` | Machine-checkable format contract (Draft 2020-12) |
| Source | `universal-agents/` | Curated canonical YAML (2,909) |
| JSON definitions | `agents/`, `skills/` | Lossless `definition-v1` (4,534 JSON) |
| Workflows | `workflows/` | `workflow-v1` (1,766, one per agent) |
| Wiring | `skills/wiring.json` + `wiring-overrides.yaml` | Evidence-backed + manual agent→skill links |
| Converter | `scripts/universal-converter.py` | 45 platform emitters |
| Pipeline scripts | `scripts/*.py` | Curation, extraction, validation, verification |
| **kdesk package** | `kdesk/` | Registry, capability model, adapters, graph, workflow engine, installer, doctor, security, provenance, license, quality, duplicates |
| Reports | `reports/` | Audit, platform matrix, adapter matrix, capability, graph, workflow, install, security, quality, duplicate reports |

## 5. kdesk Package Design

```
kdesk/
├── __init__.py          # version, public API
├── cli.py               # kdesk command-line interface
├── models.py            # Agent, Skill, Workflow, Capability dataclasses
├── registry.py          # load + index + query the catalog (mtime-keyed cache)
├── capabilities.py      # capability extraction, parameter/command indexing
├── graph.py             # agent→skill graph, cycle detection, resolvers
├── resolvers.py         # agent/skill resolution with explanations
├── workflow.py          # workflow-v1 validation + execution (dry-run)
├── runtime.py           # WorkflowRuntime: state machine, event bus, persistence
├── execution.py         # SubagentExecutor, permission engine, validation engine
├── installer.py         # transactional install (manifest / drift / rollback)
├── doctor.py            # install verification, tool detection
├── security.py          # secret scanning, path traversal checks
├── provenance.py        # conversion-provenance verification
├── license.py           # license inventory across definitions
├── quality.py           # content-quality scoring (commands, params, examples)
├── duplicates.py        # duplicate-family detection (evidence-gated)
├── stats.py             # authoritative statistics (single source of truth)
└── adapters/
    ├── __init__.py      # emission: SupportLevel, PlatformAdapter, AdapterRegistry
    │                    # (45 platforms via ADAPTER_SPECS; one registry module,
    │                    #  not one file per platform)
    └── contract.py      # runtime: RuntimeAdapter, invoke_subagent contract,
                         # ClaudeCode / Cursor / Codex adapters
```

### 5.0 Feature Classification

Every documented feature carries an honest status; nothing is claimed that is
not implemented and verified.

| Feature | Status | Evidence |
|---------|--------|----------|
| Schema validation (`schemas/`, `schema-check.py`) | IMPLEMENTED | 2,909 files, 0 violations |
| YAML→JSON conversion (`yaml-to-json.py`, `validate-conversion.py`) | IMPLEMENTED | 12 checks PASS, provenance-verified |
| 45-platform converter (`universal-converter.py`) | IMPLEMENTED | `tests/test_platform_spec.py` |
| Wiring graph (agent→skill, evidence + overrides) | IMPLEMENTED | 608 wired, 4,237 links, 0 cycles |
| Authoritative stats (`kdesk stats`, `kdesk/stats.py`) | IMPLEMENTED | matches `reports/baseline-stats.json` |
| Report freshness gate (`check-report-freshness.py`) | IMPLEMENTED | CI step, non-zero on stale reports |
| Zero-file guard (`verify-all.py`) | IMPLEMENTED | FATAL + exit 2 on 0 files |
| Capability model (`capabilities.py`) | IMPLEMENTED | command/parameter index, tool-binaries inverted index |
| Graph resolvers (`graph.py`, `resolvers.py`) | IMPLEMENTED | direct + transitive traversal, explanations, cycles/orphans |
| Workflow engine (`workflow.py`) | IMPLEMENTED | validate + topo-sort + dry-run/execute; step gates |
| Workflow runtime (`runtime.py`) | IMPLEMENTED | state machine, event bus, approval/validation gates, `RuntimeStore` persistence |
| Platform adapters (emission, `adapters/__init__.py`) | IMPLEMENTED | 45-platform registry, dispatch to verified emitters, `verify()` |
| Platform adapters (runtime, `adapters/contract.py`) | IMPLEMENTED | `detect/verify/invoke_subagent`; claude_code exercised by e2e |
| Installer (`installer.py`) | IMPLEMENTED | manifest, backups, drift detection, rollback, empty-dir pruning |
| Security scanner | PARTIAL | regex-based secret scan; no permission model, no tool risk classes |
| Quality report | PARTIAL | metadata completeness only |
| Doctor | IMPLEMENTED | verdicts OK / MISSING / EMPTY / NOT_GENERATED / UNKNOWN + status_counts |
| Workflow run / runtime orchestration | IMPLEMENTED | run_id, events, sessions, approval + validation gates |
| Resolvers (agent/skill) with explanations | IMPLEMENTED | provenance-marked, evidence-backed |
| Transactional install (manifest/drift/rollback) | IMPLEMENTED | `<base>/.kdesk/` manifest + backups, per-platform rollback |
| End-to-end platform invocation | PARTIAL | claude_code real CLI delegation (shim-verified e2e); cursor/codex return honest `ExecutionError` when CLI missing |
| Bundles (named install groups) | NOT IMPLEMENTED | no bundle data exists in the repo; nothing invented |
| SQLite index | PLANNED | optional; YAML remains canonical |

### 5.1 Domain Models (`models.py`)

- `Agent` — name, display_name, category, subcategory, description, version, tags, capabilities, knowledge, instructions, examples, platforms, created_at, updated_at.
- `Skill` — same core fields; `tools`, `prerequisites`; classified via nested `skill/` path or `*-skill.yaml` suffix or `type: skill`.
- `Capability` — name, description, commands (real CLI), examples, parameters.
- `Workflow` — id (`wf-<agent-id>`), steps (skill-load / agent / capability), input/output wiring by reference (`{{input}}`, `{{step.output}}`).
- `Link` — source agent, target skill, evidence (tokens, score), manual flag.

### 5.2 Capability Model (`capabilities.py`)

Each capability owns real CLI commands whose **first word is a tool binary** (e.g. `kubectl`, `curl`, `python`). The capability model exposes:

- `tool_binaries(capability)` — extracted binaries per capability.
- `parameters(capability)` — declared parameter blocks (name/type/description/default).
- `commands_by_tool(catalog)` — inverted index tool → capabilities for cross-catalog queries.
- Capability compatibility is *evidence*: two capabilities are similar only when their command sets overlap measurably (no fabrication).

### 5.3 Platform Adapters (`adapters/`)

`PlatformAdapter` base (in `adapters/__init__.py`): `name`, `family`, `format`, `install_target`, `support_level`, plus `exists()`, `file_count()`, `items_emitted()`, `verify()`. Support levels:

| Level | Meaning |
|-------|---------|
| `SUPPORTED` | Native format emitted by the verified converter pipeline |
| `PARTIALLY_SUPPORTED` | Format emitted, but some fields are dropped with warnings (e.g. void fragments) |
| `EMULATED` | Content available only through a non-native representation |
| `NOT_SUPPORTED` | No output for this platform/feature |
| `UNKNOWN` | No documented config; nothing claimed |

Initial levels: 44 platforms `SUPPORTED` (emitted by the converter, validated by `tests/test_platform_spec.py`); `void` `PARTIALLY_SUPPORTED` (fragments only, no native file — converter notes "⚠ unverified"). Adapters do not re-emit content; they *dispatch* to the verified emitters and verify output.

Platform lifecycle status (tracked per platform, distinct from support level):
`DEFINITION_GENERATED → CONFIG_INSTALLED → PLATFORM_VALIDATED → RUNTIME_EXECUTED`.
Currently all 45 platforms are `DEFINITION_GENERATED`; `CONFIG_INSTALLED` and
above are only claimed for platforms exercised by the runtime (Phase F).

### 5.4 Graph (`graph.py`)

Nodes = agents + skills; edges = wiring links (evidence + manual, provenance-marked) plus explicit `skills:` references from YAML when present. Resolvers:

- `resolve_agent_skills(agent)` — direct + transitive skill dependencies.
- `resolve_workflow_dependencies(workflow)` — skills/capabilities/agents required by steps.
- `cycles()` — Tarjan SCC detection over the wiring graph (currently acyclic: wiring is tool-evidence derived; verified at build time).
- `orphans()` — skills never referenced; agents with no resolvable skills.

### 5.5 Workflow Engine (`workflow.py`)

`workflow-v1` JSON: id, type, name, version, agent, description, input (parameters), steps (skill-load / agent / capability with `requires` edges), output (references `{{step.output}}`). The engine validates step references, topologically orders steps, and executes them in a **dry-run mode** (validating inputs/outputs against capability parameters) or live via `execute()`.

### 5.6 Runtime + Execution (`runtime.py`, `execution.py`)

`WorkflowRuntime` drives a workflow step-by-step as a state machine (`PENDING → RUNNING → COMPLETED | FAILED`, plus `BLOCKED_APPROVAL`), emitting events (`run_started`, `node_started`, `node_completed`, `node_failed`, `run_completed`, `run_failed`) on an `EventBus` backed by a `Session`. Nodes are input / agent / skill-load / capability / output / validate. Approval gates block agent nodes until `run.approve()`; validation gates retry on failure up to `max_attempts` (honest `FAILED` verdict when exhausted). `RuntimeStore.save/load` persists runs as JSON (`runs/<run_id>.json`).

`SubagentExecutor` delegates real agent nodes via the `invoke_subagent(agent, prompt)` contract; `PermissionEngine` allows/denies tool calls; both are replaceable and verified by e2e tests (compiled `claude.exe` shim for claude_code; honest `ExecutionError` when the CLI is not installed).

### 5.7 Installer + Doctor (`installer.py`, `doctor.py`)

- Installer (`Installer(registry, dry_run, base, home_dir)`) is transactional: copies `platform-agents/<platform>/...` to per-platform targets (`.cursor/rules/`, `~/.claude/agents|skills/`, `.github/instructions/`, `~/.config/goose/recipes/`, `.openhands/microagents/`, …), records every destination as a manifest key (`<base>/.kdesk/install-manifest.json`), snapshots pre-existing content to `<base>/.kdesk/backups/<platform>/<key-digest>.bak`, detects drift (`drift()` compares installed files against source digests), restores previous state (`rollback()`), and prunes empty directories on `uninstall()`. `--target home|project` and `--home <dir>` control destination roots.
- Doctor (`check(platform)`, `summary()`) verifies per-platform: expected file counts, frontmatter contracts (per `tests/test_platform_spec.py`), orphan detection, stale-model sweep; verdicts `OK / MISSING / EMPTY / NOT_GENERATED / UNKNOWN` with scanned-file counts (never "0 errors" on 0 files). `summary()` aggregates `platforms / status_counts / files_scanned / rows`.

### 5.8 CLI (`cli.py`)

Commands: `registry`, `graph`, `stats`, `workflow validate|run`, `resolvers`, `adapters`, `convert`, `install [--target home|project] [--home DIR]`, `uninstall`, `drift`, `status`, `rollback`, `doctor`, `security scan`, `provenance verify`, `quality report`, `license`, `duplicates`, `version`.

Exit codes: `0` success, `1` fatal error (e.g. platform not installed), `2` usage error (parser), `3` problems found (`drift` not clean, workflow validation problems, audit findings — non-zero, CI-safe).

## 6. Security Model

- **Secret scanning:** definitions are scanned for API keys, tokens, passwords, high-entropy strings (patterns for `sk-`, `AKIA`, `ghp_`, `-----BEGIN`, etc.); findings are reported with file/line, never written to logs in full.
- **Path traversal:** any install/emit target must resolve inside the platform's own directory; `..` and absolute escapes rejected.
- **Command injection:** capability commands are treated as data (documented, dry-run only) unless the user explicitly opts into execution.
- **Provenance integrity:** every generated JSON embeds `conversion` (source path, tool, schema); reports verify resolvable source files (no orphan outputs).

## 7. Quality Gates (CI)

1. `schema-check.py` — 0 violations on 2,909 files.
2. `wire-skills.py` — manifest resolves, ids unique, evidence present.
3. `yaml-to-json.py` + `validate-conversion.py` — 12 checks PASS.
4. Full test suite — 285 tests (282 passed, 3 skipped; platform-spec covers all 45 platforms).
5. `kdesk` package tests — registry, graph, workflow, adapters, doctor.
6. Zero-file guard: any checker that scanned 0 files fails loudly.

## 8. Deployment Topology

- **Content:** 2,909 canonical definitions + 45-platform outputs (regenerable).
- **Package:** `kdesk` (Python ≥3.9, stdlib + `PyYAML`; optional `platformdirs`).
- **CLI:** `kdesk registry`, `kdesk graph`, `kdesk stats`, `kdesk workflow validate|run`, `kdesk resolvers`, `kdesk adapters`, `kdesk install [--target|--home]`, `kdesk uninstall`, `kdesk drift`, `kdesk status`, `kdesk rollback`, `kdesk doctor`, `kdesk security scan`, `kdesk provenance verify`, `kdesk quality report`, `kdesk license`, `kdesk duplicates`, `kdesk version`.
- **Reports:** all 11 required reports land in `reports/` (JSON + Markdown pairs).

## 9. Known Limits (honest)

- No agent declares explicit `skills:` references in source YAML; the graph is evidence-derived and provenance-marked (manual overrides: 6 links in `wiring-overrides.yaml`).
- 62 command-less skills cannot be evidence-wired; 1,161 agents use only generic CLIs and stay unwired by design.
- 1,267 items have no capability parameters; `outputs` are `{}` everywhere (nothing invented).
- Content is ~95% template-generated; curation is evidence-gated, not human-perfect (74 duplicate-name families remain as cleanup candidates).
- `codegpt`, `cody`, `firebender` native-file assembly is pending (3 tests skipped).
- End-to-end platform invocation is verified for `claude_code` only (real CLI delegation via compiled shim in e2e; `cursor`/`codex` return honest `ExecutionError` when their CLIs are absent).
- Bundles (named install groups) are not implemented — no bundle data exists in the repo.
- Fresh-install rollback reports `no-backup` (backup captures only pre-existing state at install time).