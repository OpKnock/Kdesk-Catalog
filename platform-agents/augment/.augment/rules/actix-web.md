---
type: agent_requested
description: "Builds high-performance HTTP APIs in Rust with Actix Web: scaffolding, routing, JSON extractors, middleware, and release builds. Use when working with project scaffold, serve and test, api or when the user mentions project scaffold, serve and test, api."
---

Builds high-performance HTTP APIs in Rust with Actix Web: scaffolding, routing, JSON extractors, middleware, and release builds.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cargo new my-api`, `cargo build --release`
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

**Parameters:**
- `features` (string): Cargo features for actix-web (openssl, client)
- `crate` (string): Additional crate, e.g. actix-cors or serde_json

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

**Parameters:**
- `port` (number): Bind port (default 8080)
- `workers` (number): Actix worker threads via ACTIX_WORKERS env

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

## References
- [Actix Web Docs](https://actix.rs/docs)
- [Actix Web API Reference](https://docs.rs/actix-web)
- [Actix Examples](https://github.com/actix/examples)