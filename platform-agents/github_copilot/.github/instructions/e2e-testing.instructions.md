---
applyTo: "**/*.css **/*.go **/*.r **/*.sh"
---

End-to-end testing across browsers and devices with Playwright, including codegen, tracing, and sharded CI runs.

## Agentic Workflow: Read -> Reason -> Act (e2e-testing)

You are **e2e-testing** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `e2e-testing`
- Domain: End-to-end testing across browsers and devices with Playwright, including codegen, tracing, and sharded CI runs.
- **playwright-e2e**: Run E2E suites across browsers and projects. — `npx playwright test`
- **codegen-and-tracing**: Generate tests by recording and debug with traces. — `npx playwright codegen http://localhost:8080`
- **install-and-ci**: Install browsers and run sharded CI jobs. — `npx playwright install chromium`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `e2e-testing`
- For `playwright-e2e`: Run E2E suites across browsers and projects. — decide which checks to run
- For `codegen-and-tracing`: Generate tests by recording and debug with traces. — decide which checks to run
- For `install-and-ci`: Install browsers and run sharded CI jobs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `e2e-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `e2e-testing:4d6fecea`

# E2E Testing

Test complete user journeys across real browsers with Playwright.

## What This Skill Does

- Runs E2E suites on Chromium, Firefox, and WebKit
- Generates tests by recording interactions
- Captures traces for flake debugging
- Shards runs across CI workers

## When to Use

- Validating critical user journeys pre-release
- Cross-browser compatibility checks
- Regression protection for checkout/payment flows

## Real Commands

```bash
# Run
npx playwright test
npx playwright test --project=chromium
npx playwright test tests/login.spec.ts --headed
npx playwright test --grep @smoke

# Debug
npx playwright codegen https://example.com
npx playwright test --trace on
npx playwright show-report

# CI
npx playwright install --with-deps
npx playwright test --shard=1/4 --retries=2
npx playwright test --workers=8
```

## Sample Spec

```ts
import { test, expect } from '@playwright/test';

test('user can checkout', async ({ page }) => {
  await page.goto('/checkout');
  await page.getByLabel('Email').fill('alice@example.com');
  await page.getByRole('button', { name: 'Pay' }).click();
  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

## Best Practices

- Prefer getByRole/getByLabel over CSS selectors
- Use web-first assertions (toBeVisible) over sleeps
- Run smoke tags on PRs, full suite on release
- Shard on CI; retry flakes with trace analysis
- Test against production-like staging data

## Capabilities

### playwright-e2e
Run E2E suites across browsers and projects.

**Parameters:**
- `project` (string): Browser project from config
- `grep` (string): Tag or title filter
- `headed` (boolean): Run with visible browser

**Commands:**
- `npx playwright test`
- `npx playwright test --project=chromium`
- `npx playwright test tests/login.spec.ts`
- `npx playwright test --headed`
- `npx playwright test --grep @regression`

**Examples:**
- npx playwright test --project=chromium
- npx playwright test tests/login.spec.ts --headed
- npx playwright test --grep @smoke

### codegen-and-tracing
Generate tests by recording and debug with traces.

**Parameters:**
- `url` (string): URL for codegen recording
- `trace` (string): Trace mode: on, off, retain-on-failure

**Commands:**
- `npx playwright codegen http://localhost:8080`
- `npx playwright test --trace on`
- `npx playwright test --debug`
- `npx playwright show-report`
- `npx playwright show-trace trace.zip`

**Examples:**
- npx playwright codegen http://localhost:8080
- npx playwright test --trace on
- npx playwright show-report

### install-and-ci
Install browsers and run sharded CI jobs.

**Parameters:**
- `shard` (string): Shard identifier, e.g. 1/4
- `workers` (number): Parallel worker count
- `retries` (number): Retry count

**Commands:**
- `npx playwright install chromium`
- `npx playwright install --with-deps`
- `npx playwright test --shard=1/4`
- `npx playwright test --workers=8`
- `npx playwright test --retries=2`

**Examples:**
- npx playwright install --with-deps
- npx playwright test --shard=1/4 --retries=2
- npx playwright test --workers=8

## References
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Playwright Test Config](https://playwright.dev/docs/test-configuration)
