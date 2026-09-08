Audits and improves site SEO with Lighthouse CI, crawler checks, sitemap generation, and Core Web Vitals measurement from the CLI.

## Agentic Workflow: Read -> Reason -> Act (search-engine-optimization)

You are **search-engine-optimization** (frontend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `search-engine-optimization`
- Domain: Audits and improves site SEO with Lighthouse CI, crawler checks, sitemap generation, and Core Web Vitals measurement from the CLI.
- **lighthouse-audit**: Run Lighthouse audits for SEO, performance, and accessibility scores. — `npx lighthouse http://localhost:8080 --only-categories=seo,performance --output=`
- **crawling-and-content**: Validate meta tags, robots.txt, sitemaps, and HTTP headers with curl and htmlhint. — `curl -s http://localhost:8080/robots.txt`
- Check `knowledge` and `prerequisites: elasticsearch, meilisearch, typesense, node.js`

### 2. Reason — think for `search-engine-optimization`
- For `lighthouse-audit`: Run Lighthouse audits for SEO, performance, and accessibility scores. — decide which checks to run
- For `crawling-and-content`: Validate meta tags, robots.txt, sitemaps, and HTTP headers with curl and htmlhint. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `search-engine-optimization` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `search-engine-optimization:29643121`

# Search Engine Optimization

Audit and improve on-page SEO, crawlability, and performance signals from the terminal.

## What This Skill Does

- Runs Lighthouse SEO/performance audits and extracts scored JSON
- Validates robots.txt, sitemaps, and critical HTTP headers
- Lints HTML for missing titles, meta descriptions, and heading structure
- Measures Core Web Vitals (LCP, CLS, INP) across runs
- Enforces performance budgets in CI with Lighthouse CI

## When to Use

- A page loses rankings and needs an SEO audit
- Site migration or launch needs crawlability checks
- CI should block PRs that regress Lighthouse scores

## Real Commands

```bash
# Full audit with machine-readable output
npx lighthouse https://example.com --only-categories=seo,performance --output=json --output-path=lh.json

# CI gate with budgets and assertions
npx lhci collect --url=https://example.com --numberOfRuns=3
npx lhci assert --preset=lighthouse:recommended
npx lhci upload --target=temporary-public-storage

# Crawlability and headers
curl -s https://example.com/robots.txt
curl -s https://example.com/sitemap.xml | grep -c '<url>'
curl -sI https://example.com | grep -i 'cache-control'

# On-page linting
npx htmlhint public/index.html
curl -s https://example.com | grep -o '<title>[^<]*</title>'
```

## Sample lighthouserc

```json
{
  "ci": {
    "collect": { "url": ["https://example.com"], "numberOfRuns": 3 },
    "assert": {
      "assertions": {
        "categories:seo": ["error", { "minScore": 0.9 }],
        "categories:performance": ["warn", { "minScore": 0.8 }]
      }
    }
  }
}
```

## Best Practices

- Audit the top-traffic and money pages, not just the homepage
- Verify sitemap URLs return 200 and match canonical URLs
- Keep LCP under 2.5s: compress images, preload critical assets
- Set cache-control on static assets and avoid redirect chains
- Wire lhci into CI so SEO regressions fail the build

## Capabilities

### lighthouse-audit
Run Lighthouse audits for SEO, performance, and accessibility scores.

**Parameters:**
- `url` (string): Page URL to audit
- `categories` (array): Lighthouse categories to include, e.g. seo, performance, accessibility
- `output-path` (string): Where to write the JSON report

**Commands:**
- `npx lighthouse http://localhost:8080 --only-categories=seo,performance --output=json --output-path=lh.json`
- `npx lhci autorun`
- `npx lighthouse http://localhost:8080 --chrome-flags="--headless"`
- `npx lhci collect --url=http://localhost:8080 --numberOfRuns=3`

**Examples:**
- npx lighthouse http://localhost:8080 --only-categories=seo --output=json --output-path=seo.json
- npx lhci autorun
- npx lighthouse http://localhost:8080/checkout --budget-path=budget.json

### crawling-and-content
Validate meta tags, robots.txt, sitemaps, and HTTP headers with curl and htmlhint.

**Parameters:**
- `path` (string): URL path or local file to inspect
- `header` (string): HTTP header to filter, e.g. cache-control

**Commands:**
- `curl -s http://localhost:8080/robots.txt`
- `curl -s http://localhost:8080/sitemap.xml | head -20`
- `curl -sI http://localhost:8080 | grep -i '^HTTP\|^content-type\|^cache-control'`
- `npx htmlhint index.html`
- `curl -s http://localhost:8080 | grep -o 'demo-title[^<]*demo-title'`

**Examples:**
- curl -sI http://localhost:8080 | grep -i '^content-encoding'
- curl -s http://localhost:8080/sitemap.xml | grep -c 'http://localhost:8080'
- npx htmlhint public/index.html

## References
- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/overview)
- [Google Search Central](https://developers.google.com/search/docs)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
