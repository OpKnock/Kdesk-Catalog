---
name: "static-site-optimizer"
description: "Optimizes static sites for Core Web Vitals with Lighthouse CI, image compression, CSS purging, and asset minification. Use when working with performance audit, asset optimization, delivery optimization or when the user mentions performance audit, asset optimization, delivery optimization."
---

Optimizes static sites for Core Web Vitals with Lighthouse CI, image compression, CSS purging, and asset minification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx lhci autorun`, `npx imagemin images/**/*.png --out-dir=optimized`
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

# Static Site Optimization

Make static sites fast: measure, optimize, and enforce budgets.

## What This Skill Does

- Audits Core Web Vitals with Lighthouse in CI
- Compresses images and minifies JS/CSS
- Purges unused CSS and inlines critical CSS
- Sets compression and caching headers

## When to Use

- Lighthouse scores regress and need diagnosis
- Setting performance budgets for a redesign
- Reducing first-load bytes of a marketing site

## Real Commands

```bash
# Measure
npx lhci autorun
npx lighthouse https://example.com --only-categories=performance --output=json --output-path=lh.json

# Optimize assets
npx imagemin images/**/*.png --out-dir=optimized
npx purgecss --css dist/styles.css --content dist/**/*.html --output dist/
npx terser src/app.js -c -m -o dist/app.min.js

# Delivery
brotli -9 -k dist/index.html
gzip -9 -k dist/app.js
curl -sI -H 'Accept-Encoding: br' https://example.com | grep -i content-encoding
```

## Budgets (lighthouserc.json)

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }]
      }
    }
  }
}
```

## Best Practices

- Audit on a warmed cache and a cold cache
- Serve AVIF/WebP with responsive sizes
- Preload fonts and critical images; lazy-load below the fold
- Enable brotli at the CDN; set long cache headers on hashed assets
- Fail CI on LCP > 2.5s to prevent regressions

## Capabilities

### performance-audit
Measure and gate performance with Lighthouse.

**Parameters:**
- `url` (string): Page URL to audit
- `numberOfRuns` (number): Runs per URL for median scoring

**Commands:**
- `npx lhci autorun`
- `npx lighthouse http://localhost:8080 --only-categories=performance --output=json --output-path=lh.json`
- `npx lhci collect --url=http://localhost:8080 --numberOfRuns=3`
- `npx lhci assert --preset=lighthouse:recommended`

**Examples:**
- npx lhci autorun
- npx lighthouse http://localhost:8080 --only-categories=performance --output=json --output-path=lh.json
- npx lhci collect --url=http://localhost:8080 --numberOfRuns=3

### asset-optimization
Compress images, purge CSS, and minify bundles.

**Parameters:**
- `source` (string): Source files to optimize
- `output` (string): Output directory

**Commands:**
- `npx imagemin images/**/*.png --out-dir=optimized`
- `npx purgecss --css dist/styles.css --content dist/**/*.html --output dist/`
- `npx terser src/app.js -c -m -o dist/app.min.js`
- `npx critters dist/index.html -o dist/index.html`
- `npx webpack-bundle-analyzer dist/stats.json`

**Examples:**
- npx imagemin images/hero.png --out-dir=optimized
- npx purgecss --css dist/styles.css --content dist/**/*.html --output dist/
- npx terser src/app.js -c -m -o dist/app.min.js

### delivery-optimization
Compress responses and inspect headers.

**Parameters:**
- `file` (string): File to compress
- `quality` (number): Compression level 1-9

**Commands:**
- `gzip -9 -k dist/index.html`
- `brotli -9 -k dist/index.html`
- `curl -sI -H 'Accept-Encoding: br' http://localhost:8080 | grep -i 'content-encoding\|cache-control'`
- `npx http-server -c-1 dist`

**Examples:**
- brotli -9 -k dist/index.html
- curl -sI -H 'Accept-Encoding: br' http://localhost:8080 | grep -i content-encoding
- gzip -9 -k dist/app.js

## References
- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/overview)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [web.dev Performance](https://web.dev/explore/learn-core-web-vitals)
