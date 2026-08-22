# static-site-optimizer

Optimizes static sites for Core Web Vitals with Lighthouse CI, image compression, CSS purging, and asset minification.

## Instructions

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

**Commands:**
- `gzip -9 -k dist/index.html`
- `brotli -9 -k dist/index.html`
- `curl -sI -H 'Accept-Encoding: br' http://localhost:8080 | grep -i 'content-encoding\|cache-control'`
- `npx http-server -c-1 dist`

**Examples:**
- brotli -9 -k dist/index.html
- curl -sI -H 'Accept-Encoding: br' http://localhost:8080 | grep -i content-encoding
- gzip -9 -k dist/app.js