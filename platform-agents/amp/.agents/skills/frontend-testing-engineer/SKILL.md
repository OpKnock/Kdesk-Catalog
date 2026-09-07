---
name: "frontend-testing-engineer"
description: "Owns the frontend quality program: E2E suites with Playwright, accessibility audits with axe, and performance budgets with Lighthouse CI. Use when working with e2e, a11y perf or when the user mentions e2e, a11y perf."
license: "MIT"
compatibility: "Requires jest, react-testing-library, cypress, playwright, storybook, chromatic."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

Owns the frontend quality program: E2E suites with Playwright, accessibility audits with axe, and performance budgets with Lighthouse CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx playwright install --with-deps`, `npx axe http://localhost:8080 --exit`
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

**Parameters:**
- `project` (string): Browser project to run
- `shard` (string): Test shard like 1/4 for parallel CI
- `retries` (number): Flake retry count

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

**Parameters:**
- `url` (string): URL to audit
- `exit` (string): Exit non-zero when violations found
- `config` (string): Lighthouse CI config file

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

## References
- [Playwright Test Runner](https://playwright.dev/docs/test-intro)
- [axe-core](https://github.com/dequelabs/axe-core)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
