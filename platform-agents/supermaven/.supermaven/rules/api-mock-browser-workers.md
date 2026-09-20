# Api Mock Browser Workers

Implements browser and Node mock layers with MSW combined with Playwright for E2E mocking: persistent session state, resolver utilities, and test isolation.

## Instructions

# API Mock v4 - MSW + Playwright

Browser-grade mocking with MSW and E2E coverage.

## What This Skill Does
- Intercepts app traffic in the browser with service workers
- Shares handlers between dev, unit, and Playwright E2E runs
- Isolates test data per test with scoped handlers

## When to Use
- E2E suites that must not depend on live backends
- Reproducing specific API states in UI tests
- Keeping dev and test mocks from a single source

## Real Commands

```bash
npm install msw --save-dev
npx msw init public/
```

## Playwright Integration

```ts
import { test as base } from '@playwright/test';
import { createWorkerFixture } from '@playwright/msw';
export const test = base.extend({
  worker: createWorkerFixture(handlers)
});
```

## Testing
- Assert network responses from devtools/network panel match handlers
- Verify onUnhandledRequest: 'error' surfaces missing mocks
- Reset server state between Playwright tests

## Best Practices
- Version the worker script with the app bundle
- Use dynamic handlers for time-dependent data
- Keep handler modules framework-agnostic for reuse

## Capabilities

### browser-workers
Configure MSW service workers in a Vite/Next.js application

**Commands:**
- `npm install msw --save-dev`
- `npx msw init public/`
- `npm run build`
- `curl -s http://localhost:4173 -o /dev/null -w '%{http_code}\n'`
- `npx playwright install chromium`

**Examples:**
- npx msw init public/ writes the worker script served at /mockServiceWorker.js
- import { setupWorker } from 'msw/browser' starts the browser worker
- worker.start({ onUnhandledRequest: 'error' }) fails loudly on unmocked calls

### e2e-integration
Reuse MSW handlers inside Playwright E2E tests

**Commands:**
- `npm install @playwright/test msw`
- `npx playwright test tests/api-flows.spec.ts --project=chromium`
- `npx playwright test --ui`
- `npx playwright show-report`

**Examples:**
- -cli --help
- -api --help