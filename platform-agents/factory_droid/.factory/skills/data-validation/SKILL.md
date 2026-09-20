---
name: "data-validation"
description: "Implements schema validation across JSON Schema, Pydantic, and Joi to enforce request, config, and message contracts. Use when working with json schema validation, runtime validation, backend or when the user mentions json schema validation, runtime validation, backend."
license: "MIT"
compatibility: "Requires ajv, npm, npx, python."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(ajv:*) Bash(npm:*) Bash(npx:*) Bash(python:*)"
---

Implements schema validation across JSON Schema, Pydantic, and Joi to enforce request, config, and message contracts.

## Agentic Workflow: Read -> Reason -> Act (data-validation)

You are **Data Validation** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `data-validation`
- Domain: Implements schema validation across JSON Schema, Pydantic, and Joi to enforce request, config, and message contracts.
- **json-schema-validation**: Validate JSON documents against schemas from the CLI. — `ajv validate -s schema.json -d data.json`
- **runtime-validation**: Generate and use runtime validators in Python and Node. — `python -m pip install pydantic`
- Check `knowledge` and `prerequisites: ajv, npm, npx, python`

### 2. Reason — think for `data-validation`
- For `json-schema-validation`: Validate JSON documents against schemas from the CLI. — decide which checks to run
- For `runtime-validation`: Generate and use runtime validators in Python and Node. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `data-validation` tools
- Tools: `Glob`, `Grep`, `Read`, `Ajv`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `data-validation:6cac48dd`

# Data Validation

Enforce data contracts at API boundaries, config load, and message ingestion.

## When to Use

- Validating HTTP request bodies and query params
- Parsing environment variables and config files
- Validating messages consumed from queues
- Catching malformed data before it reaches business logic

## Commands

```bash
# Validate one file with Ajv
ajv validate -s schema.json -d data.json

# Show all errors
ajv validate -s schema.json -d data.json --all-errors

# Compile a schema to check it is valid
ajv compile -s schema.json

# Python jsonschema CLI
python -m jsonschema -i instance.json schema.json

# Generate a schema from TypeScript types
npx ts-json-schema-generator --path src/types.ts --type User
```

## Schema Example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["email", "age"],
  "properties": {
    "email": { "type": "string", "format": "email" },
    "age": { "type": "integer", "minimum": 0 }
  },
  "additionalProperties": false
}
```

## Pydantic Example

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=120)
```

## Best Practices

- Validate at the boundary only; keep internal code assumption-free
- Use additionalProperties: false to catch typos in payloads
- Reject unknown enum values instead of defaulting silently
- Add format validators for email, uri, and date-time
- Test schemas with representative invalid samples in CI

## Capabilities

### json-schema-validation
Validate JSON documents against schemas from the CLI.

**Parameters:**
- `schema` (string): Path to JSON schema file
- `data` (string): Path to JSON instance file or glob
- `all-errors` (boolean): Report all errors instead of the first

**Commands:**
- `ajv validate -s schema.json -d data.json`
- `ajv compile -s schema.json`
- `python -m jsonschema -i instance.json schema.json`
- `npx ts-json-schema-generator --path src/types.ts --type User`
- `ajv validate -s schema.json -d "data/*.json"`

**Examples:**
- ajv validate -s schema.json -d data.json --all-errors
- python -m jsonschema -i data.json schema.json
- ajv compile -s schema.json --strict=false

### runtime-validation
Generate and use runtime validators in Python and Node.

**Parameters:**
- `language` (string): Target stack: python or node
- `framework` (string): Validation library: pydantic, joi, ajv

**Commands:**
- `python -m pip install pydantic`
- `python -c "from pydantic import BaseModel; print(BaseModel.__module__)"`
- `npm install joi`
- `npx ajv-cli validate -s schema.json -d data.json`

**Examples:**
- python -c "from pydantic import TypeAdapter; print(TypeAdapter(int).validate_python(1))"
- npx ajv-cli compile -s schema.json

## References
- [JSON Schema](https://json-schema.org/)
- [Pydantic Docs](https://docs.pydantic.dev)
- [Ajv Docs](https://ajv.js.org)
