---
name: "api-mock-engineer"
description: "Designs mock API services for frontend development and tests using MSW (Mock Service Worker), with OpenAPI-driven fixtures and realistic latency profiles. Use when working with msw handlers, worker lifecycle or when the user mentions msw handlers, worker lifecycle."
license: "MIT"
compatibility: "Requires prism, wiremock, msw, node.js, python, openapi. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(node:*) Bash(npm:*) Bash(npx:*)"
---

Designs mock API services for frontend development and tests using MSW (Mock Service Worker), with OpenAPI-driven fixtures and realistic latency profiles.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install msw --save-dev`, `npx msw init public/`
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

**Parameters:**
- `handlers-dir` (string): Directory containing MSW request handler modules
- `mock-db` (object): @mswjs/data model definitions for stateful mocking
- `delay` (integer): Artificial latency in milliseconds for realistic UX

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

## References
- [MSW Documentation](https://mswjs.io/docs/)
- [@mswjs/data](https://github.com/mswjs/data)
