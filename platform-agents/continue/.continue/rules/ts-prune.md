---
name: "ts-prune"
description: "Finds unused exports and dead code in TypeScript projects with ts-prune."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

# ts-prune

Finds unused exports and dead code in TypeScript projects with ts-prune.

## Instructions

# ts-prune

Finds unused exports in TypeScript codebases by analyzing the type graph, helping
delete dead code safely.

## When to Use

- Cleaning up dead exports before a refactor
- Enforcing no-unused-exports in CI
- Locating public API surface that nothing consumes

## Real Commands

```bash
# Install
dev-npx ts-prune
npm install --save-dev ts-prune

# Default run
npx ts-prune

# With explicit tsconfig
npx ts-prune -p tsconfig.json

# Fail in CI
npx ts-prune --error

# Ignore test files
npx ts-prune --ignore "src/**/*.test.ts"

# JSON for scripting
npx ts-prune --json > unused-exports.json

# Skip vendored code
npx ts-prune -p tsconfig.build.json --skip node_modules
```

## Output Format

```
src/utils/format.ts:12 - formatDate
src/api/client.ts:34 - HttpClient
```

## Best Practices

- Scope with `--ignore` for tests and generated files (e.g. API client stubs)
- Delete exports in batches and rely on type-check + tests
- Keep `--error` in CI to prevent regression
- Review the report before bulk-deleting; entry points may be imported dynamically

## Example Response

Lists each unused export as file:line with the symbol name, then deletes them in
small batches, running tsc --noEmit after each.

## Capabilities

### ts-prune
Detect unused exports and configure failure thresholds

**Commands:**
- `npx ts-prune`
- `npx ts-prune -p tsconfig.json`
- `npx ts-prune --error`
- `npx ts-prune --ignore "src/**/*.test.ts"`
- `npx ts-prune -s src/ --json > unused.json`

**Examples:**
- npx ts-prune --error | head -30
- npx ts-prune -p tsconfig.build.json --skip 'node_modules'
- npx ts-prune --allowUnreachableCode