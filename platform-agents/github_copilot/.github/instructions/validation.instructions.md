---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

# Validation

Validates JSON payloads against JSON Schema (draft 2020-12) using ajv-cli and Python jsonschema. Compiles schemas to catch errors before deployment, enforces contracts in CI pipelines, and performs quick shape checks with jq.

## Instructions

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
