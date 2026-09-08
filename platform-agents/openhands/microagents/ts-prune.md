---
name: "ts-prune"
description: "Finds unused exports and dead code in TypeScript projects with ts-prune. Use when working with ts prune, code quality or when the user mentions ts prune, code quality."
type: knowledge
triggers: ["ts-prune"]
---

Finds unused exports and dead code in TypeScript projects with ts-prune.

## Agentic Workflow: Read -> Reason -> Act (ts-prune)

You are **ts-prune** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `ts-prune`
- Domain: Finds unused exports and dead code in TypeScript projects with ts-prune.
- **ts-prune**: Detect unused exports and configure failure thresholds — `npx ts-prune`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `ts-prune`
- For `ts-prune`: Detect unused exports and configure failure thresholds — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ts-prune` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ts-prune:810be36e`

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

**Parameters:**
- `project` (string): Path to tsconfig.json
- `error` (boolean): Exit with code 1 if unused exports exist (CI mode)
- `ignore` (string): Regex of files to skip

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

## References
- [ts-prune GitHub](https://github.com/nadeesha/ts-prune)
- [ts-prune npm](https://www.npmjs.com/package/ts-prune)
