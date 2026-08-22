---
name: "breaking-change-detection"
description: "Detects breaking changes in OpenAPI specs with openapi-diff, Redocly lint, and changelog-based CI gates."
type: knowledge
triggers: ["breaking-change-detection", "openapi-diff", "redocly-lint", "ci-gates"]
---

# Breaking Change Detection

Detects breaking changes in OpenAPI specs with openapi-diff, Redocly lint, and changelog-based CI gates.

## Instructions

# Breaking Change Detection

## What this skill does

Detects breaking changes in OpenAPI specs: openapi-diff classification, openapi-changes JSON output, Redocly lint gates, and git-based CI checks comparing released specs.

## When to use

- A PR modifies openapi.yaml; is it safe to merge?
- Planning a v2 release
- Enforcing additive-only changes in CI

## Real commands

```bash
# Classify changes
npx openapi-diff old.yaml new.yaml

# Fail CI on breaking changes
npx openapi-diff old.yaml new.yaml --fail-on incompatible

# JSON analysis
npx openapi-changes compare old.yaml new.yaml --json | jq '.breaking'

# Pull the released spec from git
 git show v1.0.0:openapi.yaml > old.yaml

# Lint
npx @redocly/cli lint new.yaml

# Validate
npx swagger-cli validate new.yaml
```

Note: ` git show` with a leading space is just shell formatting; use `git show` normally.

## Testing

- Add a test fixture pair: additive (pass) and breaking (fail) specs
- Run openapi-diff in CI on every spec change

## Best practices

- Treat openapi-diff as advisory, Redocly as style enforcement
- Require a changelog entry alongside breaking changes
- Keep old.yaml as the last released tag, not main

## Capabilities

### openapi-diff
Diff OpenAPI specs for breaking changes.

**Commands:**
- `npx openapi-diff old.yaml new.yaml`
- `npx openapi-diff old.yaml new.yaml --output console --fail-on incompatible`
- `npx openapi-changes compare old.yaml new.yaml`
- `npx openapi-changes compare old.yaml new.yaml --json | jq '.breaking'`

**Examples:**
- npx openapi-diff old.yaml new.yaml | grep -E 'incompatible|breaking'
- npx openapi-diff --fail-on incompatible old.yaml new.yaml && echo "compatible"
- npx openapi-changes compare old.yaml new.yaml --json | jq '.breaking[].path'

### redocly-lint
Lint specs and enforce API style rules in CI.

**Commands:**
- `npx @redocly/cli lint openapi.yaml`
- `npx @redocly/cli lint --extends recommended new.yaml`
- `npx @redocly/cli lint --format=stylish new.yaml`
- `npx @redocly/cli lint --skip-rule operation-4xx-response new.yaml`

**Examples:**
- npx @redocly/cli lint --extends recommended new.yaml
- npx @redocly/cli lint --format=json new.yaml > lint.json
- npx @redocly/cli lint new.yaml --skip-rule no-server-api.your-app.test

### ci-gates
Wire compat checks into CI.

**Commands:**
- `git diff --exit-code v1.0.0 v1.1.0 -- openapi.yaml`
- `npx swagger-cli validate new.yaml`
- `git show v1.0.0:openapi.yaml > old.yaml`
- `npx openapi-diff old.yaml new.yaml > compat.txt`

**Examples:**
- git show v1.0.0:openapi.yaml > old.yaml && npx openapi-diff old.yaml new.yaml
- npx swagger-cli validate new.yaml
- npx openapi-diff old.yaml new.yaml > compat.txt && grep -c incompatible compat.txt
