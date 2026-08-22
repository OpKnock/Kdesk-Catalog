# Rocket

Expert Rocket (Rust) reference covering routing with route attributes, state and guards, Rocket.toml config, and cargo build/run workflows suited to web APIs.

## Instructions

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