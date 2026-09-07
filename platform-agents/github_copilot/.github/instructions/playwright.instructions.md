---
applyTo: "**/*.css **/*.go **/*.r **/*.sh"
---

Writes and runs browser automation tests with Playwright: locators, fixtures, screenshots, and visual comparisons.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx playwright test`, `npx playwright test --debug`
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
