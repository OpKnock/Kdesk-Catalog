# Contract Testing Spec Diff

Schema-based contract testing: diff OpenAPI specs across versions and lint schemas with spectral and openapi-diff.

## Instructions

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

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml --format json`
- `npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yaml -f junit`

**Examples:**
- npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yaml
- npx @stoplight/spectral-cli lint openapi.yaml -f json > lint.json
- npx @stoplight/spectral-cli lint openapi.yaml --ruleset-json