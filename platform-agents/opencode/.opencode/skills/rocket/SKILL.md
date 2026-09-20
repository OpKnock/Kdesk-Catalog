---
name: "rocket"
description: "Expert Rocket (Rust) reference covering routing with route attributes, state and guards, Rocket.toml config, and cargo build/run workflows suited to web APIs. Use when working with rocket web, api or when the user mentions rocket web, api."
---

Expert Rocket (Rust) reference covering routing with route attributes, state and guards, Rocket.toml config, and cargo build/run workflows suited to web APIs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cargo new hello-rocket && cd hello-rocket && cargo add rocke`
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

# Rocket (Rust)

Expert skill for building web APIs with the Rocket framework.

## What this skill does

- Defines typed routes with the get/post macro attributes
- Shares mutable state via State<T> and protects routes with guards
- Configures ports, limits, and profiles through Rocket.toml

## When to use

- Greenfield Rust HTTP APIs with minimal boilerplate
- Services that want compile-time route and request typing
- Prototyping an endpoint before hardening it

## Real commands

```bash
# Scaffold
cargo new hello-rocket && cd hello-rocket && cargo add rocket

# Run with the dev profile
cargo run

# Exercise routes
curl -s http://localhost:8000/hello/Ada
curl -X POST http://localhost:8000/submit -H 'Content-Type: application/json' -d '{"title":"hi"}'

# Production build
cargo build --release
```

## Routes example

```rust
use rocket::{get, post, State};
use std::sync::atomic::{AtomicU64, Ordering};

#[get("/hello/<name>")]
fn hello(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[post("/submit", data = "<form>")]
fn submit(form: Form<Title>) -> String {
    form.into_inner().title
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![hello, submit])
        .manage(AtomicU64::new(0))
}
```

## Rocket.toml

```toml
[default]
port = 8000

[release]
port = 8080
workers = 16
```

## Testing

```bash
cargo run
curl -s http://localhost:8000/hello/Ada
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:8000/submit -d 'title=test'
```

## Best practices

- Keep routes in a routes module mounted once in rocket()
- Use managed state for shared counters/caches, not statics
- Build release for deployment; dev profile compiles faster

## Capabilities

### rocket-web
Build Rust web APIs with Rocket: routes, state, config

**Parameters:**
- `route_path` (string): Path expression like /hello/<name>
- `port` (integer): Port from Rocket.toml or ROCKET_PORT
- `profile` (string): Rocket profile: default, release, debug

**Commands:**
- `cargo new hello-rocket && cd hello-rocket && cargo add rocket`
- `cargo run`
- `curl -s http://localhost:8000/hello/Ada`
- `curl -X POST http://localhost:8000/submit -H 'Content-Type: application/json' -d '{"title":"hi"}'`
- `cargo build --release`

**Examples:**
- cargo run
- curl -s http://localhost:8000/hello/Ada
- curl -s -X POST http://localhost:8000/submit -H 'Content-Type: application/json' -d '{"title":"hi"}'

## References
- [Rocket guide](https://rocket.rs/v0.5/guide/)
- [Rocket API reference](https://api.rocket.rs/v0.5/rocket/)
