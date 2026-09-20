---
type: agent_requested
description: "Contract testing APIs with Pact: consumer expectations, provider verification, and mock services with pact-js. Use when working with pact consumer, pact verify, api or when the user mentions pact consumer, pact verify, api."
---

Contract testing APIs with Pact: consumer expectations, provider verification, and mock services with pact-js.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @pact-foundation/pact @pact-foundation/pact-node`, `npx @pact-foundation/pact-cli verify --provider-base-url htt`
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

# Contract Testing (Pact)

Test that consumers and providers agree on the API contract.

## When to Use

- Proving API compatibility without full integration tests
- CI feedback on every consumer or provider change
- Replacing brittle end-to-end tests between teams

## Consumer Test

```bash
npm install @pact-foundation/pact @pact-foundation/pact-node
```

```js
const { PactV3 } = require('@pact-foundation/pact');
const provider = new PactV3({ consumer: 'WebApp', provider: 'UserService' });

describe('UserService contract', () => {
  it('returns a user', async () => {
    await provider.addInteraction({
      uponReceiving: 'a request for a user',
      withRequest: { method: 'GET', path: '/users/42' },
      willRespondWith: { status: 200, body: { id: 42, name: 'alice' } },
    });
    await provider.executeTest(async (mockServer) => {
      const res = await fetch(`${mockServer.url}/users/42`);
      expect(await res.json()).toEqual({ id: 42, name: 'alice' });
    });
  });
});
```

```bash
npx jest --config jest.config.js
ls pacts/
```

## Provider Verification

```bash
npx @pact-foundation/pact-cli verify \
  --provider-base-url http://localhost:8080 \
  --pact-urls ./pacts/*.json
```

## Publish and Gate

```bash
npx @pact-foundation/pact-cli publish ./pacts --broker-base-url http://localhost:9292 --consumer-version 1.0.0
npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.0 --to-environment production
```

## Testing

```bash
# Break the provider response and re-run verification to see a mismatch
npm run test:provider
```

## Best Practices

- Consumers define expectations; providers verify them
- Use provider states for data setup
- Run consumer tests fast in unit test suites
- Publish pacts from CI with the commit SHA as version
- Verify against latest pact of every consumer
- Gate deploys with can-i-deploy
- Keep matchers loose enough for safe evolution

## Capabilities

### pact-consumer
Write consumer contract tests with pact-js against a mock provider

**Parameters:**
- `consumer_name` (string): Consumer application name
- `provider_name` (string): Provider application name

**Commands:**
- `npm install @pact-foundation/pact @pact-foundation/pact-node`
- `npx jest --config jest.config.js`
- `npm test`
- `npm run test:contract`

**Examples:**
- npm install @pact-foundation/pact && npx jest --config jest.config.js
- npm test -- --runInBand
- npx jest contracts/ -t 'a request for a user'

### pact-verify
Run provider verification against published pacts and mock the provider for local checks

**Parameters:**
- `pact_urls` (string): Glob or URL list of pact files
- `provider_base_url` (string): Base URL of the running provider

**Commands:**
- `npx @pact-foundation/pact-cli verify --provider-base-url http://localhost:8080 --pact-urls ./pacts/*.json`
- `npx @pact-foundation/pact-cli publish ./pacts --broker-base-url http://localhost:9292 --consumer-version 1.0.0`
- `npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.0 --to-environment production`
- `npm run test:provider`

**Examples:**
- npx @pact-foundation/pact-cli verify --provider-base-url http://localhost:8080 --pact-urls ./pacts/*.json
- npx @pact-foundation/pact-cli can-i-deploy --pacticipant WebApp --version 1.0.0 --to-environment production
- npx @pact-foundation/pact-cli publish ./pacts --broker-base-url http://localhost:9292 --consumer-version 1.0.0

## References
- [Pact Docs](https://docs.pact.io/)
- [Pact JS GitHub](https://github.com/pact-foundation/pact-js)