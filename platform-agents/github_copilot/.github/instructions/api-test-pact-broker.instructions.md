---
applyTo: "**/*.json **/*.r **/*.sh"
---

Implements contract testing with Pact: consumer expectations, provider verification, Pact Broker versioning, and can-i-deploy gating.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pact-broker create-or-update-pacticipant --name OrderService`, `npm install @pact-foundation/pact --save-dev`
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

# API Test v2 - Contract Testing

Contract testing with Pact.

## What This Skill Does
- Defines consumer expectations as pacts
- Verifies providers against pacts
- Gates deploys with Pact Broker

## When to Use
- Service-to-service APIs
- Preventing breaking changes
- Independent deployments

## Real Commands

```bash
pact-broker publish ./pacts --consumer-app-version 1.2.3 --broker-base-url https://broker.example.com
npx pact-verifier --provider-base-url http://localhost:3000 --pact-url ./pacts/order-consumer-order-service.json
pact-broker can-i-deploy --pacticipant OrderService --version 1.2.3 --to prod
```

## Contract Flow
1. Consumer generates pacts in tests
2. Publish pacts to the broker
3. Provider verifies on each build
4. can-i-deploy gates releases

## Testing
- Run verification in provider CI
- Tag versions for environment tracking
- Check matrix results for compatibility


## Best Practices
- One pact per consumer-provider pair
- Keep pacts small and focused
- Automate can-i-deploy in release pipelines

## Capabilities

### pact-broker
Publish and manage contracts with Pact Broker

**Parameters:**
- `pacticipant` (string): Service name
- `version` (string): Application version
- `broker-url` (string): Pact Broker base URL

**Commands:**
- `pact-broker create-or-update-pacticipant --name OrderService --broker-base-url http://localhost:8080`
- `pact-broker publish ./pacts --consumer-app-version 1.2.3 --broker-base-url http://localhost:8080`
- `pact-broker create-version-tag --pacticipant OrderService --version 1.2.3 --tag prod --broker-base-url https://broker.example.com`
- `pact-broker can-i-deploy --pacticipant OrderService --version 1.2.3 --to prod --broker-base-url http://localhost:8080`

**Examples:**
- publish uploads generated pact files
- create-version-tag marks prod versions
- can-i-deploy blocks incompatible releases

### pact-testing
Verify provider against consumer contracts

**Commands:**
- `npm install @pact-foundation/pact --save-dev`
- `npx pact-verifier --provider-base-url http://localhost:3000 --pact-url ./pacts/order-consumer-order-service.json`
- `npx jest --verbose`
- `pact-broker list-latest-pact-versions --broker-base-url http://localhost:8080`

**Examples:**
- -cli --help
- -api --help

## References
- [Pact Docs](https://docs.pact.io/)
- [Pact Broker](https://docs.pact.io/pact_broker/)
