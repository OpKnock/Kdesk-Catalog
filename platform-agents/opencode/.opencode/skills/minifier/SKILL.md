---
name: "minifier"
description: "Minify and mangle JS bundles with terser and esbuild. Minify CSS/HTML and apply gzip/brotli handling transfer size. and gzip/brotli compression.'. Use when working with javascript minification, css html and compression, devtools or when the user mentions javascript minification, css html and compression, devtools."
---

Minify and mangle JS bundles with terser and esbuild. Minify CSS/HTML and apply gzip/brotli handling transfer size. and gzip/brotli compression.'

## Agentic Workflow: Read -> Reason -> Act (minifier)

You are **minifier** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `minifier`
- Domain: Minify and mangle JS bundles with terser and esbuild. Minify CSS/HTML and apply gzip/brotli handling transfer size. and gzip/brotli compression.'
- **javascript-minification**: Minify and mangle JS bundles with terser and esbuild. — `terser input.js -o output.min.js`
- **css-html-and-compression**: Minify CSS/HTML and apply gzip/brotli for transfer size. — `npx cssnano styles.css styles.min.css`
- Check `knowledge` and `prerequisites: brotli, esbuild, gzip, npx`

### 2. Reason — think for `minifier`
- For `javascript-minification`: Minify and mangle JS bundles with terser and esbuild. — decide which checks to run
- For `css-html-and-compression`: Minify CSS/HTML and apply gzip/brotli for transfer size. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `minifier` tools
- Tools: `Glob`, `Grep`, `Read`, `Terser`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `minifier:9819aadc`

# Asset Minification

Shrink JavaScript, CSS, HTML, and images for production delivery.

## What This Skill Does

- Minifies and mangles JS (terser/esbuild/uglify)
- Compresses CSS (cssnano) and HTML
- Optimizes SVG (svgo)
- Applies gzip/brotli transfer encodings
- Measures before/after sizes

## When to Use

- Build pipeline release steps
- Reducing bundle size for page speed budgets
- Preparing static assets for CDN upload

## Real Commands

```bash
# JavaScript
terser input.js -o output.min.js
npx terser input.js --compress --mangle --source-map
esbuild app.js --minify --bundle --outfile=app.min.js
esbuild --minify --target=es2020 app.js -o app.min.js
npx uglifyjs input.js -c -m -o output.min.js

# CSS / HTML / SVG
npx cssnano styles.css styles.min.css
npx html-minifier-terser --collapse-whitespace --remove-comments index.html -o index.min.html
npx svgo -f assets/icons -o assets/icons-min

# Transfer compression
gzip -9 -k -c bundle.js > bundle.js.gz
brotli -q 11 -o bundle.js.br bundle.js

# Verify
ls -lh input.js output.min.js output.min.js.gz
```

## Best Practices

- Generate source maps in staging builds for debugging
- Minify at build time, not runtime
- Precompress with brotli for HTTP servers that support it
- Check bundle budgets in CI after minification
- Verify no behavior change: diff runtime tests before/after

## Capabilities

### javascript-minification
Minify and mangle JS bundles with terser and esbuild.

**Parameters:**
- `input` (string): Input file
- `output` (string): Output file
- `mangle` (boolean): Rename variables to short names

**Commands:**
- `terser input.js -o output.min.js`
- `npx terser input.js --compress --mangle --source-map`
- `esbuild app.js --minify --bundle --outfile=app.min.js`
- `esbuild --minify --target=es2020 app.js -o app.min.js`
- `npx uglifyjs input.js -c -m -o output.min.js`

**Examples:**
- terser input.js -o output.min.js
- esbuild app.js --minify --bundle --outfile=app.min.js
- npx uglifyjs input.js -c -m -o output.min.js

### css-html-and-compression
Minify CSS/HTML and apply gzip/brotli for transfer size.

**Parameters:**
- `level` (integer): Compression level (gzip 1-9, brotli 0-11)
- `quality` (integer): SVG/asset quality

**Commands:**
- `npx cssnano styles.css styles.min.css`
- `npx html-minifier-terser --collapse-whitespace --remove-comments index.html -o index.min.html`
- `gzip -9 -k -c bundle.js > bundle.js.gz`
- `brotli -q 11 -o bundle.js.br bundle.js`
- `npx svgo -f assets/icons -o assets/icons-min`

**Examples:**
- npx cssnano styles.css styles.min.css
- npx html-minifier-terser --collapse-whitespace index.html -o index.min.html
- brotli -q 11 -o bundle.js.br bundle.js

## References
- [Terser](https://terser.org/)
- [esbuild Minify](https://esbuild.github.io/api/#minify)
- [cssnano](https://cssnano.co/)
- [html-minifier-terser](https://github.com/terser/html-minifier-terser)
