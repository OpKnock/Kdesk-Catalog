---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.{js,ts,jsx,tsx} **/*.{yaml,yml}"
---

# pact

Pact contract testing. Real pact CLI.

## Instructions

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
