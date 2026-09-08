---
trigger: glob
description: "Expert Salvo (Rust) reference covering handler functions, Router chains, middleware, and Server startup suited to building async web APIs in Rust. Use when working with salvo web, api or when the user mentions salvo web, api."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh"]
---

Expert Salvo (Rust) reference covering handler functions, Router chains, middleware, and Server startup suited to building async web APIs in Rust.

## Agentic Workflow: Read -> Reason -> Act (salvo)

You are **Salvo** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `salvo`
- Domain: Expert Salvo (Rust) reference covering handler functions, Router chains, middleware, and Server startup suited to building async web APIs in Rust.
- **salvo-web**: Build async Rust web APIs with the Salvo framework — `cargo new salvo-app && cd salvo-app && cargo add salvo`
- Check `knowledge` and `prerequisites: cargo`

### 2. Reason — think for `salvo`
- For `salvo-web`: Build async Rust web APIs with the Salvo framework — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `salvo` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `salvo:1117ab4d`

# Salvo (Rust web framework)

Expert skill for building async web APIs with Salvo.

## What this skill does

- Wires handler functions into a Router tree
- Starts an async HTTP server on a TcpListener
- Adds middleware for logging, CORS, and tracing

## When to use

- High-throughput Rust APIs that prefer hyper over full frameworks
- Services where handler composition with Router chains fits the design
- Replacing Actix for smaller, hyper-native deployments

## Real commands

```bash
# Scaffold
cargo new salvo-app && cd salvo-app && cargo add salvo

# Run
cargo run

# Exercise routes
curl -s http://localhost:5800/hello
curl -s -X POST http://localhost:5800/api/echo -d 'ping'
```

## Main example

```rust
use salvo::prelude::*;

#[handler]
async fn hello() -> &'static str {
    "Hello from Salvo"
}

#[handler]
async fn echo(req: &mut Request) -> String {
    req.parse_body::<String>().await.unwrap_or_default()
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .get(hello)
        .push(Router::with_path("api").push(Router::with_path("echo").post(echo)));
    Server::new(TcpListener::bind("0.0.0.0:5800")).serve(router).await;
}
```

## Testing

```bash
cargo run
curl -s http://localhost:5800/hello
curl -s -X POST http://localhost:5800/api/echo -d 'ping'
```

## Best practices

- Push path segments into Router::with_path chains for readable trees
- Use the #[handler] attribute so functions gain the trait impls
- Enable the features you need in cargo add to keep compile time low

## Capabilities

### salvo-web
Build async Rust web APIs with the Salvo framework

**Parameters:**
- `path` (string): Router path like hello or api/<id>
- `port` (integer): Bind port passed to TcpListener
- `handler` (string): Handler function name registered on the router

**Commands:**
- `cargo new salvo-app && cd salvo-app && cargo add salvo`
- `cargo run`
- `curl -s http://localhost:5800/hello`
- `curl -s -X POST http://localhost:5800/api/echo -d 'ping'`
- `cargo add tokio --features rt-multi-thread,macros`

**Examples:**
- cargo run
- curl -s http://localhost:5800/hello
- curl -s -X POST http://localhost:5800/api/echo -d 'ping'

## References
- [Salvo documentation](https://docs.rs/salvo/latest/salvo/)
- [Salvo repo](https://github.com/salvo-rs/salvo)
