---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.{js,ts,jsx,tsx} **/*.{ts,tsx} **/*.{yaml,yml}"
---

Generic linting skill that sets up and runs ESLint across JS/TS projects, fixing problems and wiring checks into CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx eslint src/`
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

# Linting

General-purpose linting skill centered on ESLint for JavaScript/TypeScript projects,
covering setup, auto-fix, rulesets, and CI wiring.

## When to Use

- Setting up linting from scratch in a JS/TS project
- Applying auto-fixes to a codebase with thousands of violations
- Adding TypeScript-aware lint rules
- Making linting a blocking gate in CI

## Real Commands

```bash
# Initialize ESLint interactively
npm init @eslint/config

# Lint a directory
npx eslint src/

# Auto-fix everything possible
npx eslint --fix .

# Strict gate: no warnings allowed
npx eslint --ext .js,.ts --max-warnings 0

# Cache results for speed on big repos
npx eslint --cache --cache-location node_modules/.cache/eslint

# Machine-readable output
npx eslint --format json --output-file eslint-report.json .
```

## Example Config (eslint.config.js)

```js
export default [
  { ignores: ["dist/", "coverage/"] },
  ...js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      "no-unused-vars": "error",
      "@typescript-eslint/no-explicit-any": "warn"
    }
  }
];
```

## CI Gate

```yaml
- name: Lint
  run: npx eslint . --max-warnings 0
```

## Best Practices

- Use `--max-warnings 0` in CI so warnings can't accumulate
- Turn on `--cache` locally for speed, but allow cache to be written in CI
- Prefer flat config (`eslint.config.js`) over deprecated `.eslintrc`
- Run `--fix` first, then review the remaining errors manually

## Capabilities

### eslint-linting
Configure ESLint, run checks, auto-fix, and integrate with CI for JavaScript and TypeScript

**Parameters:**
- `ext` (string): File extensions to lint, e.g. .js,.jsx,.ts,.tsx
- `max-warnings` (integer): Exit non-zero when warnings exceed this count; 0 means no warnings allowed
- `quiet` (boolean): Report only errors, hiding warnings

**Commands:**
- `npx eslint src/`
- `npx eslint --fix .`
- `npx eslint --ext .js,.jsx,.ts,.tsx --max-warnings 0`
- `npx eslint --cache --report-unused-disable-directives`
- `npx eslint --format json --output-file eslint-report.json src/`

**Examples:**
- npx eslint src/ --rule 'no-console: error'
- npx eslint . --fix --ext .ts --quiet
- npx eslint --print-config src/index.ts | jq '.rules["no-console"]'

## References
- [ESLint user guide](https://eslint.org/docs/latest/user-guide/)
- [typescript-eslint docs](https://typescript-eslint.io/)
