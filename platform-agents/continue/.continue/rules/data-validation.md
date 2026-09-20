---
name: "Data Validation"
description: "Implements schema validation across JSON Schema, Pydantic, and Joi to enforce request, config, and message contracts."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

# Data Validation

Implements schema validation across JSON Schema, Pydantic, and Joi to enforce request, config, and message contracts.

## Instructions

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

**Commands:**
- `python -m pip install pydantic`
- `python -c "from pydantic import BaseModel; print(BaseModel.__module__)"`
- `npm install joi`
- `npx ajv-cli validate -s schema.json -d data.json`

**Examples:**
- python -c "from pydantic import TypeAdapter; print(TypeAdapter(int).validate_python(1))"
- npx ajv-cli compile -s schema.json