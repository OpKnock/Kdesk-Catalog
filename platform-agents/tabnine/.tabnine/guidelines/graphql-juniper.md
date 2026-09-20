# Graphql Juniper

GraphQL in Rust with Juniper: define schemas with Rust types and macros, run the server, and test queries.

## Instructions

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