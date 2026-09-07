---
name: "graphql-federation"
description: "Apollo Federation: build supergraph schemas from subgraph services, compose with rover, and operate the gateway/router. Use when working with federation tooling, api or when the user mentions federation tooling, api."
---

Apollo Federation: build supergraph schemas from subgraph services, compose with rover, and operate the gateway/router.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rover subgraph introspect http://orders:4001/graphql --outpu`
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
