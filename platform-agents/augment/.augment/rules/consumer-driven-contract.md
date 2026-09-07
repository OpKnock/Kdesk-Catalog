---
type: agent_requested
description: "Implement consumer-driven contracts with Pact: publish pacts to a broker, check compatibility, and gate deployments with can-i-deploy. Use when working with pact broker, deployment gating, api or when the user mentions pact broker, deployment gating, api."
---

Implement consumer-driven contracts with Pact: publish pacts to a broker, check compatibility, and gate deployments with can-i-deploy.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d -p 9292:9292 pactfoundation/pact-broker:latest`, `npx @pact-foundation/pact-cli can-i-deploy --pacticipant Use`
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

# Consumer-Driven Contracts

Let consumers define what they expect from providers via Pact.

## When to Use

- Many consumers depending on one API
- Safe independent releases of consumer and provider
- Verifying compatibility before deployment

## Run the Broker

```bash
docker run -d -p 9292:9292 pactfoundation/pact-broker:latest
```

## Consumer Creates a Pact

```js
const { PactV3 } = require('@pact-foundation/pact');
const provider = new PactV3({ consumer: 'WebApp', provider: 'UserService' });
await provider.addInteraction({
  states: [{ description: 'user exists' }],
  uponReceiving: 'a request for a user',
  withRequest: { method: 'GET', path: '/users/42' },
  willRespondWith: { status: 200, body: { id: 42, name: 'alice' } },
});
```

## Publish

```bash
npx @pact-foundation/pact-cli publish ./pacts \
  --broker-base-url http://localhost:9292 \
  --consumer-version 1.0.0
```

## Provider Verifies

```bash
npx @pact-foundation/pact-cli verify \
  --provider-base-url http://localhost:8080 \
  --pact-urls http://localhost:9292/pacts/provider/UserService/consumer/WebApp/latest
```

## Gate Deployments

```bash
npx @pact-foundation/pact-cli can-i-deploy \
  --pacticipant UserService --version 2.0.0 --to-environment production
npx @pact-foundation/pact-cli record-deployment \
  --pacticipant UserService --version 2.0.0 --environment production
```

## Testing

```bash
# Break a contract: remove a field the consumer expects, then verify
npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.1 --to-environment production
```

## Best Practices

- Keep contract tests on the consumer side
- Verify provider against the latest pact of every consumer
- Use provider states to control test data
- Run can-i-deploy before every production deploy
- Record deployments to track the version matrix
- Fail CI when verification fails

## Capabilities

### pact-broker
Run the Pact Broker and publish pacts from consumer builds

**Parameters:**
- `pacts_dir` (string): Directory with pact json files
- `broker_url` (string): Pact Broker base URL

**Commands:**
- `docker run -d -p 9292:9292 pactfoundation/pact-broker:latest`
- `npx @pact-foundation/pact-cli publish ./pacts --broker-base-url http://localhost:9292 --consumer-version 1.0.0`
- `npx @pact-foundation/pact-cli list-latest-pact-versions --broker-base-url http://localhost:9292`
- `curl -s http://localhost:9292/ | grep -i pact`

**Examples:**
- npx @pact-foundation/pact-cli publish ./pacts --broker-base-url http://localhost:9292 --consumer-version 1.0.0
- npx @pact-foundation/pact-cli list-latest-pact-versions --broker-base-url http://localhost:9292
- curl -s http://localhost:9292/pacts/provider/UserService/consumer/WebApp/version/1.0.0 | jq '.interactions | length'

### deployment-gating
Check compatibility and gate deployments with can-i-deploy

**Parameters:**
- `pacticipant` (string): Service name (consumer or provider)
- `version` (string): Version to check
- `environment` (string): Target environment such as production

**Commands:**
- `npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.0 --to-environment production`
- `npx @pact-foundation/pact-cli can-i-deploy --pacticipant WebApp --version 1.0.0 --to-environment production`
- `npx @pact-foundation/pact-cli record-deployment --pacticipant UserService --version 2.0.0 --environment production`
- `npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --latest`

**Examples:**
- npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.0 --to-environment production
- npx @pact-foundation/pact-cli record-deployment --pacticipant UserService --version 2.0.0 --environment production
- npx @pact-foundation/pact-cli can-i-deploy --pacticipant WebApp --version 1.0.0 --to-environment production

## References
- [Pact Consumer-Driven Contracts](https://docs.pact.io/consumer-driven-contracts)
- [Pact CLI Docs](https://docs.pact.io/pact_broker/client_cli)