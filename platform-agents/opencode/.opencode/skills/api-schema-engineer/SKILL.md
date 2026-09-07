---
name: "api-schema-engineer"
description: "Authors JSON Schema documents: drafting schema files, ajv compilation and validation, test files, and format handling with ajv-cli. Use when working with schema authoring, draft handling or when the user mentions schema authoring, draft handling."
---

Authors JSON Schema documents: drafting schema files, ajv compilation and validation, test files, and format handling with ajv-cli.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g ajv-cli`, `ajv validate -s user.schema.json -d bad.json --strict=false `
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
