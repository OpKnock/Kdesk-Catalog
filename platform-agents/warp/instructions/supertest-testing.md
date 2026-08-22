# supertest-testing

Tests Node.js HTTP APIs with supertest assertions against Express/Fastify servers, including auth and streaming.

## Instructions

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
