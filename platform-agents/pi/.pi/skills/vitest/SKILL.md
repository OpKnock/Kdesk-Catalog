---
name: "vitest"
description: "Runs Vite-native unit tests with Vitest: watch mode, UI, coverage, mocking, and snapshot updates. Use when working with vitest runs, coverage and ui, mocking and config, testing or when the user mentions vitest runs, coverage and ui, mocking and config, testing."
license: "MIT"
compatibility: "Requires npx."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

Runs Vite-native unit tests with Vitest: watch mode, UI, coverage, mocking, and snapshot updates.

## Agentic Workflow: Read -> Reason -> Act (vitest)

You are **vitest** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `vitest`
- Domain: Runs Vite-native unit tests with Vitest: watch mode, UI, coverage, mocking, and snapshot updates.
- **vitest-runs**: Run tests in watch or one-shot mode. — `npx vitest`
- **coverage-and-ui**: Coverage reports and interactive UI. — `npx vitest run --coverage`
- **mocking-and-config**: Mock modules and configure environments. — `npx vitest run --environment=jsdom`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `vitest`
- For `vitest-runs`: Run tests in watch or one-shot mode. — decide which checks to run
- For `coverage-and-ui`: Coverage reports and interactive UI. — decide which checks to run
- For `mocking-and-config`: Mock modules and configure environments. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `vitest` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `vitest:0b4d4cfd`

# Vitest

Fast, Vite-native unit testing for JS/TS.

## What This Skill Does

- Runs tests in watch or one-shot mode
- Uses Vite transforms for instant startup
- Produces coverage with thresholds
- Mocks modules and supports jsdom environments


## When to Use

- Vite/React/Vue project unit tests
- Fast iteration with watch mode
- Snapshot testing for components

## Real Commands

```bash
# Run
npx vitest
npx vitest run
npx vitest run tests/foo.test.ts
npx vitest --changed

# Coverage
npx vitest run --coverage
npx vitest run --coverage.thresholds.lines=80

# Env and UI
npx vitest run --environment=jsdom
npx vitest --ui

# Snapshots
npx vitest --update
```

## Sample Test

```ts
import { describe, it, expect, vi } from 'vitest';
import { fetchUser } from './api';

vi.mock('./api', () => ({
  fetchUser: vi.fn(() => Promise.resolve({ name: 'alice' }))
}));

describe('user card', () => {
  it('renders the name', async () => {
    const name = await fetchUser(1).then(u => u.name);
    expect(name).toBe('alice');
  });
});
```

## Best Practices

- Use vitest run in CI; watch locally
- Set coverage thresholds in config
- Mock at module boundaries, not inside tests
- Prefer jsdom over full browser for component tests
- Run --changed in pre-push hooks

## Capabilities

### vitest-runs
Run tests in watch or one-shot mode.

**Parameters:**
- `file` (string): Test file path
- `changed` (boolean): Run only changed files
- `reporter` (string): Reporter: default, verbose, json

**Commands:**
- `npx vitest`
- `npx vitest run`
- `npx vitest run tests/foo.test.ts`
- `npx vitest run --reporter=verbose`
- `npx vitest --changed`

**Examples:**
- npx vitest
- npx vitest run tests/foo.test.ts
- npx vitest --changed

### coverage-and-ui
Coverage reports and interactive UI.

**Parameters:**
- `coverage` (boolean): Enable coverage
- `thresholds` (object): Coverage thresholds
- `update` (boolean): Update snapshots

**Commands:**
- `npx vitest run --coverage`
- `npx vitest run --coverage.thresholds.lines=80`
- `npx vitest --ui`
- `npx vitest run --coverage.reporter=lcov`
- `npx vitest --update`

**Examples:**
- npx vitest run --coverage
- npx vitest --ui
- npx vitest run --coverage.thresholds.lines=80

### mocking-and-config
Mock modules and configure environments.

**Parameters:**
- `environment` (string): Test environment: node, jsdom, happy-dom
- `testNamePattern` (string): Test name filter

**Commands:**
- `npx vitest run --environment=jsdom`
- `npx vitest run --testNamePattern=login`
- `npx vitest run --config vitest.config.ts`
- `npx vitest --pool=forks`
- `npx vitest run --sequence.shuffle`

**Examples:**
- npx vitest run --environment=jsdom
- npx vitest run --testNamePattern=login
- npx vitest run --sequence.shuffle

## References
- [Vitest Documentation](https://vitest.dev/guide/)
- [Vitest CLI Reference](https://vitest.dev/guide/cli.html)
