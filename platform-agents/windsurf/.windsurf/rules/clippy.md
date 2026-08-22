---
trigger: glob
description: "Lints Rust code with clippy: lints, autofixes, custom configs, and CI enforcement with -D warnings."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh"]
---

# Clippy

Lints Rust code with clippy: lints, autofixes, custom configs, and CI enforcement with -D warnings.

## Instructions

# Clippy

The Rust linter with smart suggestions.

## When to Use

- Catching common Rust mistakes before review
- Enforcing strict quality gates in CI
- Modernizing old code with --fix
- Applying pedantic rules on codebases that want them

## Commands

```bash
# Install the component
rustup component add clippy

# Default lint set
cargo clippy

# Block on any warning
cargo clippy -- -D warnings

# All targets (tests, benches, examples)
cargo clippy --all-targets --all-features

# Auto-fix
cargo clippy --fix --allow-dirty

# Select lint groups
cargo clippy -- -W clippy::nursery
cargo clippy -- -D clippy::pedantic

# Allow specific lints
cargo clippy -- -A clippy::too_many_arguments
```

## Config Example

```toml
# Cargo.toml
[lints.clippy]
all = "warn"
pedantic = "warn"
unwrap_used = "warn"
```

## Best Practices

- Use -D warnings in CI; denials catch regressions
- Run cargo clippy --fix regularly to clean up
- Enable pedantic incrementally with per-lint allows
- Keep -A list documented for deliberate exceptions
- Run on all targets, not just lib/bin
- Format with cargo fmt before clippy for stable line numbers

## Capabilities

### clippy-lint
Run clippy over the crate.

**Commands:**
- `cargo clippy`
- `cargo clippy -- -D warnings`
- `cargo clippy --all-targets --all-features`
- `cargo clippy --fix --allow-dirty`
- `cargo clippy -- -A clippy::too_many_arguments`

**Examples:**
- cargo clippy --all-targets -- -D warnings
- cargo clippy --fix --allow-dirty --allow-staged
- cargo clippy --tests -- -A clippy::unwrap_used

### clippy-config
Configure lint levels per crate.

**Commands:**
- `cargo clippy -- -D clippy::pedantic`
- `cargo clippy -- -W clippy::nursery`
- `cargo clippy --message-format json`
- `rustup component add clippy`

**Examples:**
- cargo clippy -- -D warnings -D clippy::pedantic
- cargo clippy -- -A clippy::needless_return
