---
applyTo: "**/*.json **/*.r **/*.sh **/*.{ts,tsx}"
---

Builds synthetic monitoring with Checkly: multi-step browser checks, API checks as code, and deployment to Checkly's global runners from a Node project.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx create-checkly-project my-checks --template api-check`, `npm install @playwright/test`
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

# API Monitor v3 - Synthetic Checks

Synthetic monitoring with Checkly.

## What This Skill Does
- Defines API and browser checks as TypeScript code
- Runs checks locally and on global runners
- Alerts on failures via email, Slack, or PagerDuty

## When to Use
- Monitoring user-critical flows the backend cannot measure
- Pre-deploy canary checks
- Third-party dependency monitoring

## Real Commands

```bash
npx create-checkly-project my-checks --template api-check
npx checkly test
npx checkly deploy
```

## API Check Example

```ts
import { ApiCheck, AssertionBuilder } from 'checkly/constructs';
new ApiCheck('api-health', {
  request: { method: 'GET', url: 'https://api.example.com/health' },
  assertions: [
    AssertionBuilder.statusCode().equals(200),
    AssertionBuilder.jsonBody('status').equals('ok')
  ]
});
```

## Testing
- Run npx checkly test before merging changes
- Use browser checks for multi-step journeys (login -> search)
- Schedule groups with frequency and regions

## Best Practices
- Store check code in the API repository
- Use environments for stage-specific URLs
- Keep assertions tight; alert on user impact only

## Capabilities

### checkly-cli
Author and deploy API/browser checks as code

**Parameters:**
- `check-name` (string): Identifier of the check to run
- `template` (string): Scaffold template: api-check, browser-check, group
- `env` (string): Environment variable file for check secrets

**Commands:**
- `npx create-checkly-project my-checks --template api-check`
- `npx checkly test`
- `npx checkly deploy`
- `npx checkly run-check api-health`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:8080/health`

**Examples:**
- npx checkly test runs checks locally with live results
- npx checkly deploy publishes checks to global runners
- npx checkly run-check api-health triggers a single check on demand

### synthetic-flows
Script multi-step user journeys as Playwright browser checks

**Commands:**
- `npm install @playwright/test`
- `npx playwright test --project=chromium`
- `npx checkly test --browser`
- `npx checkly login`

**Examples:**
- -cli --help
- -api --help

## References
- [Checkly CLI Docs](https://www.checklyhq.com/docs/cli/)
- [Checkly API Checks](https://www.checklyhq.com/docs/api-checks/)
