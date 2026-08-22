---
name: "Cargo Audit"
description: "Audits Rust dependencies for known vulnerabilities with cargo-audit: advisories, fix suggestions, and CI gating."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Cargo Audit

Audits Rust dependencies for known vulnerabilities with cargo-audit: advisories, fix suggestions, and CI gating.

## Instructions

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

**Commands:**
- `cargo update -p vulnerable-crate`
- `cargo update --precise 1.2.3`
- `cargo tree -i vulnerable-crate`
- `cargo outdated`

**Examples:**
- cargo tree -i openssl
- cargo update -p openssl --precise 0.10.66
- cargo audit && echo "clean"