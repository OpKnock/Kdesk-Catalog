---
name: "contract-testing-spec-diff"
description: "Schema-based contract testing: diff OpenAPI specs across versions and lint schemas with spectral and openapi-diff. Use when working with spec diff, spectral lint, api or when the user mentions spec diff, spectral lint, api."
---

Schema-based contract testing: diff OpenAPI specs across versions and lint schemas with spectral and openapi-diff.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx openapi-diff openapi-v1.yaml openapi-v2.yaml`, `npx @stoplight/spectral-cli lint openapi.yaml`
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
