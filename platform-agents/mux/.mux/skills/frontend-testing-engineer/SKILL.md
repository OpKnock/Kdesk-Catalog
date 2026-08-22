---
name: "frontend-testing-engineer"
description: "Owns the frontend quality program: E2E suites with Playwright, accessibility audits with axe, and performance budgets with Lighthouse CI."
---

# frontend-testing-engineer

Owns the frontend quality program: E2E suites with Playwright, accessibility audits with axe, and performance budgets with Lighthouse CI.

## Instructions

# Frontend Testing Engineering

Run a measurable frontend quality program: E2E, accessibility, and performance.

## When to Use

- Establishing the frontend test strategy for a product
- Debugging flaky suites and reducing CI time
- Enforcing a11y and performance budgets per route

## E2E suite design

```bash
npx playwright install --with-deps
npx playwright test --project=chromium --shard=1/4
npx playwright show-trace trace.zip
```

Shard by project in CI: 4 workers each running one shard of the suite.

## Accessibility gates

```bash
npx axe https://app.example.com --exit
```

Run axe on every deployed preview; fail the check on serious/critical violations.

## Performance budgets

```lighthouserc.js
module.exports = {
  ci: {
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }]
      }
    },
    collect: { numberOfRuns: 3, startServerCommand: 'npm run preview' }
  }
};
```

```bash
npx @lhci/cli autorun --config=lighthouserc.js
```

## Flake management

- Always record traces on retry.
- Fix root causes; never blanket-disable tests.
- Tag smoke tests for fast PR feedback and keep the full suite for merge.

## Best practices

- Test user journeys, not implementation selectors.
- Store auth state for repeatable authenticated flows.
- Weekly review of flaky-test report from CI.
- Keep a testability budget: testable code beats untestable hacks.

## Capabilities

### e2e
Run and debug Playwright end-to-end suites at scale.

**Commands:**
- `npx playwright install --with-deps`
- `npx playwright test --project=chromium`
- `npx playwright test --shard=1/4 --project=all`
- `npx playwright show-trace trace.zip`
- `npx playwright codegen --save-storage=.auth/state.json http://localhost:8080`

**Examples:**
- npx playwright test tests/e2e --grep-invert '@smoke'
- npx playwright test --retries=2 --project=webkit
- npx playwright show-trace test-results/trace.zip

### a11y-perf
Audit accessibility and performance with axe and Lighthouse.

**Commands:**
- `npx axe http://localhost:8080 --exit`
- `npx @lhci/cli autorun --config=lighthouserc.js`
- `npx lighthouse http://localhost:8080 --view --quiet`
- `npx @lhci/cli healthcheck`
- `npx @lhci/cli collect --numberOfRuns=3`

**Examples:**
- npx axe http://localhost:8080/login --exit --chrome-options="--headless"
- npx @lhci/cli autorun --config=lighthouserc.js --upload.target=temporary-public-storage
- npx lighthouse http://localhost:8080 --output=json --output-path=lhr.json
