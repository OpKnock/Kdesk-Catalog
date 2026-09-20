# Kdesk-Catalog Conversion Report

**Generated:** 2026-08-11 · **Tools:** `scripts/yaml-to-json.py` + `scripts/validate-conversion.py`

> **Note:** This is a historical conversion report from the initial migration. Metrics (e.g., "631 agents wired", "2,947 YAML definitions") reflect the state at that time and may not match the current catalog. For current metrics, see `reports/catalog-stats.json` and `README.md`.

## Summary

| Item | YAML (source) | JSON | Workflows |
|------|---------------|------|-----------|
| **Agents** | 1,766 | 1,766 | 1,766 |
| **Skills** | 1,143 | 1,143 | — |
| **Total** | 2,909 | 2,909 | 1,766 |

The `universal-agents/` YAML files are the curated source of truth (see
Anti-Fingerprint Pass below). Byte-identical
copies are stored in the new structure; JSON definitions are generated from the source
originals and validated lossless.

## Directory Structure

```
agents/
  yaml/<category>/...   1,766 files (byte-identical YAML copies)
  json/<category>/...   1,766 files (lossless JSON definitions)
skills/
  yaml/<category>/...   1,143 files (byte-identical YAML copies)
  json/<category>/...   1,143 files (lossless JSON definitions)
workflows/<category>/...  1,766 *.workflow.json files (one per agent)
```

Relative paths mirror `universal-agents/` exactly, so every file traces 1:1 to its
source YAML.

## JSON Definition Format (definition-v1)

Every JSON contains, in order:

- **id** — stable unique ID (the agent/skill `name`, verified unique per type)
- **type** — `agent` or `skill`
- **All original YAML top-level keys, verbatim** (name, display_name, category,
  subcategory, description, version, tags, author, license, capabilities, knowledge,
  instructions, examples, platforms, created_at, updated_at, type, keywords,
  prerequisites, tools — whatever exists in the source file)
- **skills** — explicit agent→skill references from the YAML (`[]` when the source
  has none — see Warnings)
- **tools** — from the source's explicit `tools` key, else `platforms.claude_code.tools`
  (real data; provenance recorded)
- **inputs** — `{"parameters": [...]}` derived only from capability `parameters`
  blocks (name/type/description + owning capability); `{}` when absent
- **outputs** — `{}` (the source YAML defines no outputs; nothing invented)
- **dependencies** — from the source's `prerequisites`/`dependencies` key (`[]` when absent)
- **conversion** — provenance block: source YAML path, tool, schema, and the
  derived-field source for every filled field (nothing invented is untraceable)

## Workflow Format (workflow-v1)

One workflow per agent:

```json
{
  "id": "wf-<agent-id>",
  "type": "workflow",
  "name": "<Display Name> Workflow",
  "version": "<agent version>",
  "agent": "<agent-id>",
  "description": "...",
  "input": {"parameters": [...]},
  "steps": [
    {"id": "step-N-load-skill-<id>", "type": "skill", "skill": "<skill-id>"},
    {"id": "step-N-agent", "type": "agent", "agent": "<agent-id>", "input": "{{input}}"},
    {"id": "step-N-capability-<slug>", "type": "capability",
     "capability": "<cap name>", "tool": "<first CLI tool>", "requires": "step-N-agent"}
  ],
  "output": {"result": "{{<last-step>.output}}"}
}
```

Design rules:

- Steps reflect **real source data only**: one capability step per capability in the
  original YAML's order; skill-load steps only for skills the agent actually references
  (none do today); the agent step delegates to the existing agent definition instead of
  duplicating it.
- Inputs/outputs are wired by reference ({{input}}, {{step.output}}) per the requested
  convention.
- No branches, conditions, loops, parallel execution, retries, or delegation are
  represented because **the source YAML defines none** — nothing was invented.

## Validation Results

| Check | Result |
|-------|--------|
| V1  Agents: YAML copy + JSON for all 1,766 | PASS |
| V2  Skills: YAML copy + JSON for all 1,143 | PASS |
| V3  Workflows for all 1,766 agents | PASS |
| V4  All JSON files parse (3,727) | PASS |
| V5  Agent IDs unique / Skill IDs unique / Workflow IDs unique | PASS |
| V6  Agent→Skill references all resolve (0 references exist in source) | PASS (none to resolve) |
| V7  Workflow→Agent references all resolve | PASS |
| V8  Key+value preservation: every original YAML key present with identical value | PASS (100%) |
| V9  Derived fields never invented (inputs == capability parameters count, etc.) | PASS |
| V10 No files skipped, none extra (manifest match 1:1) | PASS |
| V11 YAML copies byte-identical (SHA-256) | PASS |
| V12 Wiring manifest OK (631 agents, 4,534 links) | PASS |

## Errors, Missing References, Duplicates, Invalid Files

- **Conversion errors:** 0
- **Missing references:** 0
- **Duplicate IDs:** 0 (agents / skills / workflows)
- **Invalid files:** 0

## Warnings

1. **No agent declares skill references in source YAML** — the YAML has no `skills` key
   (verified across all 2,909 files post-curation). Agent `skills` arrays are empty by
   default; derived links come only from the wiring manifest (`provenance` marked).
2. **1,544 → 1,267 items have no capability parameters** — `inputs` is `{}`. The
   gap narrowed via `scripts/extract-parameters.py`: 262 files gained parameters
   promoted strictly from their own commands (flags with ≥2 uses for `--long`,
   ≥4 for `-x`, artifact/`--agent`/`--help`/`--version` excluded; type inferred
   from the value that actually follows the flag). The rest have no flags in
   their commands, so nothing observable exists to promote.
3. **2,669 → 1,866 items have no prerequisites/dependencies after skill-tools
   extraction; the 803 skills that gained `prerequisites` are now mapped into
   dependencies** — remaining empties are agents with no tools and the 62 command-less
   skills. (`dependencies` is `[]` for them.)
4. **No `outputs` anywhere in the source** — `outputs` is `{}` in all JSONs and workflow
   outputs reference step outputs by convention.

## Skills Wiring (skills/wiring.json)

Separate manifest of agent→skill links, generated by `scripts/wire-skills.py`:

- **Rule (no invention):** a link exists only when tool evidence aligns — exact match of
  tokens from the agent's capability commands (first word per command) against tokens
  from the skill's own `tools`/`prerequisites` declarations.
- **Rarity weighting:** score = sum(1/token-frequency across declaring skills); links are
  kept when score ≥ 0.15 *or* ≥ 2 distinct tokens match. Generic CLIs (`curl`, `aws`,
  `gcloud`, `docker`, `kubectl`, `helm`, `python`, `node`, `git`, `npm`, `npx`, ...) count
  as weak evidence alone, so one shared `aws`/`python` invocation never fabricates a link.
- Block-style YAML label words (first word ending in `:`) are excluded.
- **Result:** 631 agents wired to 465 skills via 4,534 links — 4,528 evidence-backed plus
  6 manual overrides (post-curation corpus). 1,161 agents remain unwired because their
  commands share no token with any skill's declared tools.
- **Skill-side evidence widening (`scripts/extract-skill-tools.py`):** 803 of the 861
  skills that declared no `tools`/`prerequisites` had their real command binaries
  extracted as `prerequisites` (first word per command, same tokenizer as the agent
  side, labels/noise excluded). 62 skills have no commands at all and stay unwired.
  This raised skill tool evidence from 278 to 1,081 skills and wired agents from 419 to
  631 — still zero invented links, because every new prerequisite is a binary the
  skill's own commands actually invoke.
- **Usage:** run `extract-skill-tools.py --apply` and `wire-skills.py` first, then the converter with `--wiring skills/wiring.json`
  to merge links into agent JSONs (skills array + provenance) and to emit `load-skill`
  steps in workflows. Validated by check V12: every wired agent/skill id resolves, links
  are unique, evidence is present, and agent JSON skills match the manifest.

**Fidelity note:** wiring is provenance-marked (`conversion.derived.skills: "wiring (skills/wiring.json)"`)
so manifest-derived references are never confused with source-YAML references.

## Curated Overrides (skills/wiring-overrides.yaml)

Evidence wiring can never reach skills that declare no `tools`/`prerequisites`
without real command evidence (after extraction only 62 such skills remain — the
tool-less skill set). Curated, hand-verified links live in the
**committed** YAML file (`agents: {id: [skill-id...]}`); `wire-skills.py` merges them into
the manifest with `manual: true`, never duplicating evidence links, and fails loudly on
unknown agent/skill ids. Example: `api-async-agent` is manually wired to the 6 asyncapi
skills, which declare no tools. 6 manual links are in effect (631 wired agents,
4,534 total links). V12 accepts manual links without evidence but requires the flag.

## Machine-Checkable Format (schemas/universal-agent.schema.json)

JSON Schema (Draft 2020-12) describing both observed YAML shapes (metadata-rich and
tool-annotated). `schema-check.py` validates all 2,909 source files: **0 violations**.
Examples are `{input, output}` objects or strings; knowledge items have three observed
key sets, all covered.

## Hygiene Reports (scripts/catalog-hygiene.py)

- `dedup` — groups skill names by normalized family (role/v2+ suffixes stripped):
  **74 duplicate-name families** among 1,143 skills (e.g. `api-analytics-*` x6,
  `api-auth-*` x6). Cleanup candidates, not an automatic action.
- `gaps` — per-category counts of items lacking capability parameters (1,267 after
  `extract-parameters.py` promoted real flags from commands),
  prerequisites/tools (2,669 — 803 skill-side gaps since closed by
  `extract-skill-tools.py`), examples (9), and knowledge (0 — all items carry knowledge).

## Anti-Fingerprint Pass (L1–L3)

Generated names followed generator combinatorics (`api-auth-v4`, `ml-langchain-deploy-sdk-agent`).
Fingerprint measurement before acting (all numbers measured on the corpus, not assumed):

- **Content dupes:** zero full-document duplicates; 15 files had identical instructions (7 groups).
- **Skeleton dupes:** 6 skeleton groups / 13 files; 2,940/2,947 skeletons unique.
- **Name signals:** 190 names with `-vN`, 425 with `-deploy`/`-deploy-sdk` tails.
- **"You are an expert" opener claim: 0 files** (openers are diverse); no colon-prefixed
  description word pool — the third-party critique's fingerprints (1) and (3) do not match
  this corpus; the name combinatorics (2) did.

### L1 — content-derived renames (`scripts/catalog-rename.py`)

- Renames `-vN` and combinatorial tail stacks (`-deploy-sdk`, `-server-agent`, `-sdk-agent`,
  `-rag-agent`, `-inference-server`, …) into names derived from each file's own content:
  family subject stem + role words from real capability names, command labels, or command
  tools — never invented words.
- **582 files renamed** (plus 5 collision repairs): `api-auth-v2..5` → `api-auth-jwt`,
  `api-auth-oidc`, `api-auth-keys`, `api-auth-mtls`; `ml-langchain-deploy-sdk` →
  `langchain-sdk`; 190 `-vN` names eliminated (0 remaining).
- Folder (old-layout `api-auth-v4/skill/…` → `api-auth-jwt/skill/…`), `prompt_file`,
  `plugin`, `system_prompt`, and knowledge titles updated in lockstep. Run with `--apply`.
- 19 files in the flat `api/` layout that carried the skill identity only in their
  `-skill.yaml` filename had the suffix restored (`express-routing-skill.yaml`) so every
  classifier's path-based skill detection stays intact.

### L3 — evidence-gated collapse (`scripts/catalog-collapse.py`)

- Merge predicate (no fabrication): command-set overlap ≥ 0.7 **and** instruction token
  Jaccard ≥ 0.55 **and** quality-score gap ≤ 3, same category, same family (first two
  subject words). Verified by hand on samples: the `langchain-*` trio share an identical
  docker/kubectl/helm deploy shell (sim 0.84) — merged; `langchain-python` vs
  `langchain-python-sdk` (sim 0.13) — kept apart.
- **12 L3 + 4 curated + 22 family-twin shells archived (38 total; all under archive/)** (survivor = highest content score), all thin ML deploy
  shells whose only difference was `--agent <name>` inside an otherwise identical command
  list. `archive/` is git-tracked and recoverable.
- Below the auto bar the corpus is genuinely non-duplicate (pairwise command overlap ≈ 0
  for >3,000 family pairs; instruction Jaccard median ≈ 0.2 even within name families),
  so the remaining reduction is a **human curation task**: `reports/merge-candidates.md`
  ranks the closest pairs for review. Script-forced collapse to 300–400 would cancel real
  content; that target is honest only via the curated route.

### L2 — structural stance

- L2 (shape randomization / voice variation) was deliberately **not** executed as
  rewriting: varying capability counts, parameter sets, or instruction phrasing to "look
  organic" is content fabrication that would also falsify the corpus's provenance.
  Structure was varied through the honest levers: L1 names, L3 merges, and the
  1–5-capability / 0–6-parameter / 2–10-command variation already present in the data.
- Uniform fields (identical `created_at`, identical per-platform model pins) are format
  defaults, not data claims; they are preserved as-is to keep the machine-readable
  contract (schema + V9) stable.

### Post-curation numbers

- 2,909 sources (1,766 agents + 1,143 skills); names unique (0 collisions), all parse.
- Pipeline regenerated: extract-skill-tools (803 prerequisites) → wire (**631 wired /
  4,534 links** + 6 manual) → convert (**0 errors / 4,234 warnings**, down from 5,564)
  → validate (**0 errors / 0 warnings**) → schema (**0 violations**) → 27 tests green.
