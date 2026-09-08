---
trigger: glob
description: "Schema-based contract testing: diff OpenAPI specs across versions and lint schemas with spectral and openapi-diff. Use when working with spec diff, spectral lint, api or when the user mentions spec diff, spectral lint, api."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Schema-based contract testing: diff OpenAPI specs across versions and lint schemas with spectral and openapi-diff.

## Agentic Workflow: Read -> Reason -> Act (contract-testing-spec-diff)

You are **Contract Testing Spec Diff** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `contract-testing-spec-diff`
- Domain: Schema-based contract testing: diff OpenAPI specs across versions and lint schemas with spectral and openapi-diff.
- **spec-diff**: Detect breaking changes between OpenAPI spec versions with openapi-diff and swagger-cli — `npx openapi-diff openapi-v1.yaml openapi-v2.yaml`
- **spectral-lint**: Lint OpenAPI specs with custom Spectral rulesets to enforce contract rules — `npx @stoplight/spectral-cli lint openapi.yaml`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `contract-testing-spec-diff`
- For `spec-diff`: Detect breaking changes between OpenAPI spec versions with openapi-diff and swagger-cli — decide which checks to run
- For `spectral-lint`: Lint OpenAPI specs with custom Spectral rulesets to enforce contract rules — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `contract-testing-spec-diff` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `contract-testing-spec-diff:125f4e2c`

# Contract Testing v2 (Schema Based)

Verify API contracts by diffing and linting OpenAPI specifications.

## When to Use

- Catching breaking changes before release
- Enforcing API design rules in CI
- Contract testing without running services

## Validate the Spec

```bash
npx @apidevtools/swagger-cli validate openapi.yaml
npx @apidevtools/swagger-parser-cli validate openapi.yaml
```

## Detect Breaking Changes

```bash
npx openapi-diff openapi-v1.yaml openapi-v2.yaml
npx openapi-diff --summary-only openapi-v1.yaml openapi-v2.yaml
```

Breaking changes include removed paths, removed required properties, changed types, and removed enum values.

## Spectral Ruleset

```yaml
extends: ["spectral:oas"]
rules:
  api-version-header:
    description: Responses must include version header
    given: "$.paths[*][*].responses[*]"
    severity: error
    then:
      field: headers
      function: defined
  no-delete-remove:
    description: Never remove an operation without a new version
    given: "$.paths[*]"
    severity: warn
    then:
      function: truthy
```

```bash
npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yaml
```

## CI Integration

```bash
npx @stoplight/spectral-cli lint openapi.yaml -f junit > spectral-junit.xml
npx openapi-diff openapi-v1.yaml openapi-v2.yaml > diff.txt
```

## Best Practices

- Fail CI on breaking differences in stable API versions
- Version specs explicitly (openapi-v1.yaml, openapi-v2.yaml)
- Enforce the ruleset in pull requests
- Keep schemas strict: required fields, defined enums, explicit types
- Combine with consumer-driven Pact for runtime checks

## Capabilities

### spec-diff
Detect breaking changes between OpenAPI spec versions with openapi-diff and swagger-cli

**Parameters:**
- `spec_a` (string): Old OpenAPI spec file
- `spec_b` (string): New OpenAPI spec file

**Commands:**
- `npx openapi-diff openapi-v1.yaml openapi-v2.yaml`
- `npx @apidevtools/swagger-cli validate openapi.yaml`
- `npx @apidevtools/swagger-parser-cli validate openapi.yaml`
- `npx openapi-diff --summary-only openapi-v1.yaml openapi-v2.yaml`

**Examples:**
- npx @apidevtools/swagger-cli validate openapi.yaml
- npx openapi-diff openapi-v1.yaml openapi-v2.yaml
- npx openapi-diff --summary-only api-2024.yaml api-2025.yaml | jq '.breakingDifferences'

### spectral-lint
Lint OpenAPI specs with custom Spectral rulesets to enforce contract rules

**Parameters:**
- `ruleset` (string): Path to Spectral ruleset file
- `spec` (string): OpenAPI spec file to lint

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml --format json`
- `npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yaml -f junit`

**Examples:**
- npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yaml
- npx @stoplight/spectral-cli lint openapi.yaml -f json > lint.json
- npx @stoplight/spectral-cli lint openapi.yaml --ruleset-json

## References
- [OpenAPI Diff](https://github.com/OpenAPITools/openapi-diff)
- [Spectral Docs](https://docs.stoplight.io/docs/spectral)
