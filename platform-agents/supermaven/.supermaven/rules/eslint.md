# eslint

Lints JavaScript and TypeScript with ESLint: full lint runs, autofix, custom rulesets, and CI integration.

## Instructions

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

**Commands:**
- `npx eslint --rule "no-console: error" src/`
- `eslint --rulesdir ./rules src/`
- `eslint --plugin react --rule "react/jsx-uses-react: error" src/`
- `eslint --print-config src/main.js`

**Examples:**
- npx eslint --fix --ext .jsx,.tsx src/components/
- eslint --no-eslintrc --parser-options "ecmaVersion: latest" src/