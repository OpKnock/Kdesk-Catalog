---
name: "field-validation-engineer-field-validation-engineer"
description: "Builds schema-driven validation for APIs and data pipelines using JSON Schema, Ajv, and Redocly, with compile-time checks and CI enforcement. Use when working with ajv, redocly or when the user mentions ajv, redocly."
license: "MIT"
compatibility: "Requires node.js, python, pydantic, zod, ajv, joi."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

Builds schema-driven validation for APIs and data pipelines using JSON Schema, Ajv, and Redocly, with compile-time checks and CI enforcement.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx ajv-cli compile -s schema.json`, `npx @redocly/cli lint openapi.yaml`
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

# Field Validation

Enforce contract-level validation with JSON Schema so bad data fails fast at the boundary.

## When to Use

- Defining request/response contracts for REST or event payloads
- Validating bulk imports and data pipelines
- Guarding against schema drift in polyglot services

## JSON Schema fundamentals

```json
{
  "type": "object",
  "required": ["email", "age"],
  "properties": {
    "email": {"type": "string", "format": "email", "maxLength": 254},
    "age": {"type": "integer", "minimum": 0, "maximum": 130}
  },
  "additionalProperties": false
}
```

Always set `additionalProperties: false` for internal payloads and keep external-facing schemas lenient where the provider may add fields.

## Validation workflow

```bash
npx ajv-cli compile -s user.schema.json
npx ajv-cli validate -s user.schema.json -d request.json --all-errors
```

Use `--all-errors` in tests to surface every violation in one run instead of fail-first behavior.

## OpenAPI enforcement

```bash
npx @redocly/cli lint openapi.yaml --extends=recommended
npx @redocly/cli lint --format=json openapi.yaml > lint-report.json
```

## Testing

Create a test-cases file: one entry per valid and invalid payload with expected outcome.

```bash
npx ajv-cli test -s schema.json -d cases.json --valid
```

## Best practices

- Version schemas; consumers pin to a major version.
- Prefer `format` and `pattern` over open-ended string types.
- Reject unknown fields in write paths to catch typos early.
- Run schema lint in CI so breaking changes fail the build.
- Use `$defs` for reusable components, not copy-paste duplication.

## Capabilities

### ajv
Compile and validate data against JSON Schema with Ajv CLI.

**Parameters:**
- `schema` (string): Path to the JSON Schema file
- `data` (string): Path or glob of data files to validate
- `strict` (string): true|false|log — strict mode for schema correctness

**Commands:**
- `npx ajv-cli compile -s schema.json`
- `npx ajv-cli validate -s schema.json -d data.json --strict=true`
- `npx ajv-cli validate -s schema.json -d 'data/*.json' --all-errors`
- `npx ajv-cli migrate -i legacy-schema.json -o modern-schema.json`
- `npx ajv-cli test -s schema.json -d test-cases.json --valid`

**Examples:**
- npx ajv-cli validate -s user.schema.json -d request.json --all-errors
- npx ajv-cli compile -s openapi.components.json --strict=false
- npx ajv-cli validate -s order.schema.json -d 'fixtures/*.json'

### redocly
Lint OpenAPI definitions for request/response schema quality.

**Parameters:**
- `extends` (string): Config preset: recommended, minimal, or a local config
- `format` (string): Output format: stylish, json, or codeframe
- `skip-rule` (string): Rule id to skip during linting

**Commands:**
- `npx @redocly/cli lint openapi.yaml`
- `npx @redocly/cli lint --extends=recommended --format=stylish openapi.yaml`
- `npx @redocly/cli bundle openapi.yaml -o dist/openapi.yaml`
- `npx @redocly/cli lint openapi.yaml --skip-rule no-unspecified-components`
- `npx @redocly/cli preview-docs openapi.yaml`

**Examples:**
- npx @redocly/cli lint openapi.yaml --format=json > lint-report.json
- npx @redocly/cli bundle src/openapi.yaml -o build/openapi.yaml
- npx @redocly/cli lint --extends=minimal openapi.yaml

## References
- [JSON Schema Spec](https://json-schema.org/)
- [Ajv Docs](https://ajv.js.org/)
- [Redocly CLI](https://www.redocly.com/docs/cli/)
