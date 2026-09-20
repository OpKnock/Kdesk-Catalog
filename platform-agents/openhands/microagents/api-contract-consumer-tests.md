---
name: "api-contract-consumer-tests"
description: "Implements contract testing basics: Pact consumer expectations, mock services, and first provider verification runs. Use when working with consumer tests, provider verification or when the user mentions consumer tests, provider verification."
type: knowledge
triggers: ["api-contract-consumer-tests", "consumer-tests", "provider-verification"]
---

Implements contract testing basics: Pact consumer expectations, mock services, and first provider verification runs.

## Agentic Workflow: Read -> Reason -> Act (api-contract-consumer-tests)

You are **Api Contract Consumer Tests** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-contract-consumer-tests`
- Domain: Implements contract testing basics: Pact consumer expectations, mock services, and first provider verification runs.
- **consumer-tests**: Write Pact consumer tests with interactions and expected responses — `npm install @pact-foundation/pact --save-dev`
- **provider-verification**: Verify the provider against published contracts — `npm install @pact-foundation/pact-js --save-dev`
- Check `knowledge` and `prerequisites: pact, openapi, node.js, python`

### 2. Reason — think for `api-contract-consumer-tests`
- For `consumer-tests`: Write Pact consumer tests with interactions and expected responses — decide which checks to run
- For `provider-verification`: Verify the provider against published contracts — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-contract-consumer-tests` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-contract-consumer-tests:286f7ede`

# API Contract (Basics)

Implements the core consumer-driven contract loop: expectations, publication, verification.

## When to Use
- First contract test in a codebase
- Single consumer-provider pair
- Learning the Pact flow

## Real Commands

```bash
# Consumer side
npm install @pact-foundation/pact --save-dev
npx jest --testMatch '**/*.pact.test.js'

# Inspect the generated pact
cat pacts/consumer-provider.json | python -m json.tool

# Publish
npx pact-broker publish ./pacts --consumer-version 0.1.0 --broker-base-url http://localhost:9292

# Provider side
npx pact-provider-verifier --provider-base-url http://localhost:8080 --pact-urls ./pacts/consumer-provider.json
```

## The Loop
1. Consumer defines expectations
2. Pact file is generated
3. Provider verifies against it
4. can-i-deploy gates the release

## Testing
Run consumer tests in CI on every PR and provider verification nightly.

## Best Practices
- Keep interactions minimal
- Version every publish

## Capabilities

### consumer-tests
Write Pact consumer tests with interactions and expected responses

**Parameters:**
- `consumer` (string): Consumer name
- `provider` (string): Provider name
- `version` (string): Contract version

**Commands:**
- `npm install @pact-foundation/pact --save-dev`
- `npx jest --testMatch '**/*.pact.test.js'`
- `npx pact-broker publish ./pacts --consumer-version 0.1.0 --broker-base-url http://localhost:9292`
- `npx pact-broker describe-version --pacticipant consumer --version 0.1.0 --broker-base-url http://localhost:9292`
- `cat pacts/consumer-provider.json | python -m json.tool`

**Examples:**
- npx jest --testMatch '**/*.pact.test.js' --runInBand
- cat pacts/consumer-provider.json | python -m json.tool
- npx pact-broker publish ./pacts --consumer-version 0.1.0 --broker-base-url http://localhost:9292

### provider-verification
Verify the provider against published contracts

**Parameters:**
- `baseUrl` (string): Provider base URL
- `pactUrls` (string): Pact file paths

**Commands:**
- `npm install @pact-foundation/pact-js --save-dev`
- `npx pact-provider-verifier --provider-base-url http://localhost:8080 --pact-urls ./pacts/consumer-provider.json`
- `npx pact-provider-verifier --provider-base-url http://localhost:8080 --pact-broker-base-url http://localhost:9292 --provider consumer`
- `npm run verify:pacts`
- `npx pact-broker can-i-deploy --pacticipant provider --version 1.0.0 --to prod --broker-base-url http://localhost:9292`

**Examples:**
- npx pact-provider-verifier --provider-base-url http://localhost:8080 --pact-urls ./pacts/consumer-provider.json
- npm run verify:pacts
- npx pact-provider-verifier --provider-base-url http://localhost:8080 --pact-broker-base-url http://localhost:9292 --provider consumer

## References
- [Pact Mock Service](https://docs.pact.io/implementation_guides/mock_service/)
- [Pact Verifier](https://docs.pact.io/implementation_guides/rust/verifier_cli)
