---
name: "graphql-juniper"
description: "GraphQL in Rust with Juniper: define schemas with Rust types and macros, run the server, and test queries. Use when working with juniper development, api or when the user mentions juniper development, api."
---

GraphQL in Rust with Juniper: define schemas with Rust types and macros, run the server, and test queries.

## Agentic Workflow: Read -> Reason -> Act (graphql-juniper)

You are **Graphql Juniper** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `graphql-juniper`
- Domain: GraphQL in Rust with Juniper: define schemas with Rust types and macros, run the server, and test queries.
- **juniper-development**: Build Juniper schemas, integrate with Actix/Axum, and run queries. — `cargo add juniper actix-web juniper_actix`
- Check `knowledge` and `prerequisites: cargo`

### 2. Reason — think for `graphql-juniper`
- For `juniper-development`: Build Juniper schemas, integrate with Actix/Axum, and run queries. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-juniper` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-juniper:77bee2da`

# GraphQL Juniper

## What this skill does

Juniper brings GraphQL to Rust with derive macros: `#[derive(GraphQLObject)]`, `graphql_object!`, and `graphql_schema!`. Context passes shared state to resolvers; integrations cover Actix and Axum.

## When to use

- Rust services needing typed GraphQL
- High-throughput backends that want zero-copy serialization
- Rust teams already using Actix or Axum

## Real commands

```bash
# Dependencies
cargo add juniper actix-web juniper_actix

# Run, build, test
cargo run
cargo build --release
cargo test

# Query the server
curl -s -X POST http://localhost:8080/graphql -H 'Content-Type: application/json' -d '{"query":"{ hero { name } }"}' | jq
```

## Schema example

```rust
use juniper::{graphql_object, EmptyMutation, RootNode};

struct Hero { name: String }

#[graphql_object]
impl Hero {
    fn name(&self) -> &str { &self.name }
}

struct Query;

#[graphql_object]
impl Query {
    fn hero() -> Hero {
        Hero { name: "R2-D2".into() }
    }
}

type Schema = RootNode<'static, Query, EmptyMutation>;
```

## Testing

```bash
# Execute a query in a unit test
cargo test -- --nocapture
# curl the playground
curl -s -X POST http://localhost:8080/graphql -H 'Content-Type: application/json' -d '{"query":"{ __typename }"}' | jq
```

## Best practices

- Keep resolvers thin; call service layers.
- Pass DB pools via Context, not statics.
- Derive GraphQLObject for pure data types only.
- Test schema construction at compile time; it fails loudly.
- Pin juniper_actix to the same minor as actix-web.

## Capabilities

### juniper-development
Build Juniper schemas, integrate with Actix/Axum, and run queries.

**Parameters:**
- `crate` (string): juniper integration crate
- `endpoint` (string): GraphQL endpoint path
- `context-type` (string): Rust context type passed to resolvers

**Commands:**
- `cargo add juniper actix-web juniper_actix`
- `cargo run`
- `cargo build --release`
- `cargo test`
- `curl -s -X POST http://localhost:8080/graphql -H 'Content-Type: application/json' -d '{"query":"{ hero { name } }"}' | jq`

**Examples:**
- cargo add juniper actix-web juniper_actix && cargo run
- curl -s -X POST http://localhost:8080/graphql -H 'Content-Type: application/json' -d '{"query":"{ hero { name } }"}' | jq
- cargo test

## References
- [Juniper docs](https://graphql-rust.github.io/juniper/)
- [Juniper GitHub](https://github.com/graphql-rust/juniper)
