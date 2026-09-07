---
name: "cypress"
description: "Open, run, and filter it tests. Parallelize runs and record to it Cloud. Component testing and debugging helpers. recording. Use when working with cypress runs, parallel and record, component and debug, testing or when the user mentions cypress runs, parallel and record, component and debug, testing."
---

Open, run, and filter it tests. Parallelize runs and record to it Cloud. Component testing and debugging helpers. recording.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx cypress open`, `npx cypress run --record --key $CYPRESS_RECORD_KEY`
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

# Cypress

Fast, reliable E2E and component testing for web apps.

## What This Skill Does

- Runs E2E suites in headed/interactive mode
- Filters specs and tests with CLI flags
- Parallelizes runs and records to Cypress Cloud
- Writes resilient selectors and custom commands

## When to Use

- Full user-journey regression suites
- Visual and component testing
- PR gating for web frontends

## Real Commands

```bash
# Interactive and headless
npx cypress open
npx cypress run --browser chrome
npx cypress run --spec cypress/e2e/login.cy.js

# Cloud and parallel
npx cypress run --record --key $CYPRESS_RECORD_KEY
npx cypress run --parallel --record --group chrome

# Component and config
npx cypress run --component
npx cypress run --env grep='login'
npx cypress run --config video=false
```

## Sample Test

```js
describe('login', () => {
  it('logs in with valid credentials', () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type('alice@example.com');
    cy.get('[data-cy=password]').type('secret');
    cy.get('[data-cy=submit]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

## Best Practices

- Use data-cy attributes; never CSS classes in selectors
- Keep tests independent with cy.intercept stubs
- Run a smoke subset on PRs, full suite nightly
- Record to Cypress Cloud for flake analytics
- Parallelize across machines for large suites

## Capabilities

### cypress-runs
Open, run, and filter Cypress tests.

**Parameters:**
- `spec` (string): Test file or glob pattern
- `browser` (string): Browser: chrome, firefox, edge, electron

**Commands:**
- `npx cypress open`
- `npx cypress run`
- `npx cypress run --browser chrome`
- `npx cypress run --spec cypress/e2e/login.cy.js`
- `npx cypress run --headed`

**Examples:**
- npx cypress open
- npx cypress run --spec cypress/e2e/login.cy.js
- npx cypress run --browser edge

### parallel-and-record
Parallelize runs and record to Cypress Cloud.

**Parameters:**
- `recordKey` (string): Cypress Cloud record key
- `tag` (string): Run tag for filtering
- `group` (string): Group name for parallel runs

**Commands:**
- `npx cypress run --record --key $CYPRESS_RECORD_KEY`
- `npx cypress run --parallel --record`
- `npx cypress run --group chrome --browser chrome`
- `npx cypress run --tag smoke`

**Examples:**
- npx cypress run --record --key $CYPRESS_RECORD_KEY
- npx cypress run --parallel --record --group chrome
- npx cypress run --tag smoke

### component-and-debug
Component testing and debugging helpers.

**Parameters:**
- `env` (object): Environment variables for tests
- `config` (object): Runtime config overrides

**Commands:**
- `npx cypress run --component`
- `npx cypress run --env grep='login'`
- `npx cypress run --config video=false`
- `cypress verify`

**Examples:**
- npx cypress run --component
- npx cypress run --env grep='login'
- npx cypress run --config video=false

## References
- [Cypress Documentation](https://docs.cypress.io/)
- [Cypress CLI Reference](https://docs.cypress.io/app/references/command-line)
