---
type: agent_requested
description: "Lints JavaScript and TypeScript with ESLint: full lint runs, autofix, custom rulesets, and CI integration. Use when working with eslint lint, eslint rules, code quality or when the user mentions eslint lint, eslint rules, code quality."
---

Lints JavaScript and TypeScript with ESLint: full lint runs, autofix, custom rulesets, and CI integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `eslint src/ --ext .js,.mjs`, `npx eslint --rule "no-console: error" src/`
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