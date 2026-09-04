---
name: "api-sdk-unit-tests"
description: "Tests generated API SDKs: unit tests for clients, mock-server integration tests, generated code quality gates, and regression suites."
type: knowledge
triggers: ["api-sdk-unit-tests", "sdk-unit-tests", "integration-tests"]
---

# Api Sdk Unit Tests

Tests generated API SDKs: unit tests for clients, mock-server integration tests, generated code quality gates, and regression suites.

## Instructions

# API SDK Engineer v2 - Testing

SDK testing and validation.

## What This Skill Does
- Unit-tests client behavior with mocks
- Integration-tests against mock servers
- Gates SDK quality in CI

## When to Use
- Verifying generated clients
- Catching SDK regressions
- Testing error paths

## Real Commands

```bash
npm install vitest
npx vitest run tests/sdk.test.ts
npx @stoplight/prism-cli mock openapi.yaml -p 4010 &
node -e "const sdk=require('./sdk'); sdk.defaultClient.basePath='http://localhost:4010'; sdk.getUsers().then(r=>console.log(r.data.length))"
```

## Test Pattern

```ts
import nock from 'nock';
import { UsersApi } from '../sdk';

test('lists users', async () => {
  nock('https://api.example.com').get('/users').reply(200, [{ id: 1 }]);
  const api = new UsersApi();
  const res = await api.getUsers();
  expect(res.data).toHaveLength(1);
});
```

## Testing
- Cover success, 4xx, and 5xx paths
- Test pagination and auth headers
- Run coverage thresholds in CI

## Best Practices
- Keep tests independent of live APIs
- Test through the public SDK surface
- Regenerate mocks when specs change

## Capabilities

### sdk-unit-tests
Write unit tests for SDK client code

**Commands:**
- `npm install vitest`
- `npx vitest run tests/sdk.test.ts`
- `npx vitest run --coverage`
- `npm install nock`
- `node -e "const nock=require('nock'); nock('http://localhost:8080').get('/users').reply(200,[{id:1}]); fetch('https://api.example.com/users').then(r=>r.json()).then(console.log)"`

**Examples:**
- nock intercepts HTTP for client tests
- vitest run executes the SDK test suite
- --coverage reports branch coverage

### integration-tests
Run SDKs against a live mock server

**Commands:**
- `npx @stoplight/prism-cli mock openapi.yaml -p 4010 &`
- `node -e "const sdk=require('./sdk'); sdk.defaultClient.basePath='http://localhost:4010'; sdk.getUsers().then(r=>console.log(r.data.length))"`
- `npm test`
- `npx vitest run`

**Examples:**
- -cli --help
- -api --help
