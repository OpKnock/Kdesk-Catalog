---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# Graphql Federation

Apollo Federation: build supergraph schemas from subgraph services, compose with rover, and operate the gateway/router.

## Instructions

# GraphQL Federation

## What this skill does

Federation splits one GraphQL API across subgraph services, each owning types it defines. Apollo Router serves the composed supergraph; rover introspects, composes, publishes, and checks subgraphs.

## When to use

- Multiple teams owning different domains behind one graph
- Adding a new service to an existing federated graph
- Composing the supergraph in CI

## Real commands

```bash
# Introspect a subgraph
rover subgraph introspect http://orders:4001/graphql --output subgraph-orders.graphql

# Publish to the graph registry
rover subgraph publish my-graph@prod --name orders --schema subgraph-orders.graphql

# Compose a supergraph locally
rover supergraph compose --config supergraph.yaml --output supergraph.graphql

# Check before publish
rover subgraph check my-graph@prod --name orders --schema subgraph-orders.graphql
```

## supergraph.yaml example

```yaml
federation_version: 2
subgraphs:
  orders:
    routing_url: http://orders:4001/graphql
    schema:
      file: ./subgraph-orders.graphql
  users:
    routing_url: http://users:4002/graphql
    schema:
      file: ./subgraph-users.graphql
```

## Subgraph directive example

```graphql
type Order @key(fields: "id") {
  id: ID!
  total: Int!
  buyer: User
}

extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}
```

## Testing

```bash
# Run the router with a local supergraph
rover dev --supergraph-config supergraph.yaml
# query it: curl -X POST localhost:4000/graphql -d '{"query":"{ orders { id total } }"}'
```

## Best practices

- Run `rover subgraph check` in CI for every subgraph change.
- Publish schemas to the registry; never hand-compose in prod.
- Keep cross-subgraph references limited to @key entities.
- Version the supergraph with the router deployment.
- Test local composition with rover dev before publishing.

## Capabilities

### federation-tooling
Compose subgraph schemas into a supergraph and manage the router with rover.

**Commands:**
- `rover subgraph introspect http://orders:4001/graphql --output subgraph-orders.graphql`
- `rover subgraph publish my-graph@prod --name orders --schema subgraph-orders.graphql`
- `rover supergraph compose --config supergraph.yaml --output supergraph.graphql`
- `rover supergraph fetch my-graph@prod --output supergraph.graphql`
- `rover subgraph check my-graph@prod --name orders --schema subgraph-orders.graphql`

**Examples:**
- rover subgraph introspect http://orders:4001/graphql --output subgraph-orders.graphql
- rover supergraph compose --config supergraph.yaml --output supergraph.graphql
- rover subgraph check my-graph@prod --name orders --schema subgraph-orders.graphql
