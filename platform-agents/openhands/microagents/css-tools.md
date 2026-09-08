---
name: "css-tools"
description: "Processes, lints, and optimizes CSS with PostCSS, Stylelint, Sass, Lightning CSS, and PurgeCSS pipelines. Use when working with lint, process, frontend or when the user mentions lint, process, frontend."
type: knowledge
triggers: ["css-tools", "lint", "process"]
---

Processes, lints, and optimizes CSS with PostCSS, Stylelint, Sass, Lightning CSS, and PurgeCSS pipelines.

## Agentic Workflow: Read -> Reason -> Act (css-tools)

You are **css-tools** (frontend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `css-tools`
- Domain: Processes, lints, and optimizes CSS with PostCSS, Stylelint, Sass, Lightning CSS, and PurgeCSS pipelines.
- **lint**: Lint and auto-fix CSS and SCSS with Stylelint. — `npx stylelint 'src/**/*.css'`
- **process**: Compile and optimize CSS with PostCSS, Sass, and Lightning CSS. — `npx postcss src/styles.css -o dist/styles.css --use autoprefixer`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `css-tools`
- For `lint`: Lint and auto-fix CSS and SCSS with Stylelint. — decide which checks to run
- For `process`: Compile and optimize CSS with PostCSS, Sass, and Lightning CSS. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `css-tools` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `css-tools:08a60161`

# CSS Tooling

Compile, lint, and minify CSS with a production-grade toolchain.

## When to Use

- Enforcing consistent CSS quality across a codebase
- Building Sass/PostCSS pipelines with vendor prefixing
- Shrinking shipped CSS by purging unused rules

## Stylelint

```css
/* .stylelintrc.json */
{
  "extends": "stylelint-config-standard",
  "rules": { "declaration-block-no-duplicate-properties": true }
}
```

```bash
npx stylelint 'src/**/*.css' --max-warnings 0
npx stylelint --fix 'src/**/*.css'
```

## Sass pipeline

```bash
npx sass src/scss/main.scss dist/main.css --style compressed --watch
```

## PostCSS + autoprefixer

```bash
npx postcss src/styles.css -o dist/styles.css --use autoprefixer
```

## PurgeCSS for shipped CSS

```bash
npx purgecss --css dist/main.css --content 'dist/**/*.{html,js}' --output dist/
```

Only purge on final production builds, never in dev.

## Lightning CSS (alternative bundler-level pipeline)

```bash
npx lightningcss --minify --targets '>= 0.5%' src/styles.css -o dist/styles.css
```

## Best practices

- Run Stylelint in CI with `--max-warnings 0`.
- Keep nesting depth under 3 levels.
- Prefer CSS custom properties over Sass variables for runtime theming.
- Measure CSS bytes with a size budget per route.

## Capabilities

### lint
Lint and auto-fix CSS and SCSS with Stylelint.

**Parameters:**
- `config` (string): Path to Stylelint config
- `max-warnings` (number): Exit non-zero beyond this many warnings
- `formatter` (string): stylish, json, compact output

**Commands:**
- `npx stylelint 'src/**/*.css'`
- `npx stylelint 'src/**/*.scss' --config .stylelintrc.json`
- `npx stylelint --fix 'src/**/*.css'`
- `npx stylelint --formatter json 'src/**/*.css'`
- `npx stylelint --max-warnings 0 'src/**/*.css'`

**Examples:**
- npx stylelint 'src/**/*.css' --max-warnings 0
- npx stylelint --fix 'src/**/*.scss'
- npx stylelint 'src/**/*.css' --formatter=json > stylelint-report.json

### process
Compile and optimize CSS with PostCSS, Sass, and Lightning CSS.

**Parameters:**
- `output` (string): Output CSS path or directory
- `watch` (string): Rebuild on file changes
- `style` (string): expanded or compressed output style

**Commands:**
- `npx postcss src/styles.css -o dist/styles.css --use autoprefixer`
- `npx sass src/scss/main.scss dist/main.css --style compressed`
- `npx lightningcss --minify --browserslist '>= 0.5%' src/styles.css -o dist/styles.css`
- `npx purgecss --css dist/styles.css --content 'dist/**/*.html' --output dist/`
- `npx postcss --watch src/styles.css -o dist/styles.css`

**Examples:**
- npx sass src/scss/main.scss dist/main.css --watch --style compressed
- npx purgecss --css build/*.css --content 'build/**/*.{html,js}' --output build/
- npx lightningcss --minify --targets '>= 0.5%' src/a.css src/b.css -o dist/out.css

## References
- [Stylelint](https://stylelint.io/)
- [PostCSS](https://postcss.org/)
- [Sass Docs](https://sass-lang.com/documentation/cli/dart-sass)
