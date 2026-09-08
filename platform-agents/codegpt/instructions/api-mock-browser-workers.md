Implements browser and Node mock layers with MSW combined with Playwright for E2E mocking: persistent session state, resolver utilities, and test isolation.

## Agentic Workflow: Read -> Reason -> Act (api-mock-browser-workers)

You are **Api Mock Browser Workers** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-mock-browser-workers`
- Domain: Implements browser and Node mock layers with MSW combined with Playwright for E2E mocking: persistent session state, resolver utilities, and test isolation.
- **browser-workers**: Configure MSW service workers in a Vite/Next.js application — `npm install msw --save-dev`
- **e2e-integration**: Reuse MSW handlers inside Playwright E2E tests — `npm install @playwright/test msw`
- Check `knowledge` and `prerequisites: prism, wiremock, msw`

### 2. Reason — think for `api-mock-browser-workers`
- For `browser-workers`: Configure MSW service workers in a Vite/Next.js application — decide which checks to run
- For `e2e-integration`: Reuse MSW handlers inside Playwright E2E tests — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-mock-browser-workers` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-mock-browser-workers:883a8e2a`

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

**Parameters:**
- `worker-dir` (string): Directory that serves the service worker script
- `onUnhandledRequest` (string): warn | error | bypass for unmatched requests
- `quiet` (boolean): Suppress worker console output

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

## References
- [MSW Browser Docs](https://mswjs.io/docs/basics/mocking/browser)
- [Playwright Test Docs](https://playwright.dev/docs/test-intro)
