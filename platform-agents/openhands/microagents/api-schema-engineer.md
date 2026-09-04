---
name: "api-schema-engineer"
description: "Authors JSON Schema documents: drafting schema files, ajv compilation and validation, test files, and format handling with ajv-cli."
type: knowledge
triggers: ["api-schema-engineer", "schema-authoring", "draft-handling"]
---

# api-schema-engineer

Authors JSON Schema documents: drafting schema files, ajv compilation and validation, test files, and format handling with ajv-cli.

## Instructions

# API Schema Engineer

JSON Schema authoring and validation.

## What This Skill Does
- Writes JSON Schema for API payloads
- Validates instances with ajv-cli
- Maintains schema test suites

## When to Use
- Defining API request/response contracts
- Validating configuration files
- Sharing validation rules across services

## Real Commands

```bash
npm install -g ajv-cli
ajv compile -s user.schema.json --strict=false
ajv validate -s user.schema.json -d user.json --strict=false
ajv test -s user.schema.json -t user.schema.test.json --strict=false
```

## Schema Example

```json
{
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "email": { "type": "string", "format": "email" }
  },
  "required": ["email"]
}
```

## Testing
- Maintain positive and negative test files
- Run ajv test in CI
- Test formats like email, date-time, uri

## Best Practices
- Keep schemas in a shared package
- Reference with $ref instead of duplication
- Use $defs for reusable components

## Capabilities

### schema-authoring
Write and validate JSON Schema files

**Commands:**
- `npm install -g ajv-cli`
- `ajv compile -s user.schema.json --strict=false`
- `ajv validate -s user.schema.json -d user.json --strict=false`
- `ajv test -s user.schema.json -t user.schema.test.json --strict=false`
- `ajv migrate -s legacy.schema.json -o modern.schema.json`

**Examples:**
- ajv compile checks schema syntax
- ajv validate checks a data file against the schema
- ajv test runs positive/negative test files

### draft-handling
Handle schema drafts and formats

**Commands:**
- `ajv validate -s user.schema.json -d bad.json --strict=false 2>&1 | head -5`
- `node -e "const Ajv=require('ajv'); const addFormats=require('ajv-formats'); const a=new Ajv(); addFormats(a); const v=a.compile({type:'string',format:'email'}); console.log(v('x@y.com'), v('nope'))"`
- `node -e "console.log(require('ajv').defaults)"`

**Examples:**
- -cli --help
- -api --help
