---
type: agent_requested
description: "Validates API contracts continuously: response schema checks at runtime, spec diffs in CI, and consumer contract verification. Use when working with runtime validation, spec diff checking or when the user mentions runtime validation, spec diff checking."
---

Validates API contracts continuously: response schema checks at runtime, spec diffs in CI, and consumer contract verification.

## Agentic Workflow: Read -> Reason -> Act (api-contract-validator-api-contract-validator)

You are **api-contract-validator-api-contract-validator** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-contract-validator-api-contract-validator`
- Domain: Validates API contracts continuously: response schema checks at runtime, spec diffs in CI, and consumer contract verification.
- **runtime-validation**: Validate API responses at runtime against the OpenAPI contract — `npm install express-openapi-validator`
- **spec-diff-checking**: Diff specs across versions in CI to block breaking changes — `openapi-diff v1.yaml v2.yaml`
- Check `knowledge` and `prerequisites: pact, openapi, node.js, python`

### 2. Reason — think for `api-contract-validator-api-contract-validator`
- For `runtime-validation`: Validate API responses at runtime against the OpenAPI contract — decide which checks to run
- For `spec-diff-checking`: Diff specs across versions in CI to block breaking changes — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-contract-validator-api-contract-validator` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Openapi-diff` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-contract-validator-api-contract-validator:ea1d2090`

# API Contract Validator

Validates contracts everywhere: at runtime, in tests, and in CI diffs.

## When to Use
- Spec drift reaches production
- Teams need early breaking-change alerts
- Third-party responses must match contracts

## Real Commands

```bash
# Runtime validation
npm install express-openapi-validator

# Test-time response checks
npm install supertest --save-dev
npx jest

# CI diff gates
openapi-diff --fail-on-incompatible v1.yaml v2.yaml

# Probe responses
curl -s http://localhost:3000/api/products/1 | python -m json.tool
```

## Validation Layers
- Runtime middleware: request/response shapes
- Tests: supertest assertions
- CI: openapi-diff on PRs

## Testing
Add negative tests: send responses that violate the schema and assert 500-level handling.

## Best Practices
- One spec per version, diffs in CI
- Log validation failures with request IDs

## Capabilities

### runtime-validation
Validate API responses at runtime against the OpenAPI contract

**Parameters:**
- `spec` (string): OpenAPI spec for runtime validation
- `endpoint` (string): Endpoint to validate

**Commands:**
- `npm install express-openapi-validator`
- `node -e "const v=require('express-openapi-validator');console.log(typeof v.middleware)"`
- `npm install @faker-js/faker --save-dev`
- `curl -s http://localhost:3000/api/products/1 | python -m json.tool`
- `npm install supertest --save-dev`

**Examples:**
- npm install express-openapi-validator
- curl -s http://localhost:3000/api/products/1 | python -m json.tool
- npm install supertest --save-dev && npx jest

### spec-diff-checking
Diff specs across versions in CI to block breaking changes

**Parameters:**
- `oldSpec` (string): Baseline spec
- `newSpec` (string): Candidate spec

**Commands:**
- `openapi-diff v1.yaml v2.yaml`
- `openapi-diff --fail-on-incompatible v1.yaml v2.yaml`
- `openapi-diff --fail-on-changed v1.yaml v2.yaml`
- `node -e "const {compare}=require('openapi-spec-validator');console.log(typeof compare)" 2>/dev/null || echo 'install openapi-spec-validator'`
- `git diff v1.yaml v2.yaml --stat`

**Examples:**
- openapi-diff --fail-on-incompatible v1.yaml v2.yaml
- openapi-diff v1.yaml v2.yaml | grep -i 'breaking'
- git diff v1.yaml v2.yaml --stat && openapi-diff v1.yaml v2.yaml

## References
- [express-openapi-validator](https://github.com/cdimascio/express-openapi-validator)
- [openapi-diff](https://github.com/OpenAPITools/openapi-diff)
- [supertest](https://github.com/ladjs/supertest)