---
name: "cargo-audit"
description: "Audits Rust dependencies for known vulnerabilities with cargo-audit: advisories, fix suggestions, and CI gating. Use when working with cargo audit scan, cargo fix, code quality or when the user mentions cargo audit scan, cargo fix, code quality."
license: "MIT"
compatibility: "Requires cargo."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(cargo:*)"
---

Audits Rust dependencies for known vulnerabilities with cargo-audit: advisories, fix suggestions, and CI gating.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cargo install cargo-audit`, `cargo update -p vulnerable-crate`
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

# cargo-audit

Audit Rust dependencies for vulnerabilities.

## When to Use

- Before every release
- In CI on every merge
- When adding or upgrading dependencies
- Investigating reported CVEs affecting your crates

## Commands

```bash
# Install
cargo install cargo-audit

# Scan the lockfile
cargo audit

# No network (use cached advisory db)
cargo audit -n

# Ignore known accepted advisories
cargo audit --ignore RUSTSEC-2024-0001

# Update a vulnerable crate
cargo update -p vulnerable-crate

# Find who depends on a crate
cargo tree -i openssl

# Preview dependency updates
cargo outdated
```

## CI Example

```yaml
- name: Audit dependencies
  run: cargo audit --deny warnings
```

## Best Practices

- Keep Cargo.lock committed for applications
- Run cargo audit --deny warnings in CI
- Review ignored advisories; never ignore silently
- Update directly vulnerable crates first (cargo update -p)
- Check the advisory details for patched versions
- Pin the cargo-audit version in CI for stable output

## Capabilities

### cargo-audit-scan
Scan dependency trees for vulnerabilities.

**Parameters:**
- `ignore` (string): Comma-separated RUSTSEC ids to ignore
- `file` (string): Lockfile path

**Commands:**
- `cargo install cargo-audit`
- `cargo audit`
- `cargo audit --ignore RUSTSEC-2024-0001`
- `cargo audit -n`
- `cargo audit --version`

**Examples:**
- cargo audit --file Cargo.lock
- cargo audit --ignore RUSTSEC-2023-0021,RUSTSEC-2024-0010
- cargo audit --db ~/.cargo/advisory-db

### cargo-fix
Update vulnerable dependencies.

**Parameters:**
- `crate` (string): Crate name
- `precise` (string): Exact version

**Commands:**
- `cargo update -p vulnerable-crate`
- `cargo update --precise 1.2.3`
- `cargo tree -i vulnerable-crate`
- `cargo outdated`

**Examples:**
- cargo tree -i openssl
- cargo update -p openssl --precise 0.10.66
- cargo audit && echo "clean"

## References
- [cargo-audit on GitHub](https://github.com/rustsec/rustsec)
- [RustSec Advisory DB](https://rustsec.org/advisories/)
