# Contributing to Kdesk-Catalog

Thank you for your interest in contributing!

## Quick Start

```bash
git clone https://github.com/OpKnock/Kdesk-Catalog
cd Kdesk-Catalog
pip install pyyaml jsonschema pytest
```

## Adding an Agent or Skill

1. Create a `.yaml` file under `universal-agents/<category>/agent/` or `<category>/skill/`
2. Follow the schema in `schemas/universal-agent.schema.json`
3. Required fields: `name`, `display_name`, `category`, `description`, `version`, `platforms`, `capabilities`, `examples`, `instructions`, `knowledge`

### Description Rules

- Minimum **200 characters** (enforced by policy engine)
- Explain what the agent does, when to use it, and what tools it needs

### Capabilities

Every capability must include:
- `name` — short identifier
- `description` — what it does
- `commands` — real working CLI commands (first word = tool binary for wiring)
- `examples` — realistic usage examples
- `parameters` — typed input parameters with descriptions

## Validation

```bash
# Schema validation (must pass)
python scripts/schema-check.py

# Policy checks
python -m kdesk.cli policy

# Full verification
python -m kdesk.cli verify --fast
```

## Pull Requests

1. Branch from `main`: `git checkout -b feat/my-agent`
2. Make changes in `universal-agents/` only (never edit `agents/`, `skills/`, `workflows/`, `platform-agents/`)
3. Run validation locally
4. Push and open a PR — CI will auto-regenerate outputs

## Code Style

- Python: follow PEP 8, no comments unless asked
- YAML: 2-space indent, lowercase kebab-case names
- Commit messages: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
