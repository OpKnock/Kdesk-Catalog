# Kdesk Authoring Guide

How to author and contribute agents/skills to Kdesk-Catalog.

## 1. Where things live

| What | Where |
|------|-------|
| Source of truth | `universal-agents/<family>/agent/<name>.yaml` or `universal-agents/<family>/skill/<name>.yaml` |
| Schema | `schemas/universal-agent.schema.json` |
| Manual skill links | `skills/wiring-overrides.yaml` |
| Generated (never edit) | `agents/`, `skills/`, `workflows/`, `platform-agents/` |

## 2. Authoring an agent

Create `universal-agents/<family>/agent/<name>.yaml` with:

```yaml
name: my-awesome-agent        # lowercase, hyphens, unique
display_name: My Awesome Agent
category: devops
subcategory: deployment
description: One-line description
version: 1.0.0
tags: [kubernetes, helm]
capabilities:
  - name: Deploy Helm Chart
    description: Deploys a chart to the cluster
    commands:
      - helm upgrade --install myapp ./chart --namespace prod
    examples:
      - helm upgrade --install myapp ./chart --namespace prod
    parameters:
      - name: namespace
        type: string
        description: Target namespace
        default: default
knowledge:
  - title: Helm docs
    type: documentation
    source: https://helm.sh/docs
    description: Official Helm documentation
instructions: |
  Detailed system prompt for the agent (200+ chars).
examples:
  - usage example
platforms:
  claude_code:
    tools: [Bash, Read, Write, Edit, Glob, Grep]
    model: inherit
```

Rules:

- **Real commands only.** Every command must be a real working CLI command. First word is the tool binary used for wiring evidence. No `your-command`, `<placeholder>`, or template placeholders.
- **No stale model IDs.** Never pin `claude-3-5-sonnet-20241022` etc. Use `inherit` or omit. Verify with `python scripts/fix-stale-model-ids.py --dry-run`.
- **No secrets.** Never commit API keys, tokens, or passwords.
- **Naming:** lowercase with hyphens (`python-reviewer.yaml`). No `-v2`/`-v3` suffixes — content-derived names only.
- **No code comments** unless asked.

Optional personality fields (used by generated marketplaces):

```yaml
color: "#10B981"    # hex accent
emoji: "🚀"          # icon emoji
vibe: pragmatic      # tone descriptor
voice: concise       # voice descriptor
```

## 3. Authoring a skill

Same schema as agents. Skills are placed at `universal-agents/<family>/skill/<name>.yaml` (nested) or as `<name>-skill.yaml` next to agents (flat legacy layout — both are supported).

Skill-specific rules:

- Declare `tools:` or `prerequisites:` with the real binaries the skill invokes — this is what makes the skill wireable to agents (`extract-skill-tools.py` can derive them from commands, but explicit declarations are stronger evidence).
- Skills without any commands (conceptual skills) stay unwired by design — they teach conventions via universal primitives.

### 3.1 Routing descriptions (use when / don't use for)

Every skill description should end with routing guidance so agents pick the right skill and know its neighbors:

```yaml
description: Audits dependencies for known vulnerabilities. Use when scanning a
  dependency tree for CVEs. Don't use for container-image scanning (see
  container-security) or IaC misconfiguration checks (see checkov).
```

- Start with `Use when ...` — the concrete trigger.
- Follow with `Don't use for ... (see <sibling-skill>)` — name a real sibling skill by its `name` field so the pointer resolves.
- Omit the sibling reference only when no sibling exists; a generic exclusion is still better than none.

## 4. Wiring (agent → skill links)

1. Run `python scripts/extract-skill-tools.py --apply` — derives `prerequisites` for tool-less skills from their own commands.
2. Run `python scripts/extract-parameters.py --apply` — promotes real CLI flags into `parameters`.
3. Run `python scripts/wire-skills.py --agents universal-agents --out skills/wiring.json` — evidence-backed links.
4. For manual links (skills with no tool evidence), add to `skills/wiring-overrides.yaml`:

```yaml
agents:
  my-agent: [some-conceptual-skill]
```

5. Regenerate: `python scripts/yaml-to-json.py --agents universal-agents --out . --wiring skills/wiring.json`

## 5. Validating your contribution

```bash
python scripts/schema-check.py                                  # 0 violations
python scripts/fix-stale-model-ids.py --dry-run                 # no stale models
pytest -q tests                                   # full suite green
python scripts/universal-converter.py --platforms claude_code   # regenerate one platform
python scripts/validate-conversion.py                           # 12 checks
```

## 6. Curation passes (don't invent, don't delete)

- `catalog-rename.py --apply` — content-derived renames only (no `-vN`).
- `catalog-collapse.py --apply` — evidence-gated collapse (command overlap ≥ 0.7 AND instruction Jaccard ≥ 0.55 AND quality gap ≤ 3) into `archive/`.
- `de-fingerprint.py --apply` — content/name consistency.
- `merge-candidates-v2.py` — family-level merge ranking report; decide per line manually.
- Nothing is ever deleted: `archive/` is git-tracked and recoverable.