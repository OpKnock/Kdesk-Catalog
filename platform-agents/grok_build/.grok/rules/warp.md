Creates HTTP APIs with the Warp web framework in Rust. Uses filter-based routing with combinators, adds warp and tokio dependencies via cargo, runs the server, and tests with cargo test and curl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cargo new my-api`
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