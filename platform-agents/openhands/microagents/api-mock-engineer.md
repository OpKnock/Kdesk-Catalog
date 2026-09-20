---
name: "api-mock-engineer"
description: "Designs mock API services for frontend development and tests using MSW (Mock Service Worker), with OpenAPI-driven fixtures and realistic latency profiles."
type: knowledge
triggers: ["api-mock-engineer", "msw-handlers", "worker-lifecycle"]
---

# api-mock-engineer

Designs mock API services for frontend development and tests using MSW (Mock Service Worker), with OpenAPI-driven fixtures and realistic latency profiles.

## Instructions

# API Mock Engineer

Builds mock API layers with Mock Service Worker.

## What This Skill Does
- Intercepts fetch/XHR at the network level with service workers
- Provides stateful mock databases with @mswjs/data
- Reuses the same handlers in dev, CI, and Playwright tests

## When to Use
- Frontend work blocked by an unfinished backend
- Removing flaky live-network calls from test suites
- Demo environments needing deterministic data

## Real Commands

```bash
npm install msw --save-dev
npx msw init public/ --save
```

## Handler Example

```js
import { http, HttpResponse, delay } from 'msw';
export const handlers = [
  http.get('/api/users', async () => {
    await delay(300);
    return HttpResponse.json(db.user.getAll());
  }),
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(db.user.create(body), { status: 201 });
  })
];
```

## Testing
- Start the server with setupServer from msw/node in vitest/jest
- Assert UI behavior without touching the network
- Verify 404 handlers produce the same error shapes as the real API

## Best Practices
- Keep handlers close to route definitions for easy diffing against OpenAPI
- Add delay() to surface loading states
- Enable onUnhandledRequest warnings in tests to catch gaps

## Capabilities

### msw-handlers
Set up MSW request handlers for browser and Node test environments

**Commands:**
- `npm install msw --save-dev`
- `npx msw init public/ --save`
- `npm install @mswjs/data`
- `node -e "const { http, HttpResponse } = require('msw'); console.log(typeof http.get)"`
- `curl -s http://localhost:3000/api/users -o /dev/null -w '%{http_code}\n'`

**Examples:**
- npx msw init public/ --save registers the service worker script
- const user = factory({ name: String, role: String }) builds a mock database
- http.get('/api/users', () => HttpResponse.json(db.user.getAll()))

### worker-lifecycle
Start and stop the mock server in tests and development

**Commands:**
- `npx msw init public/`
- `node test-setup.js`
- `npx vitest run`
- `curl -s http://localhost:3000/api/health | jq .`

**Examples:**
- -cli --help
- -api --help
