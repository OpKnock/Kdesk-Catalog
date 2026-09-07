---
applyTo: "**/*.css **/*.html **/*.json **/*.r **/*.sh"
---

Processes, lints, and optimizes CSS with PostCSS, Stylelint, Sass, Lightning CSS, and PurgeCSS pipelines.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx stylelint 'src/**/*.css'`, `npx postcss src/styles.css -o dist/styles.css --use autopref`
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
