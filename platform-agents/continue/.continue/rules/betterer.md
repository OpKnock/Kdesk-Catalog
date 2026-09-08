---
name: "betterer"
description: "Tracks and enforces code quality metrics over time with betterer: type coverage, lint counts, and complexity budgets that never regress. Use when working with betterer core, betterer config, code quality or when the user mentions betterer core, betterer config, code quality."
globs: ["**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

Tracks and enforces code quality metrics over time with betterer: type coverage, lint counts, and complexity budgets that never regress.

## Agentic Workflow: Read -> Reason -> Act (betterer)

You are **betterer** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `betterer`
- Domain: Tracks and enforces code quality metrics over time with betterer: type coverage, lint counts, and complexity budgets that never regress.
- **betterer-core**: Initialize, run, and update betterer metrics. — `npx betterer init`
- **betterer-config**: Configure custom tests and thresholds. — `npx betterer --ci`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `betterer`
- For `betterer-core`: Initialize, run, and update betterer metrics. — decide which checks to run
- For `betterer-config`: Configure custom tests and thresholds. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `betterer` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `betterer:7dcf20af`

# Betterer

Prevent code quality regressions over time.

## When to Use

- Inheriting a codebase with existing lint/type debt
- Ensuring debt only decreases, never increases
- Gating merges on quality metric budgets
- Tracking coverage, complexity, or TODO counts

## Commands

```bash
# Init
npx betterer init

# Run and compare against baseline
npx betterer

# Update baseline after intentional improvements
npx betterer --update

# Strict: any regression fails
npx betterer --strict

# CI mode
npx betterer --ci

# Precommit check
npx betterer --precommit
```

## Config Example

```typescript
// .betterer.ts
import { ts } from "@betterer/typescript";

export default {
  "no unused": ts.noUnusedLocals("./src/**/*.ts"),
  "test coverage": coverage(...),
};
```

## Best Practices

- Run betterer in CI; never let results regress
- Update baselines only with an explicit, reviewed change
- Use --strict in CI to catch even unchanged failures
- Combine with eslint/tsc outputs for a single quality gate
- Keep the baseline file in version control
- Document why each baseline entry exists

## Capabilities

### betterer-core
Initialize, run, and update betterer metrics.

**Parameters:**
- `update` (boolean): Update baseline results
- `strict` (boolean): Reject unchanged results as failures

**Commands:**
- `npx betterer init`
- `npx betterer`
- `npx betterer --update`
- `npx betterer --strict`
- `npx betterer --check-timestamps`

**Examples:**
- npx betterer --update --workers 4
- npx betterer --precommit
- npx betterer --config .betterer.ts

### betterer-config
Configure custom tests and thresholds.

**Parameters:**
- `ci` (boolean): CI-friendly mode
- `workers` (integer): Worker processes for checks

**Commands:**
- `npx betterer --ci`
- `npx betterer --cache`
- `npx betterer --silent`
- `npm run betterer`

**Examples:**
- npx betterer --ci --silent
- npx betterer --cache-dir .cache/betterer

## References
- [Betterer Docs](https://phenomnomnominal.github.io/betterer/)
- [Betterer on GitHub](https://github.com/phenomnomnominal/betterer)