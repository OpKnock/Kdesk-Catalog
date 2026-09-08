---
name: "static-site-optimizer"
description: "Optimizes static sites for Core Web Vitals with Lighthouse CI, image compression, CSS purging, and asset minification. Use when working with performance audit, asset optimization, delivery optimization or when the user mentions performance audit, asset optimization, delivery optimization."
globs: ["**/*.css", "**/*.go", "**/*.html", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Optimizes static sites for Core Web Vitals with Lighthouse CI, image compression, CSS purging, and asset minification.

## Agentic Workflow: Read -> Reason -> Act (static-site-optimizer)

You are **static-site-optimizer** (frontend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `static-site-optimizer`
- Domain: Optimizes static sites for Core Web Vitals with Lighthouse CI, image compression, CSS purging, and asset minification.
- **performance-audit**: Measure and gate performance with Lighthouse. — `npx lhci autorun`
- **asset-optimization**: Compress images, purge CSS, and minify bundles. — `npx imagemin images/**/*.png --out-dir=optimized`
- **delivery-optimization**: Compress responses and inspect headers. — `gzip -9 -k dist/index.html`
- Check `knowledge` and `prerequisites: next.js, astro, node.js, sharp`

### 2. Reason — think for `static-site-optimizer`
- For `performance-audit`: Measure and gate performance with Lighthouse. — decide which checks to run
- For `asset-optimization`: Compress images, purge CSS, and minify bundles. — decide which checks to run
- For `delivery-optimization`: Compress responses and inspect headers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `static-site-optimizer` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Gzip` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `static-site-optimizer:8ccfe750`

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