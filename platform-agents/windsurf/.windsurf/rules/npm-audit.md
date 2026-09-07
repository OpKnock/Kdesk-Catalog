---
trigger: glob
description: "Run npm audits, fix vulnerable packages, and enforce severity thresholds. Use when working with npm audit, code quality or when the user mentions npm audit, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Run npm audits, fix vulnerable packages, and enforce severity thresholds.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm audit`
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

# npm Audit

Checks your installed dependency tree against the npm advisory database and reports
known vulnerabilities with severities and fix versions.

## When to Use

- Before release to catch critical advisories
- After adding new dependencies
- In CI as a security gate

## Real Commands

```bash
# Full audit
npm audit

# Audit production dependencies only
npm audit --production

# Automatically fix non-breaking upgrades
npm audit fix

# Preview the changes without applying
npm audit fix --dry-run

# Force semver-major (breaking) fixes
npm audit fix --force

# Machine-readable report
npm audit --json > audit-report.json

# Fail on moderate+ only in CI
npm audit --audit-level=moderate
```

## Fix Strategy

1. Run `npm audit fix --dry-run` and review what would change
2. Apply `npm audit fix` for safe patches
3. For remaining items, upgrade the direct dependency manually and re-audit
4. Use `--force` only when you accept breaking changes; verify with the test suite

## CI

```yaml
- name: Audit deps
  run: npm audit --audit-level=high --omit=dev
```

## Best Practices

- Run `npm audit --omit=dev` for production builds
- Never blanket-apply `--force`; review the diff first
- If no fix exists, the advisory page shows mitigations - document the decision

## Example Response

Lists each vulnerable package as name@version -> Patched in X, with severity and
advisory URL; then proposes the fix command.

## Capabilities

### npm-audit
Run npm audits, fix vulnerable packages, and enforce severity thresholds

**Parameters:**
- `audit-level` (string): Minimum severity to fail: info, low, moderate, high, critical
- `omit` (string): Exclude dependency types, e.g. dev
- `force` (boolean): Apply breaking semver-major fixes

**Commands:**
- `npm audit`
- `npm audit --production`
- `npm audit fix`
- `npm audit fix --force`
- `npm audit --json > audit-report.json`

**Examples:**
- npm audit --audit-level=high
- npm audit fix --dry-run
- npm audit --omit=dev --json | jq '.metadata.vulnerabilities'

## References
- [npm audit docs](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [npm audit fix docs](https://docs.npmjs.com/cli/v10/commands/npm-audit-fix)
