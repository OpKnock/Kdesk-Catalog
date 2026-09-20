# api-gov-specialist

Deep expertise in API governance: authoring style guides, custom Spectral rulesets, and API review automation at scale.

## Instructions

# API Gov Specialist

Designs and operates API governance programs: style guides, custom linting, and automated review.

## When to Use
- Building org-wide API standards
- Custom rule enforcement beyond defaults
- Scaling review across many teams

## Real Commands

```bash
# Lint with custom ruleset
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml openapi.yaml

# JSON report for dashboards
npx @stoplight/spectral-cli lint -r .spectral.yaml --format json openapi.yaml > report.json

# Detect breaking changes between versions
openapi-diff --fail-on-incompatible v1.yaml v2.yaml

# CI-friendly output
redocly lint --extends=recommended openapi.yaml --output-style=github-actions
```

## Ruleset Example

```yaml
# .spectral.yaml
extends: [[spectral:oas, recommended]]
rules:
  no-internal-paths:
    message: Internal paths must be prefixed /internal
    given: $.paths[*]~
    severity: error
    then:
      function: pattern
      functionOptions: {match: "^(/internal|/v[0-9]+)"}
```

## Testing
Keep a fixture spec with intentional violations to verify rules fire correctly.

## Best Practices
- Version the ruleset like code
- Review new rules against existing specs before enabling as error

## Capabilities

### ruleset-authoring
Write custom Spectral rulesets with functions for org-specific API conventions

**Commands:**
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml openapi.yaml`
- `npx @stoplight/spectral-cli lint -r .spectral.yaml --format json openapi.yaml > report.json`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --verbose openapi.yaml`
- `node -e "const s=require('@stoplight/spectral'); console.log(s.version)"`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --fail-severity warn openapi.yaml`

**Examples:**
- npx @stoplight/spectral-cli lint -r .spectral.yaml --format json openapi.yaml > report.json && jq '.summary' report.json
- npx @stoplight/spectral-cli lint -r .spectral.yaml --verbose openapi.yaml
- npx @stoplight/spectral-cli lint -r .spectral.yaml --fail-severity error openapi.yaml

### review-automation
Automate API design review in PRs with linting and diff checks

**Commands:**
- `git diff --name-only --diff-filter=ACM origin/main HEAD | grep -E '\.(yaml|yml)$' | xargs npx @stoplight/spectral-cli lint`
- `openapi-diff --fail-on-incompatible --ignore-path path-to-ignore.json old.yaml new.yaml`
- `npx @stoplight/spectral-cli lint --summary --fail-severity error openapi.yaml`
- `redocly lint --extends=recommended openapi.yaml --output-style=github-actions`
- `swagger-cli validate $(git diff --name-only HEAD~1 | grep openapi.yaml)`

**Examples:**
- git diff --name-only origin/main HEAD | grep openapi.yaml | xargs npx @stoplight/spectral-cli lint --fail-severity error
- openapi-diff --fail-on-incompatible prod.yaml pr.yaml
- redocly lint --extends=recommended openapi.yaml --output-style=github-actions