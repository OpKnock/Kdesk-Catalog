---
name: "Synthetic Monitoring"
description: "Build always-on synthetic checks that catch outages before users do. Records browser journeys with Playwright, runs lightweight uptime probes with k6 and curl, and verifies status codes, timing, and page content from multiple regions. Use when working with synthetic checks, api or when the user mentions synthetic checks, api."
globs: ["**/*.go", "**/*.java", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
alwaysApply: false
---

Build always-on synthetic checks that catch outages before users do. Records browser journeys with Playwright, runs lightweight uptime probes with k6 and curl, and verifies status codes, timing, and page content from multiple regions.

## Agentic Workflow: Read -> Reason -> Act (synthetic-monitoring)

You are **Synthetic Monitoring** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `synthetic-monitoring`
- Domain: Build always-on synthetic checks that catch outages before users do. Records browser journeys with Playwright, runs lightweight uptime probes with k6 and curl, and verifies status codes, timing, and p
- **synthetic-checks**: Build browser and uptime checks that run on a schedule — `npx playwright test`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `synthetic-monitoring`
- For `synthetic-checks`: Build browser and uptime checks that run on a schedule — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `synthetic-monitoring` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `K6` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `synthetic-monitoring:dc888f31`

# Synthetic Monitoring

Hand-crafted skill for always-on checks that catch outages before users do.

## What this skill does

- Records browser journeys with Playwright codegen and replays them
- Runs lightweight uptime probes with k6 and curl
- Verifies status codes, timing, and page content

## When to use

- Critical journeys: login, checkout, search
- Verifying deployments from outside the network
- Catching slow-but-not-down degradations

## Real commands

```bash
# Record a journey
npx playwright codegen https://staging.your-app.test/login

# Run the recorded checks
npx playwright test
npx playwright test --headed

# k6 uptime probe
k6 run --vus 1 --iterations 1 uptime.js

# Instant probe
curl -s -o /dev/null -w '%{http_code} %{time_total}\n' https://api.your-app.test/health
```

## Playwright check

```js
import { test, expect } from "@playwright/test";

test("login works", async ({ page }) => {
  await page.goto("https://staging.your-app.test/login");
  await page.fill("#email", "ada@example.com");
  await page.fill("#password", "secret");
  await page.click("button[type=submit]");
  await expect(page.locator(".welcome")).toContainText("Ada");
});
```

## k6 uptime probe

```javascript
import http from "k6/http";
import { check } from "k6";

export const options = { vus: 1, iterations: 1 };

export default function () {
  const res = http.get("https://api.your-app.test/health");
  check(res, {
    "status is 200": (r) => r.status === 200,
    "responds fast": (r) => r.timings.duration < 1000,
  });
}
```

## Best practices

- Run synthetic checks from multiple regions
- Alert on 2 consecutive failures to avoid flapping
- Keep journeys short: a check that times out helps nobody

## Capabilities

### synthetic-checks
Build browser and uptime checks that run on a schedule

**Parameters:**
- `url` (string): URL under check
- `browser` (string): chromium, firefox, or webkit for Playwright
- `schedule` (string): Run cadence, e.g. every 5m

**Commands:**
- `npx playwright test`
- `npx playwright test --headed`
- `npx playwright codegen https://staging.your-app.test/login`
- `k6 run --vus 1 --iterations 1 uptime.js`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}\n' https://api.your-app.test/health`

**Examples:**
- npx playwright test --headed
- npx playwright codegen https://staging.your-app.test/login
- k6 run --vus 1 --iterations 1 uptime.js

## References
- [Playwright test docs](https://playwright.dev/docs/test-intro)
- [k6 docs](https://grafana.com/docs/k6/latest/)