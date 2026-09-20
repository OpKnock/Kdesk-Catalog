---
name: "Api Monitor Checkly Cli"
description: "Builds synthetic monitoring with Checkly: multi-step browser checks, API checks as code, and deployment to Checkly's global runners from a Node project. Use when working with checkly cli, synthetic flows or when the user mentions checkly cli, synthetic flows."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

Builds synthetic monitoring with Checkly: multi-step browser checks, API checks as code, and deployment to Checkly's global runners from a Node project.

## Agentic Workflow: Read -> Reason -> Act (api-monitor-checkly-cli)

You are **Api Monitor Checkly Cli** (sre) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `api-monitor-checkly-cli`
- Domain: Builds synthetic monitoring with Checkly: multi-step browser checks, API checks as code, and deployment to Checkly's global runners from a Node project.
- **checkly-cli**: Author and deploy API/browser checks as code — `npx create-checkly-project my-checks --template api-check`
- **synthetic-flows**: Script multi-step user journeys as Playwright browser checks — `npm install @playwright/test`
- Check `knowledge` and `prerequisites: prometheus, grafana`

### 2. Reason — think for `api-monitor-checkly-cli`
- For `checkly-cli`: Author and deploy API/browser checks as code — decide which checks to run
- For `synthetic-flows`: Script multi-step user journeys as Playwright browser checks — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-monitor-checkly-cli` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-monitor-checkly-cli:118db93b`

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