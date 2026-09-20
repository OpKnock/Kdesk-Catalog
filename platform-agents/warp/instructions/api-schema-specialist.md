# api-schema-specialist

Reviews and hardens API schemas with spectral: OpenAPI rulesets, custom rules, JSON output for CI, and schema quality gating.

## Instructions

# API Schema Specialist

Schema linting and review with spectral.

## What This Skill Does
- Lints OpenAPI contracts for consistency
- Enforces custom schema rules
- Exports reports for CI gating

## When to Use
- Reviewing schema PRs
- Enforcing API design standards
- Auditing legacy specs

## Real Commands

```bash
npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yml
npx @stoplight/spectral-cli lint openapi.yaml -f json -o report.json
npx @stoplight/spectral-cli lint openapi.yaml --fail-severity=warn
```

## Custom Rule

```yaml
rules:
  schemas-need-description:
    given: $.components.schemas[*]
    severity: error
    then:
      field: description
      function: truthy
```

## Testing
- Fail builds on error-severity violations
- Review JSON reports for triage
- Add rules incrementally

## Best Practices
- Extend a base ruleset before adding custom rules
- Document rule intent in comments
- Run lint in pre-merge checks

## Capabilities

### spectral-linting
Lint OpenAPI schemas with spectral

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yml`
- `npx @stoplight/spectral-cli lint openapi.yaml -f json -o report.json`
- `npx @stoplight/spectral-cli lint openapi.yaml -f junit -o junit.xml`
- `npx @stoplight/spectral-cli lint openapi.yaml --fail-severity=warn`

**Examples:**
- -f json exports machine-readable results
- --fail-severity=warn makes warnings fail CI
- -f junit integrates with test reports

### schema-review
Enforce schema quality rules

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml -r quality-rules.yaml`
- `curl -s http://localhost:3000/openapi.json -o openapi.json`
- `npx @stoplight/spectral-cli lint openapi.json -r .spectral.yml`
