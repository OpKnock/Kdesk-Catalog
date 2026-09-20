---
applyTo: "**/*.go **/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# api-graphql-architect

Architects enterprise GraphQL: federated graphs, schema registry governance, and supergraph operations with Rover and GraphOS.

## Instructions

# API GraphQL Architect

Designs and operates enterprise GraphQL platforms.

## When to Use
- Multiple teams share one graph
- Schema changes must be safe
- Standardizing subgraph patterns

## Real Commands

```bash
# Introspect a subgraph
rover graph introspect http://localhost:4001/graphql > products.graphql

# Publish
rover subgraph publish mygraph@prod --name products --schema ./products.graphql --routing-url http://products:4001

# Check for breaking changes
rover subgraph check mygraph@prod --name products --schema ./products.graphql

# Compose supergraph
rover supergraph compose --config supergraph.yaml --output supergraph.graphql

# Diff schemas locally
npx graphql-inspector diff old.graphql new.graphql
```

## Federation Principles
- One subgraph per team boundary
- Entities with @key for shared types
- Checks run on every subgraph PR

## Testing
Compose the supergraph locally and smoke-test queries across subgraphs.

## Best Practices
- Never publish unchecked subgraphs
- Keep supergraph artifacts in version control

## Capabilities

### supergraph-ops
Compose, publish, and check supergraphs with Rover

**Commands:**
- `rover supergraph compose --config supergraph.yaml --output supergraph.graphql`
- `rover subgraph publish mygraph@prod --name products --schema ./products.graphql --routing-url http://products:4001`
- `rover subgraph check mygraph@prod --name products --schema ./products.graphql`
- `rover graph introspect http://localhost:4001/graphql > products.graphql`
- `rover supergraph fetch mygraph@prod --output current.graphql`

**Examples:**
- rover supergraph compose --config supergraph.yaml --output supergraph.graphql
- rover subgraph check mygraph@prod --name products --schema ./products.graphql
- rover supergraph fetch mygraph@prod --output current.graphql

### schema-governance
Guard the schema against breaking changes with checks and linting

**Commands:**
- `rover subgraph check mygraph@prod --name products --schema ./products.graphql --compare prod`
- `npx graphql-inspector diff old.graphql new.graphql`
- `graphql-inspector validate documents/**/*.graphql schema.graphql`
- `npx @graphql-inspector/cli coverage schema.graphql docs/**/*.graphql`
- `graphql-inspector simulate-client requests.json schema.graphql`

**Examples:**
- npx graphql-inspector diff old.graphql new.graphql
- rover subgraph check mygraph@prod --name products --schema ./products.graphql
- graphql-inspector validate docs/**/*.graphql schema.graphql
