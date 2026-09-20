---
name: "rust"
description: "Builds Rust backends: cargo projects, workspace management, builds, tests, benchmarks, and clippy-driven quality."
type: knowledge
triggers: ["rust", "cargo-build", "cargo-quality"]
---

# rust

Builds Rust backends: cargo projects, workspace management, builds, tests, benchmarks, and clippy-driven quality.

## Instructions

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
