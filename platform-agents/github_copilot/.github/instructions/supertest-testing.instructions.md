---
applyTo: "**/*.json **/*.r **/*.sh"
---

Tests Node.js HTTP APIs with supertest assertions against Express/Fastify servers, including auth and streaming.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx jest test/api.test.js`, `request(app).get('/api/users').expect(200)`
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

# supertest

HTTP assertions for Node.js APIs.

## What This Skill Does

- Sends requests to an app instance without binding ports
- Asserts status, headers, and bodies fluently
- Tests auth headers and JSON content
- Integrates with jest/mocha runners

## When to Use

- Unit-level API tests for Express/Fastify apps
- Contract checks on endpoints
- Regression tests for handlers

## Real Commands

```bash
# With jest
npx jest test/api.test.js

# With mocha
npx mocha test/api.test.js

# Direct
node test/api.test.js
```

## Sample Test

```js
const request = require('supertest');
const app = require('../app');

describe('GET /api/users', () => {
  it('returns users', async () => {
    const res = await request(app)
      .get('/api/users')
      .set('Authorization', 'Bearer tok')
      .expect(200)
      .expect('Content-Type', /json/);
    expect(res.body.users).toBeInstanceOf(Array);
  });

  it('rejects unauthenticated', async () => {
    await request(app).get('/api/users').expect(401);
  });
});
```

## Best Practices

- Import the app, not a running server
- Assert status AND body shape
- Test auth and error paths, not just happy paths
- Use .expect('Content-Type', /json/) for contract
- Keep tests independent of network and databases

## Capabilities

### supertest-api-tests
Write and run API assertions with supertest.

**Parameters:**
- `testFile` (string): Test file path
- `runner` (string): Test runner: jest, mocha, node

**Commands:**
- `npx jest test/api.test.js`
- `npx mocha test/api.test.js`
- `node test/api.test.js`
- `npm test -- --runInBand`

**Examples:**
- npx jest test/api.test.js
- npx mocha test/api.test.js
- npm test

### request-assertions
Chain requests and assert responses.

**Parameters:**
- `method` (string): HTTP method
- `path` (string): Endpoint path
- `body` (object): Request payload

**Commands:**
- `request(app).get('/api/users').expect(200)`
- `request(app).post('/api/users').send({ name: 'alice' }).expect(201)`
- `request(app).get('/api/users').set('Authorization', 'Bearer tok').expect(200)`
- `request(app).get('/api/users').expect('Content-Type', /json/)`
- `request(app).get('/api/stream').pipe(process.stdout)`

**Examples:**
- request(app).get('/api/users').expect(200, { users: [] })
- request(app).post('/api/users').send({ name: 'alice' }).expect(201)
- request(app).get('/api/users').set('Authorization', 'Bearer tok').expect(200)

## References
- [supertest GitHub](https://github.com/ladjs/supertest)
- [supertest npm](https://www.npmjs.com/package/supertest)
