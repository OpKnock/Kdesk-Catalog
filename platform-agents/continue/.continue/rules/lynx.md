---
name: "Lynx"
description: "End-to-end and unit testing with the Lynx test framework, writing assertions in plain JavaScript with instant watch mode."
globs: ["**/*.css", "**/*.java", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Lynx

End-to-end and unit testing with the Lynx test framework, writing assertions in plain JavaScript with instant watch mode.

## Instructions

# Lynx

Lynx is a fast end-to-end and unit test framework for JavaScript that runs in watch
mode by default and needs zero config for most projects.

## When to Use

- End-to-end tests that drive a real browser
- Unit tests with instant reload during development
- Snapshot testing of UI output

## Real Commands

```bash
# Install
npm install --save-dev @lynx-js/lynx

# Run all tests once
npx lynx

# Watch mode (default during development)
npx lynx --watch

# Visible browser for E2E debugging
npx lynx --headed

# Run a specific file
npx lynx run tests/e2e/auth.spec.js

# Refresh snapshots after an intentional change
npx lynx --update-snapshots

# Different browser engine
npx lynx --browser=webkit
```

## Example Test

```js
import { test, expect, browser } from '@lynx-js/lynx';

test('adds a todo', async () => {
  const page = await browser.open('https://example.com/todos');
  await page.fill('[data-testid=new-todo]', 'write tests');
  await page.click('button[type=submit]');
  await expect(page).toHaveText('.todo-item', 'write tests');
});
```

## CI

```yaml
- name: E2E
  run: npx lynx --browser=chromium
```

## Best Practices

- Use `--headed` only for debugging; CI runs headless
- Keep E2E tests in `tests/e2e/` and unit tests in `tests/unit/`
- Prefer stable data-testid selectors over CSS classes
- Update snapshots deliberately, then review the diff

## Capabilities

### lynx-tests
Run, watch, and snapshot-test with the Lynx framework for browser and Node tests

**Commands:**
- `npx lynx --watch`
- `npx lynx --headed`
- `npx lynx run tests/e2e/`
- `npx lynx --update-snapshots`
- `npx lynx --browser=webkit`

**Examples:**
- npx lynx --headed tests/auth.spec.js
- npx lynx --watch --filter login
- npx lynx --update-snapshots tests/snapshots/