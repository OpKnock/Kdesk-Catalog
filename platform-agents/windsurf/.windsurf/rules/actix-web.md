---
trigger: glob
description: "Builds high-performance HTTP APIs in Rust with Actix Web: scaffolding, routing, JSON extractors, middleware, and release builds."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh"]
---

# Actix Web

Builds high-performance HTTP APIs in Rust with Actix Web: scaffolding, routing, JSON extractors, middleware, and release builds.

## Instructions

# Actix Web

## What this skill does

Develops HTTP services in Rust with Actix Web: scaffolding projects, defining routes and state, extracting typed JSON payloads, adding middleware, and producing release binaries.

## When to use

- Building a new Rust REST API
- Adding JSON endpoints, middleware, or WebSockets to an Actix app
- Tuning a server build for production

## Real commands

```bash
cargo new my-api
cargo add actix-web serde --features serde/derive

cargo run
curl http://localhost:8080/health

# Production build
cargo build --release
ACTIX_WORKERS=4 ./target/release/my-api

# Lint and test
cargo clippy -- -D warnings
cargo test
```

## Minimal server

```rust
use actix_web::{get, App, HttpServer, Responder};

#[get("/health")]
async fn health() -> impl Responder { "ok" }

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(health))
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
}
```

## JSON endpoint

```rust
#[derive(Deserialize)]
struct User { name: String }

#[post("/users")]
async fn create(user: web::Json<User>) -> HttpResponse {
    HttpResponse::Created().json(user.0)
}
```

## Testing

- Unit-test handlers with actix_web::test::init_service + TestRequest
- Run `cargo test` for handlers and `cargo clippy` in CI

## Best practices

- Put app state behind web::Data<T> instead of statics
- Use --release builds in production; debug builds are much slower
- Set ACTIX_WORKERS to the number of cores

## Capabilities

### project-scaffold
Create and configure a new Actix Web project with Cargo.

**Commands:**
- `cargo new my-api`
- `cargo add actix-web`
- `cargo add serde --features derive`
- `cargo build`
- `cargo run`

**Examples:**
- cargo new my-api && cargo add actix-web@4
- cargo add actix-web --features openssl
- cargo add actix-cors

### serve-and-test
Build, run, lint, and test the Actix server.

**Commands:**
- `cargo build --release`
- `cargo clippy -- -D warnings`
- `cargo test`
- `cargo run --release`
- `curl -s http://localhost:8080/health`

**Examples:**
- cargo clippy --all-targets -- -D warnings
- cargo test -- --nocapture
- cargo build --release && ./target/release/my-api
