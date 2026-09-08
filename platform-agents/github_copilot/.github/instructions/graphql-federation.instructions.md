---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Apollo Federation: build supergraph schemas from subgraph services, compose with rover, and operate the gateway/router.

## Agentic Workflow: Read -> Reason -> Act (graphql-federation)

You are **Graphql Federation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `graphql-federation`
- Domain: Apollo Federation: build supergraph schemas from subgraph services, compose with rover, and operate the gateway/router.
- **federation-tooling**: Compose subgraph schemas into a supergraph and manage the router with rover. — `rover subgraph introspect http://orders:4001/graphql --output subgraph-orders.gr`
- Check `knowledge` and `prerequisites: rover`

### 2. Reason — think for `graphql-federation`
- For `federation-tooling`: Compose subgraph schemas into a supergraph and manage the router with rover. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-federation` tools
- Tools: `Glob`, `Grep`, `Read`, `Rover` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-federation:59fc78cc`

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

**Parameters:**
- `subgraph-name` (string): Name of the subgraph service
- `graph-ref` (string): Graph ref like my-graph@prod
- `compose-config` (string): supergraph.yaml path

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

## References
- [Apollo Federation docs](https://www.apollographql.com/docs/federation/)
- [rover CLI docs](https://www.apollographql.com/docs/rover/)
