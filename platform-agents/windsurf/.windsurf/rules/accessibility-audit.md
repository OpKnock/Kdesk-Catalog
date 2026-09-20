---
trigger: glob
description: "Run an accessibility scan of a single URL and capture violations in machine-readable format. Wire accessibility checks into CI pipelines with pa11y-ci and Lighthouse CI. producing WCAG 2.x violation reports and CI gates. Use when auditing a site or app against WCAG 2.x. Don't use for fixing individual accessibility defects or for manual keyboard-navigation testing."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.scala", "**/*.sh"]
---

Run an accessibility scan of a single URL and capture violations in machine-readable format. Wire accessibility checks into CI pipelines with pa11y-ci and Lighthouse CI. producing WCAG 2.x violation reports and CI gates. Use when auditing a site or app against WCAG 2.x. Don't use for fixing individual accessibility defects or for manual keyboard-navigation testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx pa11y http://localhost:8080 --reporter=json`, `npm install --save-dev pa11y-ci`
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

# Accessibility Audit

## What this skill does

Runs automated accessibility audits on web apps using pa11y, axe-core and Lighthouse. It produces WCAG conformance violation lists, severity counts, and Lighthouse accessibility scores that can be wired into CI so regressions fail the build.

## When to use

- Checking a page or site for WCAG 2.1/2.2 conformance
- Accessibility regressions keep appearing in a SPA (contrast, alt text, ARIA)
- Setting up automated accessibility gates in a CI pipeline

## Real commands

```bash
# Single-page audit with JSON output
npx pa11y https://example.com --reporter=json

# Lighthouse accessibility-only run
npx lighthouse https://example.com --only-categories=accessibility --output=json --output-path=./a11y.json

# Fail if more than 5 errors
pa11y --standard WCAG2AA --threshold 5 https://example.com/login

# axe-core with exit code 1 on violations
npx axe https://example.com --exit

# Audit every URL in a sitemap
npx pa11y-ci --sitemap https://example.com/sitemap.xml
```

## .pa11yci config

```json
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 30000,
    "chromeLaunchConfig": { "args": ["--no-sandbox"] }
  },
  "urls": {
    "https://example.com/": ["a11y/landmarks-one-main"]
  }
}
```

## Testing

- Run `npx pa11y-ci` locally first; exit code is non-zero when violations exceed threshold
- Archive `results.json` as a CI artifact

## Best practices

- Default to `WCAG2AA`, escalate to `WCAG2AAA` for public content
- Combine pa11y (DOM) with axe-core (in-page rules) for broader coverage
- Treat `threshold 0` as the long-term goal; escalate thresholds gradually
- Run headless Chrome in CI to keep the footprint small

## Capabilities

### audit-page
Run an accessibility scan of a single URL and capture violations in machine-readable format.

**Parameters:**
- `url` (string): Target page URL to audit
- `standard` (string): WCAG conformance level: WCAG2A, WCAG2AA, WCAG2AAA
- `threshold` (number): Maximum number of errors before the run fails

**Commands:**
- `npx pa11y http://localhost:8080 --reporter=json`
- `npx lighthouse http://localhost:8080 --output=json --output-path=./lighthouse-report.json`
- `npx axe http://localhost:8080 --exit`
- `pa11y --config .pa11yci http://localhost:8080`
- `npx pa11y-ci --sitemap http://localhost:8080/sitemap.xml`

**Examples:**
- npx pa11y --standard WCAG2AA --threshold 5 http://localhost:8080/login
- npx lighthouse http://localhost:8080 --only-categories=accessibility --output=html --output-path=report.html
- pa11y --include-notices http://localhost:8080

### ci-integration
Wire accessibility checks into CI pipelines with pa11y-ci and Lighthouse CI.

**Parameters:**
- `config` (string): Path to .pa11yci or lighthouserc config file
- `sitemap` (string): Sitemap URL to crawl for multi-page audits

**Commands:**
- `npm install --save-dev pa11y-ci`
- `npx pa11y-ci`
- `pa11y-ci --sitemap http://localhost:8080/sitemap.xml --json > results.json`
- `npx lhci autorun --config=./lighthouserc.json`

**Examples:**
- npx pa11y-ci --sitemap http://localhost:8080/sitemap.xml
- npx lhci healthcheck && npx lhci autorun
- npm install --save-dev @lhci/cli

## References
- [pa11y Documentation](https://pa11y.org/)
- [axe-core Docs](https://www.deque.com/axe/core-documentation/)
- [Lighthouse Accessibility Audits](https://developer.chrome.com/docs/lighthouse/accessibility/)
- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
