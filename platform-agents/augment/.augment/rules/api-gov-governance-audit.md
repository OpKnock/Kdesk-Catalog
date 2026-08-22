---
type: agent_requested
description: "Audits and enforces API governance on existing OpenAPI specs, blocking non-compliant changes via CI linting with Spectral rulesets."
---

# Api Gov Governance Audit

Audits and enforces API governance on existing OpenAPI specs, blocking non-compliant changes via CI linting with Spectral rulesets.

## Instructions

# API Gov (Audit & Enforce)

Audits existing OpenAPI specs against an organizational style guide and enforces compliance in CI.

## When to Use
- Enforcing standards on a mature spec base
- Blocking breaking or non-compliant PRs
- Measuring governance drift over time
- Onboarding teams onto a published style guide

## Real Commands

```bash
# Install tooling
npm install -g @stoplight/spectral-cli
npm install -g @redocly/cli

# Lint a spec
npx @stoplight/spectral-cli lint openapi.yaml

# Lint with a custom ruleset
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml

# Recommended defaults
redocly lint openapi.yaml --extends=recommended

# Validate structure first
swagger-cli validate openapi.yaml
```

## CI Gate

```yaml
# .github/workflows/api-governance.yml
- name: Lint specs
  run: npx @stoplight/spectral-cli lint --fail-severity error ${{ matrix.spec }}
```

## Testing
Run the linter on the PR branch against the main branch baseline and compare JSON reports.

## Best Practices
- Publish the style guide alongside the ruleset
- Use `--fail-severity error` in CI, `warn` locally
- Review lint report trends each sprint

## Capabilities

### governance-audit
Run Spectral linting against existing OpenAPI specs to surface style guide violations and drift

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml`
- `redocly lint openapi.yaml --extends=recommended`
- `swagger-cli validate openapi.yaml`
- `npx @stoplight/spectral-cli lint --fail-severity error openapi.yaml`

**Examples:**
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > spectral-report.json
- redocly lint api/v1/*.yaml --output-style=github-actions
- swagger-cli validate openapi.yaml && npx @stoplight/spectral-cli lint openapi.yaml

### compliance-gates
Wire lint gates into CI/CD so non-compliant API changes fail the pipeline

**Commands:**
- `npx @stoplight/spectral-cli lint --fail-severity warn openapi.yaml`
- `npx @stoplight/spectral-cli lint --fail-on-unmatched-globs openapi.yaml`
- `git diff --name-only HEAD~1 | grep -E '\.(yaml|yml|json)$' | xargs npx @stoplight/spectral-cli lint`
- `openapi-diff --fail-on-incompatible old.yaml new.yaml`
- `npx @stoplight/spectral-cli lint --summary openapi.yaml`

**Examples:**
- git diff --name-only HEAD~1 | xargs npx @stoplight/spectral-cli lint --fail-severity error
- openapi-diff --fail-on-incompatible prod-spec.yaml pr-spec.yaml
- npx @stoplight/spectral-cli lint --summary --quiet openapi.yaml