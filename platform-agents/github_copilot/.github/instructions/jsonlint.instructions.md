---
applyTo: "**/*.json **/*.py **/*.r **/*.rs **/*.sh"
---

# jsonlint

Validate JSON syntax from files or stdin. Query, format, and transform JSON with jq.

## Instructions

# JSON Lint

Validate and manipulate JSON files.

## When to Use

- Verifying config and seed files parse correctly
- CI checks that catch invalid JSON early
- Querying and transforming JSON without writing scripts
- Cleaning up unformatted JSON output

## Commands

```bash
# Validate
jsonlint config.json
jsonlint -q config.json
jq empty config.json
python -m json.tool config.json > /dev/null

# Format
jq . config.json
python -m json.tool config.json

# Query
jq -r ".name" package.json
jq ".items | length" data.json
jq -r ".users[].email" users.json
jq "map(select(.active))" users.json

# Write sorted output
jq -S . config.json > formatted.json
```

## CI Example

```bash
jq empty ./*.json && echo "all valid"
```

## Best Practices

- Use jq empty in CI to validate without output
- Prefer -S for stable, sorted JSON in git
- Quote filters with single quotes in shells
- Use --arg to inject variables into filters safely
- Never eval JSON as code (no JSON.parse of untrusted)
- Keep JSON configs pretty-printed for review

## Capabilities

### json-validation
Validate JSON syntax from files or stdin.

**Commands:**
- `jsonlint config.json`
- `jsonlint -q config.json`
- `python -m json.tool config.json > /dev/null`
- `jq empty config.json`
- `echo "{\"a\":1}" | jsonlint`

**Examples:**
- jsonlint -q package.json && echo valid
- jq empty db/seed.json
- python -m json.tool config.json | head -20

### json-processing
Query, format, and transform JSON with jq.

**Commands:**
- `jq . config.json`
- `jq -r ".name" package.json`
- `jq ".items | length" data.json`
- `jq -S . config.json > formatted.json`
- `jq "map(select(.active))" users.json`

**Examples:**
- jq -r ".users[].email" users.json
- jq "group_by(.type) | map({type: .[0].type, count: length})" data.json
- jq --arg k "key" ".[$k]" data.json
