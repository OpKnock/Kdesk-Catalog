# Api Monitor Checkly Cli

Builds synthetic monitoring with Checkly: multi-step browser checks, API checks as code, and deployment to Checkly's global runners from a Node project.

## Instructions

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
