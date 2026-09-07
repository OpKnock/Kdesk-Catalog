---
type: agent_requested
description: "Implements schema validation across JSON Schema, Pydantic, and Joi to enforce request, config, and message contracts. Use when working with json schema validation, runtime validation, backend or when the user mentions json schema validation, runtime validation, backend."
---

Implements schema validation across JSON Schema, Pydantic, and Joi to enforce request, config, and message contracts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ajv validate -s schema.json -d data.json`, `python -m pip install pydantic`
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