---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# field-validation-engineer-field-validation-engineer

Builds schema-driven validation for APIs and data pipelines using JSON Schema, Ajv, and Redocly, with compile-time checks and CI enforcement.

## Instructions

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
