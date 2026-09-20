---
type: agent_requested
description: "Tests Express APIs with supertest and jest: request assertions, route coverage, snapshot testing, and CI-friendly test configuration. Use when working with supertest, assertion patterns or when the user mentions supertest, assertion patterns."
---

Tests Express APIs with supertest and jest: request assertions, route coverage, snapshot testing, and CI-friendly test configuration.

## Agentic Workflow: Read -> Reason -> Act (api-test-supertest)

You are **Api Test Supertest** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-test-supertest`
- Domain: Tests Express APIs with supertest and jest: request assertions, route coverage, snapshot testing, and CI-friendly test configuration.
- **supertest**: Test HTTP APIs in-process with supertest — `npm install -D supertest jest`
- **assertion-patterns**: Assert status, body, and headers — `node -e "const request=require('supertest'); console.log(typeof request)"`
- Check `knowledge` and `prerequisites: jest, pytest, postman`

### 2. Reason — think for `api-test-supertest`
- For `supertest`: Test HTTP APIs in-process with supertest — decide which checks to run
- For `assertion-patterns`: Assert status, body, and headers — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-test-supertest` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-test-supertest:ddcd3df7`

# API Test v3 - Supertest/Jest

In-process API testing.

## What This Skill Does
- Tests routes without binding a port
- Asserts status, bodies, and headers
- Reports coverage per route

## When to Use
- Node/Express API suites
- Fast unit-style endpoint tests
- Route regression coverage

## Real Commands

```bash
npm install -D supertest jest
npx jest test/api.test.js --verbose
npx jest --coverage --collectCoverageFrom='routes/**/*.js'
```

## Test Example

```js
const request = require('supertest');
const app = require('../app');

test('creates a user', async () => {
  const res = await request(app).post('/api/users').send({ name: 'alice' });
  expect(res.status).toBe(201);
  expect(res.body.id).toBeDefined();
});
```

## Testing
- Cover success and error paths per route
- Use coverage thresholds in CI
- Keep tests independent with in-memory DBs


## Best Practices
- Export the app separately from the server
- Test through the HTTP interface
- Group tests by route resource

## Capabilities

### supertest
Test HTTP APIs in-process with supertest

**Parameters:**
- `test-file` (string): Test file path
- `coverage` (boolean): Collect coverage
- `test-name` (string): Filter by test name

**Commands:**
- `npm install -D supertest jest`
- `npx jest test/api.test.js --verbose`
- `npx jest --coverage --collectCoverageFrom='routes/**/*.js'`
- `npx jest -t 'creates a user'`
- `npm test`

**Examples:**
- supertest(app).get('/api/users') mounts the app in-process
- jest --coverage reports route coverage
- -t filters to a single test name

### assertion-patterns
Assert status, body, and headers

**Commands:**
- `node -e "const request=require('supertest'); console.log(typeof request)"`
- `npx jest test/api.test.js --runInBand`
- `npx jest --watch`

**Examples:**
- -cli --help
- -api --help

## References
- [Supertest Docs](https://github.com/ladjs/supertest)
- [Jest Docs](https://jestjs.io/docs/getting-started)