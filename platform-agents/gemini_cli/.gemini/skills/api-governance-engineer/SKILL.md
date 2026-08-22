---
name: "api-governance-engineer"
description: "Implements automated API governance: Spectral rulesets, PR review bots, and CI gates for OpenAPI quality."
---

# api-governance-engineer

Implements automated API governance: Spectral rulesets, PR review bots, and CI gates for OpenAPI quality.

## Instructions

# API Governance Engineer

Implements governance tooling: lint rules, CI gates, and PR checks.

## When to Use
- Enforcing API conventions mechanically
- Blocking non-compliant PRs
- Standardizing review effort

## Real Commands

```bash
# Local lint
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml openapi.yaml

# JSON report
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > report.json

# CI-friendly annotations
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format github-actions openapi.yaml

# Diff-based checks
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --fail-severity error openapi.yaml
```

## Ruleset Structure

```yaml
extends: [[spectral:oas, recommended]]
rules:
  path-kebab-case:
    message: Paths must use kebab-case
    given: $.paths[*]~
    then: {function: pattern, functionOptions: {match: '^/.*[a-z0-9-]*$'}}
```

## Testing
Create a violating spec fixture and assert the gate fails, then assert it passes after fixes.

## Best Practices
- Start warn, escalate to error over time
- Keep the ruleset in version control

## Capabilities

### ci-linting
Run Spectral in CI with custom rulesets and JSON reports

**Commands:**
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml openapi.yaml`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > report.json`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --fail-severity error openapi.yaml`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --verbose openapi.yaml`
- `node -e "const r=require('./report.json');console.log(r.filter(x=>x.severity===0).length+' errors')"`

**Examples:**
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --fail-severity error openapi.yaml
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > report.json && node -e "const r=require('./report.json');console.log(r.length+' violations')"
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --verbose openapi.yaml

### pr-checks
Wire governance checks into pull requests with GitHub Actions

**Commands:**
- `mkdir -p .github/workflows`
- `node -e "const fs=require('fs');fs.writeFileSync('.github/workflows/api-lint.yml','name: api-lint\non: [pull_request]\njobs:\n  lint:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: npx @stoplight/spectral-cli lint -r .spectral.yaml openapi.yaml\n')"`
- `git add .github/workflows/api-lint.yml && git commit -m 'add API lint gate'`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format github-actions openapi.yaml`
- `git diff --name-only origin/main HEAD | grep openapi | xargs npx @stoplight/spectral-cli lint`

**Examples:**
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format github-actions openapi.yaml
- git diff --name-only origin/main HEAD | grep openapi | xargs npx @stoplight/spectral-cli lint
- git add .github/workflows/api-lint.yml && git commit -m 'add API lint gate'
