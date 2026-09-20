---
type: agent_requested
description: "End-to-end and unit testing with the Lynx test framework, writing assertions in plain JavaScript with instant watch mode. Use when working with lynx tests, code quality or when the user mentions lynx tests, code quality."
---

End-to-end and unit testing with the Lynx test framework, writing assertions in plain JavaScript with instant watch mode.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx lynx --watch`
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

**Parameters:**
- `headed` (boolean): Run browser tests with a visible UI window
- `filter` (string): Run only tests whose names match the pattern
- `browser` (string): Browser engine: chromium, firefox, or webkit

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

## References
- [Lynx E2E framework docs](https://github.com/stackblitz/lynx)
- [Lynx CLI reference](https://github.com/stackblitz/lynx/blob/main/README.md)