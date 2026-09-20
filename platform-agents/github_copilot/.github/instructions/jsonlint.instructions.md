---
applyTo: "**/*.json **/*.py **/*.r **/*.rs **/*.sh"
---

Validate JSON syntax from files or stdin. Query, format, and transform JSON with jq.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `jsonlint config.json`, `jq . config.json`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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
