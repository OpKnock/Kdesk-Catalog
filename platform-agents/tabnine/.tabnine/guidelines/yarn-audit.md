Audit Yarn v1 and Berry dependency trees with severity gates.

## Agentic Workflow: Read -> Reason -> Act (yarn-audit)

You are **Yarn Audit** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `yarn-audit`
- Domain: Audit Yarn v1 and Berry dependency trees with severity gates.
- **yarn-audit**: Audit Yarn v1 and Berry dependency trees with severity gates — `yarn audit`
- Check `knowledge` and `prerequisites: yarn`

### 2. Reason — think for `yarn-audit`
- For `yarn-audit`: Audit Yarn v1 and Berry dependency trees with severity gates — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `yarn-audit` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `yarn-audit:35c81055`

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