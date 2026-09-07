---
trigger: glob
description: "Audit Yarn v1 and Berry dependency trees with severity gates. Use when working with yarn audit, code quality or when the user mentions yarn audit, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Audit Yarn v1 and Berry dependency trees with severity gates.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `yarn audit`
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

# Yarn Audit

Scans Yarn-managed dependencies against vulnerability advisories. Syntax differs
between Yarn v1 (classic) and Berry (v2+).

## When to Use

- Pre-release security check for Yarn projects
- CI security gate
- After a dependency bump to confirm no new advisories

## Real Commands

```bash
# Yarn v1 (classic)
yarn audit

# Only high+ in v1
yarn audit --level high

# JSON in v1
yarn audit --json > audit.json

# Yarn Berry: production deps only
yarn npm audit --environment production

# Berry: recursive (dependencies of dependencies)
yarn npm audit --recursive

# Berry: minimum severity
yarn npm audit --severity high
```

## Fixing Findings

```bash
# v1: no auto-fix; upgrade the direct dependency
yarn upgrade lodash@^4.17.21

# Berry: upgrade with constraints
yarn up lodash@^4.17.21 --exact
```

## CI

```yaml
# v1
- name: Audit
  run: yarn audit --level high --json || exit 0 # capture and parse
```

## Best Practices

- Know which Yarn major you run: `yarn --version` before choosing flags
- In Berry, prefer `--environment production` for release checks
- There is no `yarn audit fix`; upgrade packages explicitly and re-audit
- Audit after every lockfile change

## Example Response

Reports each advisory with package, severity, and patched range, then proposes
the exact `yarn upgrade` command per vulnerable package.

## Capabilities

### yarn-audit
Audit Yarn v1 and Berry dependency trees with severity gates

**Parameters:**
- `level` (string): Minimum severity to report: info, low, moderate, high, critical (v1)
- `environment` (string): Berry: production or development
- `json` (boolean): Machine-readable JSON output

**Commands:**
- `yarn audit`
- `yarn audit --level high`
- `yarn audit --json`
- `yarn npm audit --environment production`
- `yarn npm audit --recursive`

**Examples:**
- yarn audit --groups dependencies
- yarn audit --json > audit.json
- yarn npm audit --severity high

## References
- [yarn audit docs (v1)](https://classic.yarnpkg.com/lang/en/docs/cli/audit/)
- [yarn npm audit docs (Berry)](https://yarnpkg.com/cli/npm/audit)
