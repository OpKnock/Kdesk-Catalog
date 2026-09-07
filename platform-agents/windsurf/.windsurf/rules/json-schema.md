---
trigger: glob
description: "Validate JSON documents against JSON Schema drafts (2020-12, 2019-09) with check-jsonschema and ajv, plus compile schemas and generate instances from tooling. Use when working with schema validation, schema compile, api or when the user mentions schema validation, schema compile, api."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Validate JSON documents against JSON Schema drafts (2020-12, 2019-09) with check-jsonschema and ajv, plus compile schemas and generate instances from tooling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `check-jsonschema --schemafile schema.json data.json`, `npx ajv compile -s schema.json`
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

# JSON Schema

Validate JSON documents against JSON Schema drafts with real CLI validators.

## What this skill does

- Validates JSON instances against schemas with check-jsonschema, ajv, and jsonschema.
- Compiles schemas ahead of time to catch schema syntax errors.
- Detects the document format (JSON/YAML/TOML) automatically.

## When to use

- Validating API payloads in CI before deploying.
- Enforcing contract compliance for config files and data exports.
- Auditing whether a schema change is backwards compatible.

## Real commands

```bash
# Basic validation (schema + document)
check-jsonschema --schemafile schema.json data.json

# Verbose mode reports every failing property
check-jsonschema --schemafile schema.json --verbose data.json

# YAML documents against a JSON schema
check-jsonschema --schemafile schema.json --default-filetype yaml config.yaml

# ajv validation with format keywords
npx ajv validate -s schema.json -d data.json -c ajv-formats

# Compile a schema to catch invalid schema syntax
npx ajv compile -s schema.json

# Python CLI
python3 -m jsonschema -i data.json schema.json
```

## Schema example (2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "amount", "currency"],
  "properties": {
    "id": {"type": "string", "pattern": "^ord_"},
    "amount": {"type": "number", "minimum": 0},
    "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]}
  },
  "additionalProperties": false
}
```

## Testing

```bash
# Negative test
echo '{"id":"bad","amount":-5}' | check-jsonschema --schemafile schema.json --default-filetype json /dev/stdin
```

## Best practices

- Pin the draft in the $schema keyword; different drafts change keyword semantics.
- Run check-jsonschema in CI for every schema change and data release.
- Use -c ajv-formats for date-time, email, and uuid format validation.
- Keep additionalProperties: false for strict contracts; relax for forward compatibility.

## Capabilities

### schema-validation
Validate JSON data files against a schema using check-jsonschema, ajv, and the Python jsonschema CLI.

**Parameters:**
- `schemafile` (string): Path to the JSON Schema file.
- `datafile` (string): Path to the JSON instance/document to validate.
- `filetype` (string): Input type: json, yaml, toml, or auto (default: json).

**Commands:**
- `check-jsonschema --schemafile schema.json data.json`
- `check-jsonschema --schemafile schema.json --default-filetype json --verbose data.json`
- `npx ajv validate -s schema.json -d data.json`
- `npx ajv validate -s schema.json -d data.json --strict=false`
- `python3 -m jsonschema -i data.json schema.json`

**Examples:**
- check-jsonschema --schemafile orders/schema.json orders/batch-1.json
- npx ajv validate -s schema.json -d data.json
- python3 -m jsonschema -i data.json schema.json

### schema-compile
Compile schemas with ajv for reuse and check schema syntax early in CI.

**Parameters:**
- `strict` (boolean): Enable/disable strict mode for unknown keywords.

**Commands:**
- `npx ajv compile -s schema.json`
- `npx ajv compile -s schema.json --strict=false -c ajv-formats`
- `check-jsonschema --schemafile schema.json --default-filetype json data.json --cache-filename schema-cache.json`

**Examples:**
- npx ajv compile -s schema.json
- npx ajv compile -s openapi.json -c ajv-formats

## References
- [JSON Schema Specifications](https://json-schema.org/specification)
- [check-jsonschema](https://github.com/python-jsonschema/check-jsonschema)
- [Ajv CLI](https://ajv.js.org/packages/ajv-cli.html)
