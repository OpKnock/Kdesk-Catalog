---
name: "Warp"
description: "Creates HTTP APIs with the Warp web framework in Rust. Uses filter-based routing with combinators, adds warp and tokio dependencies via cargo, runs the server, and tests with cargo test and curl. Use when working with warp api, rust or when the user mentions warp api, rust."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh"]
alwaysApply: false
---

Creates HTTP APIs with the Warp web framework in Rust. Uses filter-based routing with combinators, adds warp and tokio dependencies via cargo, runs the server, and tests with cargo test and curl.

## Agentic Workflow: Read -> Reason -> Act (warp)

You are **Warp** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `warp`
- Domain: Creates HTTP APIs with the Warp web framework in Rust. Uses filter-based routing with combinators, adds warp and tokio dependencies via cargo, runs the server, and tests with cargo test and curl.
- **warp-api**: Create and run Warp-based Rust HTTP services — `cargo new my-api`
- Check `knowledge` and `prerequisites: cargo`

### 2. Reason — think for `warp`
- For `warp-api`: Create and run Warp-based Rust HTTP services — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `warp` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `warp:c7f1c0db`

# Warp (Rust)

## What this skill does

Create HTTP APIs with the Warp web framework in Rust. Warp is filter-based: you compose routes from path, method, header, and body filters with combinators like `and`, `or`, and `map`.

## When to use

- Writing typed, safe Rust HTTP services
- Building proxy or middleware-style APIs
- Learning filter composition

## Real commands

```bash
# New binary project
cargo new my-api
cd my-api

# Add dependencies
cargo add warp tokio
cargo add tokio --features tokio/full

# Run dev server
cargo run

# Build release
cargo build --release

# Test
cargo test

# Verify
curl -s http://localhost:3030/api/health
```

## Minimal main.rs

```rust
use warp::Filter;

#[tokio::main]
async fn main() {
    let health = warp::path!("api" / "health")
        .map(|| warp::reply::json(&serde_json::json!({"status": "ok"})));

    warp::serve(health).run(([127, 0, 0, 1], 3030)).await;
}
```

## JSON POST with body

```rust
let create = warp::path!("items")
    .and(warp::post())
    .and(warp::body::json())
    .map(|item: Item| { /* store */ warp::reply::with_status("created", StatusCode::CREATED) });
```

## Best practices

- Use `warp::reject` + `warp::recover` for typed error handling
- Compose small filters instead of one large route
- Test filters with `warp::test::request()`
- Enable `tokio/full` for real-world I/O

## Testing

```rust
#[tokio::test]
async fn test_health() {
    let res = warp::test::request().path("/api/health").reply(&health).await;
    assert_eq!(res.status(), 200);
}
```

## Capabilities

### warp-api
Create and run Warp-based Rust HTTP services

**Parameters:**
- `port` (integer): Bind port for the warp server (default 3030)
- `features` (string): Cargo features for tokio, e.g. tokio/full

**Commands:**
- `cargo new my-api`
- `cargo add warp tokio`
- `cargo run`
- `cargo test`
- `curl -s http://localhost:3030/api/health`

**Examples:**
- cargo add warp tokio --features tokio/full
- cargo build --release
- curl -s -X POST http://localhost:3030/items -H "Content-Type: application/json" -d "{\"name\":\"widget"}"

## References
- [warp docs.rs](https://docs.rs/warp)
- [warp GitHub](https://github.com/seanmonstar/warp)
- [Tokio docs](https://docs.rs/tokio)