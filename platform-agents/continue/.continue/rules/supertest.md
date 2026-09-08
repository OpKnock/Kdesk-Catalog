---
name: "Supertest"
description: "Write and run HTTP API tests with it and jest. Use when working with supertest http tests, api or when the user mentions supertest http tests, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Write and run HTTP API tests with it and jest.

## Agentic Workflow: Read -> Reason -> Act (supertest)

You are **Supertest** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `supertest`
- Domain: Write and run HTTP API tests with it and jest.
- **supertest-http-tests**: Write and run HTTP API tests with supertest and jest — `npm init -y && npm i -D supertest jest`
- Check `knowledge` and `prerequisites: node, npm, npx`

### 2. Reason — think for `supertest`
- For `supertest-http-tests`: Write and run HTTP API tests with supertest and jest — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `supertest` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `supertest:e4243697`

# Supertest

Hand-crafted skill for HTTP-level API testing in Node with supertest.

## What this skill does

- Attaches supertest to an Express/Fastify app without a live server
- Chains status, header, and body expectations
- Runs targeted tests and coverage with jest

## When to use

- Testing Express routes in-process and fast
- Verifying middleware behavior (auth, validation) at the HTTP layer
- Filling the gap between unit tests and E2E suites

## Real commands

```bash
# Setup
npm init -y && npm i -D supertest jest

# Run the whole suite
npx jest --verbose

# Run one test by name
npx jest tests/api.test.js -t 'should return 200'

# Coverage
npx jest --coverage

# One-liner smoke test
node -e 'const request = require("supertest"); request(require("./app")).get("/health").expect(200).end(() => console.log("ok"))'
```

## Test example

```js
const request = require("supertest");
const app = require("../app");

describe("GET /api/users", () => {
  it("should return 200 with JSON", async () => {
    await request(app)
      .get("/api/users")
      .set("Accept", "application/json")
      .expect("Content-Type", /json/)
      .expect(200)
      .expect((res) => {
        expect(Array.isArray(res.body)).toBe(true);
      });
  });
});
```

## Testing

```bash
npx jest tests/api.test.js -t 'should return 200'
npx jest --verbose --watch
```

## Best practices

- Test behaviors users hit, not implementation details
- Use .set() for headers and .send() for bodies on mutating calls
- Mock external services (DB, HTTP) so tests stay deterministic

## Capabilities

### supertest-http-tests
Write and run HTTP API tests with supertest and jest

**Parameters:**
- `app` (string): Express app export to attach supertest to
- `test_file` (string): Test file path for jest
- `path` (string): Endpoint under test

**Commands:**
- `npm init -y && npm i -D supertest jest`
- `npx jest --verbose`
- `npx jest tests/api.test.js -t 'should return 200'`
- `npx jest --coverage`
- `node -e 'const request = require("supertest"); const app = require("./app"); request(app).get("/").expect(200).end((err,res) => { if (err) throw err; console.log(res.status); })'`

**Examples:**
- npx jest tests/api.test.js -t 'should return 200'
- npx jest --verbose
- node -e 'const request = require("supertest"); request(require("./app")).get("/health").expect(200).end(() => console.log("ok"))'

## References
- [Supertest repo](https://github.com/ladjs/supertest)
- [Jest docs](https://jestjs.io/docs/getting-started)