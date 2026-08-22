---
type: agent_requested
description: "Wires contract testing into CI/CD: broker pipelines, deploy gates, and breaking-change detection for every release."
---

# Api Contract Ci

Wires contract testing into CI/CD: broker pipelines, deploy gates, and breaking-change detection for every release.

## Instructions

# API Contract (CI/CD)

Makes contract tests a release gate, not an afterthought.

## When to Use
- Releases break consumers silently
- Multiple teams share one API
- Need deploy-time confidence

## Real Commands

```bash
# In the consumer pipeline
npx pact-broker publish ./pacts --consumer-version $BUILD_NUMBER --broker-base-url http://localhost:9292

# In the provider pipeline
npx pact-provider-verifier --provider-base-url http://localhost:8080 --pact-broker-base-url http://localhost:9292 --provider api

# Gate the release
npx pact-broker can-i-deploy --pacticipant api --version $BUILD_NUMBER --to prod --broker-base-url http://localhost:9292

# Record the deployment
npx pact-broker record-deployment --pacticipant api --version $BUILD_NUMBER --environment prod --broker-base-url http://localhost:9292

# Spec diff gate
openapi-diff --fail-on-incompatible main.yaml pr.yaml
```

## Pipeline Layout
- Consumer: test, publish, can-i-deploy
- Provider: verify, can-i-deploy
- Release: record-deployment

## Testing
Break a contract on purpose and confirm the gate blocks the release.

## Best Practices
- Version every build
- Record deployments so the broker knows prod state

## Capabilities

### ci-integration
Add Pact publish, verify, and can-i-deploy steps to pipelines

**Commands:**
- `npx pact-broker publish ./pacts --consumer-version $BUILD_NUMBER --broker-base-url http://localhost:9292`
- `npx pact-provider-verifier --provider-base-url http://localhost:8080 --pact-broker-base-url http://localhost:9292 --provider api --consumer-version-selector '{"branch":"main"}'`
- `npx pact-broker can-i-deploy --pacticipant api --version $BUILD_NUMBER --to prod --broker-base-url http://localhost:9292`
- `npx pact-broker record-deployment --pacticipant api --version $BUILD_NUMBER --environment prod --broker-base-url http://localhost:9292`
- `npx pact-broker list-environments --broker-base-url http://localhost:9292`

**Examples:**
- npx pact-broker publish ./pacts --consumer-version $BUILD_NUMBER --broker-base-url http://localhost:9292
- npx pact-broker can-i-deploy --pacticipant api --version $BUILD_NUMBER --to prod --broker-base-url http://localhost:9292
- npx pact-broker record-deployment --pacticipant api --version $BUILD_NUMBER --environment prod --broker-base-url http://localhost:9292

### breaking-change-gates
Block incompatible spec changes with automated diffs

**Commands:**
- `openapi-diff --fail-on-incompatible main.yaml pr.yaml`
- `git diff main.yaml pr.yaml --stat`
- `npx @stoplight/spectral-cli lint pr.yaml`
- `swagger-cli validate pr.yaml`
- `openapi-diff --fail-on-changed main.yaml pr.yaml`

**Examples:**
- openapi-diff --fail-on-incompatible main.yaml pr.yaml
- git diff main.yaml pr.yaml --stat && openapi-diff --fail-on-incompatible main.yaml pr.yaml
- swagger-cli validate pr.yaml && npx @stoplight/spectral-cli lint pr.yaml