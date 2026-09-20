---
trigger: glob
description: "Builds HTTP APIs in Rust with Axum: routing, extractors, shared state, middleware, and testing with tower."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh"]
---

# Axum

Builds HTTP APIs in Rust with Axum: routing, extractors, shared state, middleware, and testing with tower.

## Instructions

# Axum

## What this skill does

Builds HTTP APIs in Rust with Axum: routing, extractors, shared state, middleware (CORS/tracing), and route testing with tower.

## When to use

- A new Rust REST API with tokio
- Adding extractors, state, or middleware to an existing app
- Fast, compile-time-safe routing

## Real commands

```bash
cargo new axum-api
cargo add axum tokio --features tokio/full
cargo add serde --features derive
cargo add tower-http --features cors,trace

cargo run
curl -s http://localhost:3000/health

cargo test
cargo clippy -- -D warnings
cargo build --release
```

## Minimal server

```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(|| async { "ok" }));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## State + extractors

```rust
#[derive(Clone)]
struct Db { pool: String }

let app = Router::new()
    .route("/users/:id", get(get_user))
    .with_state(Db { pool: "postgres://db".into() });

async fn get_user(State(db): State<Db>, Path(id): Path<u64>) -> String {
    format!("user {id} via {}", db.pool)
}
```

## Testing

- Test routers with tower::ServiceExt::oneshot
- Use `cargo test` and clippy in CI

## Best practices

- Share dependencies via state, not globals
- Use path parameters and typed extractors instead of manual parsing
- Layer CORS via tower-http, not hand-rolled middleware

## Capabilities

### project-setup
Create an Axum project and add dependencies.

**Commands:**
- `cargo new axum-api`
- `cargo add axum tokio --features tokio/full`
- `cargo add serde --features derive`
- `cargo add tower-http --features cors`
- `cargo build`

**Examples:**
- cargo new axum-api && cargo add axum tokio --features tokio/full
- cargo add axum --features multipart,ws
- cargo add tower-http --features trace,cors

### serve-and-test
Run the server and test routes with tower ServiceExt.

**Commands:**
- `cargo run`
- `curl -s http://localhost:3000/health`
- `cargo test`
- `cargo clippy -- -D warnings`
- `cargo build --release`

**Examples:**
- cargo run && curl -s http://localhost:3000/health
- cargo test -- --nocapture
- cargo clippy --all-targets -- -D warnings
