---
trigger: glob
description: "Wires contract testing into CI/CD: broker pipelines, deploy gates, and breaking-change detection for every release. Use when working with ci integration, breaking change gates or when the user mentions ci integration, breaking change gates."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Wires contract testing into CI/CD: broker pipelines, deploy gates, and breaking-change detection for every release.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx pact-broker publish ./pacts --consumer-version $BUILD_NU`, `openapi-diff --fail-on-incompatible main.yaml pr.yaml`
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

**Parameters:**
- `broker` (string): Broker base URL
- `environment` (string): Deployment environment
- `buildNumber` (string): Build/version identifier

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

**Parameters:**
- `base` (string): Baseline spec
- `candidate` (string): PR spec

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

## References
- [Pact Broker can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy)
- [Pact Broker Environments](https://docs.pact.io/pact_broker/recording_deployments)
