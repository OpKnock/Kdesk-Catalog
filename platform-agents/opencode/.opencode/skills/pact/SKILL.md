---
name: "pact"
description: "Pact contract testing. Real pact CLI. Use when working with pact, testing or when the user mentions pact, testing."
---

Pact contract testing. Real pact CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -D @pact-foundation/pact`
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

# Pact

Pact contract testing using real CLI.

## When to Use

- Consumer-driven contracts
- Provider verification
- Contract testing
- Microservice testing

## Commands

```bash
# Install (Node)
npm install -D @pact-foundation/pact

# Install (CLI)
brew install pact-foundation/pact/pact-cli

# Verify
pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/consumer-provider.json

# Publish
pact-broker publish ./pacts --broker-base-url=http://localhost:9292

# Can I deploy
pact-broker can-i-deploy --pacticipant=consumer --version=1.0.0 --broker-base-url=http://localhost:9292
```

## Consumer Test (JavaScript)

```javascript
// consumer.test.js
const { Pact } = require('@pact-foundation/pact');
const path = require('path');

const provider = new Pact({
  consumer: 'MyConsumer',
  provider: 'MyProvider',
  port: 1234,
  log: path.resolve(process.cwd(), 'logs', 'pact.log'),
  dir: path.resolve(process.cwd(), 'pacts'),
  spec: 2,
});

describe('User API Consumer', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());
  
  it('returns user', async () => {
    await provider.addInteraction({
      state: 'user with id 123 exists',
      uponReceiving: 'a request for user 123',
      withRequest: {
        method: 'GET',
        path: '/users/123',
        headers: { Accept: 'application/json' },
      },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: '123',
          name: 'John',
          email: 'john@example.com',
        },
      },
    });
    
    // Make request to mock server
    const response = await fetch('http://localhost:1234/users/123');
    expect(response.status).toBe(200);
  });
});
```

## Provider Verification (JavaScript)

```javascript
// provider.test.js
const { Verifier } = require('@pact-foundation/pact');
const path = require('path');

describe('User API Provider', () => {
  it('verifies contracts', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:8080',
      pactUrls: [path.resolve(process.cwd(), 'pacts', 'myconsumer-myprovider.json')],
      provider: 'MyProvider',
    });
    
    await verifier.verifyProvider();
  });
});
```

## Examples

```bash
# Verify
pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/consumer-provider.json

# Publish
pact-broker publish ./pacts --broker-base-url=http://localhost:9292
```

## CI/CD

```yaml
# GitHub Actions
- name: Verify Pact
  run: |
    pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/consumer-provider.json

# GitLab CI
pact:
  stage: test
  script:
    - pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/consumer-provider.json
```

## Capabilities

### pact
Pact contract testing. Real pact CLI.

**Parameters:**
- `broker-base-url` (boolean): CLI flag --broker-base-url observed in capability commands
- `pact-url` (boolean): CLI flag --pact-url observed in capability commands
- `provider-base-url` (boolean): CLI flag --provider-base-url observed in capability commands

**Commands:**
- `npm install -D @pact-foundation/pact`
- `brew install pact-foundation/pact/pact-cli`
- `pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/consumer-provider.json`
- `pact-broker publish ./pacts --broker-base-url=http://localhost:9292`
- `pact-broker can-i-deploy --pacticipant=consumer --version=1.0.0 --broker-base-url=http://localhost:9292`
- `pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/consumer-provider.json`
- `pact-broker publish ./pacts --broker-base-url=http://localhost:9292`

**Examples:**
- npm install -D @pact-foundation/pact
- brew install pact-foundation/pact/pact-cli
- pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/consumer-provider.json

## References
- [pact Skill Documentation](skills/testing/pact.md)
