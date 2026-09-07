---
applyTo: "**/*.r **/*.sh **/*.{ts,tsx}"
---

Tracks and enforces code quality metrics over time with betterer: type coverage, lint counts, and complexity budgets that never regress.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx betterer init`, `npx betterer --ci`
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
