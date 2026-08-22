# playwright-config

Configures Playwright test projects: browsers, webServer, baseURL, devices, and CI settings.

## Instructions

# Playwright Configuration

Tune Playwright Test for your projects and CI.

## What This Skill Does

- Initializes Playwright and installs browsers
- Defines projects for desktop/mobile devices
- Manages webServer startup and baseURL
- Configures parallelism, retries, and reporters

## When to Use

- Setting up Playwright for a new repo
- Adjusting browser matrix and sharding
- Debugging CI flakiness via config

## Real Commands

```bash
# Init
npm init playwright@latest
npx playwright install --with-deps
npx playwright test --list

# Projects
npx playwright test --project=desktop
npx playwright test --project=mobile --grep @smoke

# CI overrides
npx playwright test --workers=2 --retries=3 --reporter=html
npx playwright test --config=playwright.config.ts --baseURL=https://staging.example.com
```

## Sample Config

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry'
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } }
  ]
});
```

## Best Practices

- Enable trace on-first-retry for flake debugging
- Use reuseExistingServer locally for fast loops
- Set retries higher in CI than locally
- Pin devices from the devices module; avoid hardcoded viewports
- Keep webServer commands environment-agnostic

## Capabilities

### playwright-init
Initialize and validate Playwright configuration.

**Commands:**
- `npm init playwright@latest`
- `npx playwright install chromium`
- `npx playwright install --with-deps`
- `npx playwright test --list`
- `npx playwright test --config=playwright.config.ts`

**Examples:**
- npm init playwright@latest
- npx playwright install --with-deps
- npx playwright test --list

### config-projects
Configure projects, devices, and baseURL.

**Commands:**
- `npx playwright test --project=desktop`
- `npx playwright test --project=mobile --grep @smoke`
- `npx playwright test --config=playwright.config.ts --baseURL=http://localhost:8080`
- `npx playwright test --project=webkit`

**Examples:**
- npx playwright test --project=desktop
- npx playwright test --config=playwright.config.ts --baseURL=http://localhost:8080
- npx playwright test --project=mobile

### ci-and-webserver
Web server and CI worker configuration.

**Commands:**
- `npx playwright test --workers=2`
- `npx playwright test --reporter=html`
- `npx playwright test --retries=3`
- `npx playwright test --global-timeout=1800000`
- `npx playwright test --timeout=30000`

**Examples:**
- npx playwright test --workers=2 --retries=3
- npx playwright test --reporter=html
- npx playwright test --timeout=30000
