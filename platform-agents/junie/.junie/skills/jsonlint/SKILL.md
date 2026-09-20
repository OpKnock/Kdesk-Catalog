---
name: "jsonlint"
description: "Validate JSON syntax from files or stdin. Query, format, and transform JSON with jq. Use when working with json validation, json processing, code quality or when the user mentions json validation, json processing, code quality."
license: "MIT"
compatibility: "Requires echo, jsonlint, python."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(echo:*) Bash(jq:*) Bash(jsonlint:*) Bash(python:*)"
---

Validate JSON syntax from files or stdin. Query, format, and transform JSON with jq.

## Agentic Workflow: Read -> Reason -> Act (jsonlint)

You are **jsonlint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `jsonlint`
- Domain: Validate JSON syntax from files or stdin. Query, format, and transform JSON with jq.
- **json-validation**: Validate JSON syntax from files or stdin. — `jsonlint config.json`
- **json-processing**: Query, format, and transform JSON with jq. — `jq . config.json`
- Check `knowledge` and `prerequisites: echo, jsonlint, python`

### 2. Reason — think for `jsonlint`
- For `json-validation`: Validate JSON syntax from files or stdin. — decide which checks to run
- For `json-processing`: Query, format, and transform JSON with jq. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `jsonlint` tools
- Tools: `Glob`, `Grep`, `Read`, `Jsonlint`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `jsonlint:fd9bb9f2`

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

**Parameters:**
- `file` (string): JSON file path
- `quiet` (boolean): Silent on success

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

**Parameters:**
- `filter` (string): jq filter expression
- `output` (string): Output file path

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

## References
- [jq Manual](https://jqlang.github.io/jq/manual/)
- [JSON Spec](https://www.json.org/json-en.html)
