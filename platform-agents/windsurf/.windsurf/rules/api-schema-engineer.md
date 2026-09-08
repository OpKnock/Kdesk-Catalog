---
trigger: glob
description: "Authors JSON Schema documents: drafting schema files, ajv compilation and validation, test files, and format handling with ajv-cli. Use when working with schema authoring, draft handling or when the user mentions schema authoring, draft handling."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Authors JSON Schema documents: drafting schema files, ajv compilation and validation, test files, and format handling with ajv-cli.

## Agentic Workflow: Read -> Reason -> Act (api-schema-engineer)

You are **api-schema-engineer** (data) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `api-schema-engineer`
- Domain: Authors JSON Schema documents: drafting schema files, ajv compilation and validation, test files, and format handling with ajv-cli.
- **schema-authoring**: Write and validate JSON Schema files — `npm install -g ajv-cli`
- **draft-handling**: Handle schema drafts and formats — `ajv validate -s user.schema.json -d bad.json --strict=false 2>&1 | head -5`
- Check `knowledge` and `prerequisites: openapi, json-schema, node.js, python`

### 2. Reason — think for `api-schema-engineer`
- For `schema-authoring`: Write and validate JSON Schema files — decide which checks to run
- For `draft-handling`: Handle schema drafts and formats — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-schema-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Ajv` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-schema-engineer:a01c526d`

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

**Parameters:**
- `schema` (string): Schema file path
- `data` (string): Data file to validate
- `strict` (boolean): Disable strict mode when false

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

## References
- [JSON Schema Docs](https://json-schema.org/learn/)
- [Ajv Docs](https://ajv.js.org/)
