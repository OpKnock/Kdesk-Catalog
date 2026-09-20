# Frontend Testing

Tests frontend applications end-to-end and at the component level with Playwright, Cypress, and Vitest.

## Instructions

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
