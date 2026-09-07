---
type: agent_requested
description: "Lints CSS/SCSS and CSS-in-JS with Stylelint, enforcing order, naming, and browser-compatibility rules. Use when working with stylelint css, code quality or when the user mentions stylelint css, code quality."
---

Lints CSS/SCSS and CSS-in-JS with Stylelint, enforcing order, naming, and browser-compatibility rules.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx stylelint "src/**/*.css"`
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