---
name: "eslint"
description: "Lints JavaScript and TypeScript with ESLint: full lint runs, autofix, custom rulesets, and CI integration. Use when working with eslint lint, eslint rules, code quality or when the user mentions eslint lint, eslint rules, code quality."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}", "**/*.{ts,tsx}"]
alwaysApply: false
---

Lints JavaScript and TypeScript with ESLint: full lint runs, autofix, custom rulesets, and CI integration.

## Agentic Workflow: Read -> Reason -> Act (eslint)

You are **eslint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `eslint`
- Domain: Lints JavaScript and TypeScript with ESLint: full lint runs, autofix, custom rulesets, and CI integration.
- **eslint-lint**: Lint and fix code with real CLI flags. — `eslint src/ --ext .js,.mjs`
- **eslint-rules**: Inspect and apply specific rules. — `npx eslint --rule "no-console: error" src/`
- Check `knowledge` and `prerequisites: eslint, npx`

### 2. Reason — think for `eslint`
- For `eslint-lint`: Lint and fix code with real CLI flags. — decide which checks to run
- For `eslint-rules`: Inspect and apply specific rules. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `eslint` tools
- Tools: `Glob`, `Grep`, `Read`, `Eslint`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `eslint:32c93066`

# ESLint

JavaScript and TypeScript linting.

## When to Use

- Enforcing code style and catching bugs early
- Autofixing safe issues in CI or pre-commit
- TS projects with typescript-eslint
- Framework code with React/Vue plugins

## Commands

```bash
# Basic lint
eslint src/

# Autofix
eslint src/ --fix
eslint --fix-dry-run src/  # preview

# Scope and extensions
eslint . --ext .js,.ts
eslint src/components/ --ext .jsx,.tsx

# Warnings budget
eslint --max-warnings 10 src/

# Reports
eslint --format json src/ -o eslint-report.json
eslint --format sarif src/ -o eslint-report.sarif

# Caching
eslint --cache src/
```

## Common Rules

```javascript
rules: {
  "semi": ["error", "always"],
  "no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
  "@typescript-eslint/no-explicit-any": "warn",
}
```

## Best Practices

- Use --fix in pre-commit, verify-only in CI
- Set --max-warnings 0 to block warning creep
- Cache runs locally; disable cache in CI
- Emit JSON/SARIF reports in CI for dashboards
- Pin ESLint and plugin versions together
- Use --fix-dry-run to review autofixes before applying

## Capabilities

### eslint-lint
Lint and fix code with real CLI flags.

**Parameters:**
- `paths` (string): Files or directories
- `fix` (boolean): Autofix problems
- `max-warnings` (integer): Warnings allowed before error

**Commands:**
- `eslint src/ --ext .js,.mjs`
- `eslint src/main.js --fix`
- `eslint . --ext .js,.ts`
- `eslint --max-warnings 10 src/`
- `eslint --format json src/ -o eslint-report.json`

**Examples:**
- eslint src/ --fix-dry-run
- eslint --no-error-on-unmatched-pattern "src/**/*.ts"
- eslint --cache src/

### eslint-rules
Inspect and apply specific rules.

**Parameters:**
- `rule` (string): Inline rule override
- `plugin` (string): Plugin namespace to enable, e.g. react

**Commands:**
- `npx eslint --rule "no-console: error" src/`
- `eslint --rulesdir ./rules src/`
- `eslint --plugin react --rule "react/jsx-uses-react: error" src/`
- `eslint --print-config src/main.js`

**Examples:**
- npx eslint --fix --ext .jsx,.tsx src/components/
- eslint --no-eslintrc --parser-options "ecmaVersion: latest" src/

## References
- [ESLint Docs](https://eslint.org/docs/latest/)
- [ESLint Rules](https://eslint.org/docs/latest/rules/)