---
name: "frontend-testing"
description: "Tests frontend applications end-to-end and at the component level with Playwright, Cypress, and Vitest. Use when working with playwright, vitest, frontend or when the user mentions playwright, vitest, frontend."
---

Tests frontend applications end-to-end and at the component level with Playwright, Cypress, and Vitest.

## Agentic Workflow: Read -> Reason -> Act (frontend-testing)

You are **Frontend Testing** (frontend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `frontend-testing`
- Domain: Tests frontend applications end-to-end and at the component level with Playwright, Cypress, and Vitest.
- **playwright**: Write and run browser end-to-end tests with Playwright. — `npx playwright install --with-deps`
- **vitest**: Run fast component and unit tests with Vitest. — `npx vitest run`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `frontend-testing`
- For `playwright`: Write and run browser end-to-end tests with Playwright. — decide which checks to run
- For `vitest`: Run fast component and unit tests with Vitest. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `frontend-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `frontend-testing:36cd193e`

# Frontend Testing

Layer unit, component, and end-to-end tests to catch regressions at every level.

## When to Use

- Verifying critical user journeys (login, checkout)
- Regression testing across browsers and viewports
- Locking down component behavior before refactors

## E2E with Playwright

```bash
npx playwright install --with-deps
npx playwright test
npx playwright codegen https://example.com
npx playwright show-report
```

Write tests with user-visible queries:

```typescript
await page.goto('/checkout');
await page.getByRole('button', { name: 'Place order' }).click();
await expect(page.getByText('Order confirmed')).toBeVisible();
```

## Component tests with Vitest + Testing Library

```typescript
import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';

test('shows error when email invalid', async () => {
  render(<SignupForm />);
  await screen.getByLabelText('Email').then(el => {
    // fireEvent.change, expect error message
  });
});
```

```bash
npx vitest run --coverage
```

## Parallelism and flakiness

- Prefer `getByRole`/`getByLabel` over selectors on CSS classes.
- Use `expect(...).toPass()` for slow async assertions in Cypress.
- Run unit tests on every commit; E2E on PRs and nightly.

## Best practices

- Keep E2E suites small and business-critical only.
- Test mobile viewport at least for the top 3 journeys.
- Record videos/traces on failure only, to save CI time.
- Aim for > 80% coverage on logic-heavy utilities and state reducers.

## Capabilities

### playwright
Write and run browser end-to-end tests with Playwright.

**Parameters:**
- `project` (string): Browser project: chromium, firefox, webkit
- `grep` (string): Run only tests matching a pattern
- `workers` (number): Parallel worker count

**Commands:**
- `npx playwright install --with-deps`
- `npx playwright test`
- `npx playwright test --project=chromium --headed`
- `npx playwright codegen http://localhost:8080`
- `npx playwright show-report`

**Examples:**
- npx playwright test tests/e2e/checkout.spec.ts --grep 'checkout'
- npx playwright test --project=firefox --workers=4
- npx playwright codegen --viewport-size '390,844' http://localhost:8080

### vitest
Run fast component and unit tests with Vitest.

**Parameters:**
- `coverage` (string): Enable coverage collection
- `reporter` (string): default, json, junit, dot
- `changed` (string): Test only files changed vs branch

**Commands:**
- `npx vitest run`
- `npx vitest run --coverage`
- `npx vitest --ui`
- `npx vitest run tests/unit/button.test.tsx`
- `npx vitest watch`

**Examples:**
- npx vitest run --coverage --reporter=json --outputFile=coverage.json
- npx vitest run --changed main
- npx vitest watch --exclude '**/e2e/**'

## References
- [Playwright Docs](https://playwright.dev/docs/intro)
- [Cypress Docs](https://docs.cypress.io/)
- [Vitest Docs](https://vitest.dev/guide/)
