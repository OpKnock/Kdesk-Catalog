---
trigger: glob
description: "Lints CSS/SCSS and CSS-in-JS with Stylelint, enforcing order, naming, and browser-compatibility rules. Use when working with stylelint css, code quality or when the user mentions stylelint css, code quality."
globs: ["**/*.css", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Lints CSS/SCSS and CSS-in-JS with Stylelint, enforcing order, naming, and browser-compatibility rules.

## Agentic Workflow: Read -> Reason -> Act (stylelint)

You are **stylelint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `stylelint`
- Domain: Lints CSS/SCSS and CSS-in-JS with Stylelint, enforcing order, naming, and browser-compatibility rules.
- **stylelint-css**: Check and fix CSS/SCSS with Stylelint and its standard configs — `npx stylelint "src/**/*.css"`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `stylelint`
- For `stylelint-css`: Check and fix CSS/SCSS with Stylelint and its standard configs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `stylelint` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `stylelint:c254510b`

# Stylelint

Modern linter for CSS and CSS-like syntax (SCSS, Less, CSS-in-JS) with 200+ rules
covering formatting, patterns, and browser quirks.

## When to Use

- Enforcing consistent CSS/SCSS style across a project
- Catching invalid property values or unknown at-rules
- Ordering properties and declarations consistently

## Real Commands

```bash
# Install with standard config
npm install --save-dev stylelint stylelint-config-standard

# Check all CSS
npx stylelint "src/**/*.css"

# Auto-fix
npx stylelint --fix "src/**/*.{css,scss}"

# Custom config
npx stylelint --config .stylelintrc.json .

# Lint stdin (editor integration)
echo '.a { color: red }' | npx stylelint --stdin-filename app.css

# Custom formatter for CI
npx stylelint "src/**/*.css" --custom-formatter=node_modules/stylelint-json-formatter
```

## Config (.stylelintrc.json)

```json
{
  "extends": "stylelint-config-standard",
  "customSyntax": "postcss-scss",
  "rules": {
    "color-hex-length": "long",
    "max-nesting-depth": 3
  }
}
```

## CI

```yaml
- name: Stylelint
  run: npx stylelint "src/**/*.css"
```

## Best Practices

- Extend `stylelint-config-standard` and only override what you disagree with
- Use `postcss-scss` customSyntax for SCSS files
- Enable the property-order config for team consistency
- Run `--fix` locally, plain check in CI

## Example Response

Reports violations as `file:line:col severity message rule-name`, then applies
--fix and confirms the remaining list.

## Capabilities

### stylelint-css
Check and fix CSS/SCSS with Stylelint and its standard configs

**Parameters:**
- `fix` (boolean): Auto-fix fixable violations
- `config` (string): Path to the stylelint config file
- `stdin-filename` (string): Filename to associate with piped stdin content

**Commands:**
- `npx stylelint "src/**/*.css"`
- `npx stylelint --fix "src/**/*.{css,scss}"`
- `npx stylelint --config .stylelintrc.json .`
- `npx stylelint --custom-formatter=node_modules/stylelint-json-formatter .`
- `npx stylelint "src/**/*.css" --stdin-filename app.css --stdin`

**Examples:**
- npx stylelint --ignore-path .gitignore "**/*.css"
- npx stylelint --fix src/styles/
- echo '.a {color:red}' | npx stylelint --stdin-filename app.css

## References
- [Stylelint docs](https://stylelint.io/)
- [Stylelint rules](https://stylelint.io/user-guide/rules/)
