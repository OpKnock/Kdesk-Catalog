---
name: "rust"
description: "Builds Rust backends: cargo projects, workspace management, builds, tests, benchmarks, and clippy-driven quality. Use when working with cargo build, cargo quality, backend or when the user mentions cargo build, cargo quality, backend."
type: knowledge
triggers: ["rust", "cargo-build", "cargo-quality"]
---

Builds Rust backends: cargo projects, workspace management, builds, tests, benchmarks, and clippy-driven quality.

## Agentic Workflow: Read -> Reason -> Act (rust)

You are **rust** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `rust`
- Domain: Builds Rust backends: cargo projects, workspace management, builds, tests, benchmarks, and clippy-driven quality.
- **cargo-build**: Create and build Rust projects and workspaces. — `cargo new myapp`
- **cargo-quality**: Test, lint, and benchmark Rust code. — `cargo test`
- Check `knowledge` and `prerequisites: cargo`

### 2. Reason — think for `rust`
- For `cargo-build`: Create and build Rust projects and workspaces. — decide which checks to run
- For `cargo-quality`: Test, lint, and benchmark Rust code. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rust` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rust:eca9d68a`

# Rust

Backend development with the Rust toolchain.

## When to Use

- Performance-critical services and hot paths
- Network daemons with tokio/axum
- Tools that ship as single static binaries
- Systems where memory safety matters

## Commands

```bash
# New project
cargo new myapp
cargo new myapp --bin

# Build
cargo build
cargo build --release

# Add deps
cargo add tokio --features full
cargo add axum serde --features serde/derive

# Run
cargo run

# Test
cargo test
cargo test -- --nocapture

# Lint
cargo clippy -- -D warnings

# Format
cargo fmt --check

# Bench
cargo bench
```

## Axum Example

```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(|| async { "ok" }));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## Best Practices

- Treat clippy warnings as errors in CI: cargo clippy -- -D warnings
- Use feature flags to keep dependencies lean
- Prefer error types over panics in library code
- Benchmark hot paths with cargo bench before optimizing
- Pin lockfile (Cargo.lock) for applications
- Test with cargo test --workspace in monorepos

## Capabilities

### cargo-build
Create and build Rust projects and workspaces.

**Parameters:**
- `bin` (string): Binary name
- `features` (string): Cargo features to enable

**Commands:**
- `cargo new myapp`
- `cargo build`
- `cargo build --release`
- `cargo run`
- `cargo add tokio --features full`

**Examples:**
- cargo new myapp --bin
- cargo build --release --features rustls
- cargo install cargo-watch

### cargo-quality
Test, lint, and benchmark Rust code.

**Parameters:**
- `test-filter` (string): Test name filter
- `all-targets` (boolean): Lint all targets including tests

**Commands:**
- `cargo test`
- `cargo test -- --nocapture`
- `cargo clippy -- -D warnings`
- `cargo fmt --check`
- `cargo bench`

**Examples:**
- cargo test --workspace
- cargo clippy --all-targets -- -D warnings
- cargo fmt --all -- --check

## References
- [Rust Book](https://doc.rust-lang.org/book/)
- [Cargo Book](https://doc.rust-lang.org/cargo/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
