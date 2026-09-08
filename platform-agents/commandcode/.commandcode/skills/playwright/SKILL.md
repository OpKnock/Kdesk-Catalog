---
name: "playwright"
description: "Writes and runs browser automation tests with Playwright: locators, fixtures, screenshots, and visual comparisons. Use when working with playwright testing, locators and assertions, fixtures and screenshots or when the user mentions playwright testing, locators and assertions, fixtures and screenshots."
license: "MIT"
compatibility: "Requires npx, page.getbyrole('button',, page.getbytestid('checkout-form, page.locator('[data-cy=price, page.screenshot({."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(npx:*) Bash(page.getByRole('button',:*) Bash(page.getByTestId('checkout-form'):*) Bash(page.locator('[data-cy=price]'):*) Bash(page.screenshot({:*)"
---

Writes and runs browser automation tests with Playwright: locators, fixtures, screenshots, and visual comparisons.

## Agentic Workflow: Read -> Reason -> Act (playwright)

You are **playwright** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `playwright`
- Domain: Writes and runs browser automation tests with Playwright: locators, fixtures, screenshots, and visual comparisons.
- **playwright-testing**: Run browser tests with projects and tags. — `npx playwright test`
- **locators-and-assertions**: Interact with pages using role and test-id locators. — `npx playwright test --debug`
- **fixtures-and-screenshots**: Use fixtures, screenshots, and storage state. — `npx playwright screenshot --device='iPhone 13' --full-page http://localhost:8080`
- Check `knowledge` and `prerequisites: npx, page.getbyrole('button',, page.getbytestid('checkout-form, page.locator('[data-cy=price`

### 2. Reason — think for `playwright`
- For `playwright-testing`: Run browser tests with projects and tags. — decide which checks to run
- For `locators-and-assertions`: Interact with pages using role and test-id locators. — decide which checks to run
- For `fixtures-and-screenshots`: Use fixtures, screenshots, and storage state. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `playwright` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `page.getByRole('button',` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `playwright:b7d0c869`

# Playwright

Browser automation and E2E testing for modern web apps.

## What This Skill Does

- Runs browser tests with role-based locators
- Captures screenshots and visual snapshots
- Uses fixtures for shared setup and auth state
- Emulates devices and network conditions

## When to Use

- E2E regression suites for web UIs
- Cross-browser compatibility checks
- Visual regression testing

## Real Commands

```bash
# Run
npx playwright test
npx playwright test tests/checkout.spec.ts --headed
npx playwright test --grep @smoke

# Debug
npx playwright test --debug
npx playwright test --trace on

# Screenshots
npx playwright screenshot --device='iPhone 13' --full-page https://example.com iphone.png
npx playwright test --update-snapshots

# Reports
npx playwright show-report
```

## Sample Spec

```ts
import { test, expect } from '@playwright/test';

test('adds item to cart', async ({ page }) => {
  await page.goto('/products/42');
  await page.getByRole('button', { name: 'Add to cart' }).click();
  await expect(page.getByTestId('cart-count')).toHaveText('1');
});
```

## Best Practices

- Prefer getByRole/getByLabel over CSS selectors
- Use data-testid for non-semantic elements
- Keep tests independent; reset state in beforeEach
- Run a smoke subset on PRs, full suite nightly
- Use fixtures to authenticate once and share storage state

## Capabilities

### playwright-testing
Run browser tests with projects and tags.

**Parameters:**
- `file` (string): Test file or directory
- `grep` (string): Test tag/title filter
- `headed` (boolean): Visible browser mode

**Commands:**
- `npx playwright test`
- `npx playwright test tests/checkout.spec.ts`
- `npx playwright test --project=chromium --grep @smoke`
- `npx playwright test --headed`
- `npx playwright test --grep-invert @slow`

**Examples:**
- npx playwright test tests/checkout.spec.ts
- npx playwright test --grep @smoke
- npx playwright test --headed

### locators-and-assertions
Interact with pages using role and test-id locators.

**Parameters:**
- `role` (string): ARIA role to locate
- `testId` (string): data-testid value

**Commands:**
- `npx playwright test --debug`
- `page.getByRole('button', { name: 'Submit' })`
- `page.getByTestId('checkout-form')`
- `page.locator('[data-cy=price]')`
- `npx playwright test --trace on`

**Examples:**
- page.getByRole('button', { name: 'Submit' }).click()
- expect(page.getByTestId('order-confirmed')).toBeVisible()
- npx playwright test --debug

### fixtures-and-screenshots
Use fixtures, screenshots, and storage state.

**Parameters:**
- `device` (string): Emulated device
- `updateSnapshots` (boolean): Update golden snapshots

**Commands:**
- `npx playwright screenshot --device='iPhone 13' --full-page http://localhost:8080 iphone.png`
- `page.screenshot({ path: 'checkout.png', fullPage: true })`
- `npx playwright test --update-snapshots`
- `npx playwright test --config=playwright.config.ts --reporter=list`
- `npx playwright show-report`

**Examples:**
- npx playwright screenshot --device='iPhone 13' --full-page http://localhost:8080 iphone.png
- npx playwright test --update-snapshots
- npx playwright show-report

## References
- [Playwright Introduction](https://playwright.dev/docs/intro)
- [Playwright Locators](https://playwright.dev/docs/locators)
