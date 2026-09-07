---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Audits dependency licenses across ecosystems with licensee, license-checker, and go-licenses, enforcing allowlists in CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `licensee detect .`, `license-checker --failOn 'GPL;LGPL' --summary`
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

# License Compliance

Know every dependency's license and enforce policy in CI.

## When to Use

- Open-sourcing a component or product
- Vendor reviews and legal audits
- Adding a new dependency to a gated repo

## Detect licenses

```bash
licensee detect .
licensee detect --json | jq '.licenses[] | .key'
```

## npm inventory

```bash
npx license-checker --summary
npx license-checker --production --json > licenses.json
```

## Go inventory

```bash
go-licenses csv ./...
go-licenses check ./... --allowed_licenses=MIT,Apache-2.0
```

## Enforce policy

```bash
npx license-checker --onlyAllow 'MIT;Apache-2.0;ISC;BSD-2-Clause;BSD-3-Clause'
license-checker --failOn 'GPL;LGPL' --summary
```

Run the policy in CI on every PR that changes lockfiles.

## When a violation appears

1. Identify the package and version.
2. Check the license text, not just SPDX id.
3. Evaluate: replace, relicense (with author), or legal review.
4. Record the decision in the audit report.

## Best practices

- Keep a licenses.json artifact per release.
- Include attribution files with vendored code.
- Prefer permissive stacks (MIT/Apache) for libraries.
- Review license changes when upgrading major versions.

## Testing

```bash
licensee detect . --unlicensed
npx license-checker --failOn GPL --summary
```

Both should pass on main; fail on known-bad branches.

## Capabilities

### audit
Detect licenses for codebases and packages.

**Parameters:**
- `exclude` (string): Licenses to exclude from report
- `production` (string): Only production dependencies
- `allowed_licenses` (string): Comma-separated allowlist (go-licenses)

**Commands:**
- `licensee detect .`
- `licensee detect --json`
- `npx license-checker --summary`
- `npx license-checker --production --json > licenses.json`
- `go-licenses csv ./...`

**Examples:**
- licensee detect --json | jq '.licenses[] | .key'
- npx license-checker --summary --exclude 'MIT'
- go-licenses check ./... --allowed_licenses=MIT,Apache-2.0

### enforce
Gate builds on license policy.

**Parameters:**
- `failOn` (string): Licenses that fail the check
- `onlyAllow` (string): Allowed license list
- `unlicensed` (string): Report unlicensed code

**Commands:**
- `license-checker --failOn 'GPL;LGPL' --summary`
- `licensee detect --unlicensed --no-remote`
- `go-licenses check ./... --disallowed_types=forbidden`
- `npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-3-Clause'`
- `npm audit --omit=dev`

**Examples:**
- license-checker --failOn GPL --summary
- npx license-checker --onlyAllow 'MIT;Apache-2.0;ISC;BSD-2-Clause;BSD-3-Clause'
- go-licenses csv ./... | grep -i 'gpl'

## References
- [licensee](https://github.com/licensee/licensee)
- [license-checker](https://github.com/davglass/license-checker)
- [SPDX License List](https://spdx.org/licenses/)
