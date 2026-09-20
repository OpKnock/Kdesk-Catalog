---
name: "validation"
description: "Validates JSON payloads against JSON Schema (draft 2020-12) using ajv-cli and Python jsonschema. Compiles schemas to catch errors before deployment, enforces contracts in CI pipelines, and performs quick shape checks with jq. Use when working with schema validate, api, json schema, validation or when the user mentions schema validate, api, json schema, validation."
type: knowledge
triggers: ["validation", "schema-validate"]
---

Validates JSON payloads against JSON Schema (draft 2020-12) using ajv-cli and Python jsonschema. Compiles schemas to catch errors before deployment, enforces contracts in CI pipelines, and performs quick shape checks with jq.

## Agentic Workflow: Read -> Reason -> Act (validation)

You are **Validation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `validation`
- Domain: Validates JSON payloads against JSON Schema (draft 2020-12) using ajv-cli and Python jsonschema. Compiles schemas to catch errors before deployment, enforces contracts in CI pipelines, and performs qu
- **schema-validate**: Validate JSON payloads against JSON Schema — `npx ajv-cli validate -s schema.json -d data.json --strict=false`
- Check `knowledge` and `prerequisites: npx, python, jq`

### 2. Reason — think for `validation`
- For `schema-validate`: Validate JSON payloads against JSON Schema — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `validation` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `validation:73dc273a`

# Validation

Hand-crafted skill for schema validation of JSON payloads.

## What this skill does

- Validates payloads against JSON Schema (draft 2020-12)
- Compiles schemas to check them before shipping
- Guards pipelines and webhooks against bad shapes

## When to use

- CI gates on API response shapes
- Validating webhook payloads before processing
- Enforcing contracts between producers and consumers

## Real commands

```bash
# Validate a document
npx ajv-cli validate -s schema.json -d data.json --strict=false

# Python alternative
python -m jsonschema -i data.json schema.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('data.json')), json.load(open('schema.json'))); print('valid')"

# Compile-only check (schema itself must be valid)
npx ajv-cli compile -s schema.json

# Quick jq shape checks
jq 'type == "object" and (.id | type == "string") and (.price | type == "number")' data.json
jq 'has("required_field")' data.json
```

## Example schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "price"],
  "properties": {
    "id": {"type": "string"},
    "price": {"type": "number", "minimum": 0}
  }
}
```

## Testing

```bash
npx ajv-cli validate -s schema.json -d data.json --strict=false
npx ajv-cli compile -s schema.json
```

## Best practices

- Ship the schema with the contract, not after
- Keep --strict off only when schemas use unknown extensions
- Fail CI on invalid payloads, never warn

## Capabilities

### schema-validate
Validate JSON payloads against JSON Schema

**Parameters:**
- `schema` (string): Path to JSON Schema file
- `data` (string): Path to data file to validate
- `strict` (boolean): Reject unknown keywords

**Commands:**
- `npx ajv-cli validate -s schema.json -d data.json --strict=false`
- `python -m jsonschema -i data.json schema.json`
- `python -c "import json, jsonschema; jsonschema.validate(json.load(open(\"data.json\")), json.load(open(\"schema.json\"))); print(\"valid\")"`
- `npx ajv-cli compile -s schema.json`
- `jq "type == \"object\" and (.id | type == \"string\") and (.price | type == \"number\")" data.json`

**Examples:**
- npx ajv-cli validate -s schema.json -d data.json --strict=false
- python -m jsonschema -i data.json schema.json
- jq "has(\"required_field\")" data.json

## References
- [JSON Schema spec](https://json-schema.org/)
- [Ajv CLI docs](https://ajv.js.org/guide/cli.html)
- [Python jsonschema](https://python-jsonschema.readthedocs.io/)
