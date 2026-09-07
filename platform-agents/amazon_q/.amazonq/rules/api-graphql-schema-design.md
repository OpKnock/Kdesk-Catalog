Designs advanced GraphQL schemas — interfaces, unions, custom scalars — and federated graphs with Apollo Federation subgraphs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx graphql-codegen init`, `rover subgraph publish my-graph@prod --name inventory --sche`
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

# API GraphQL (Schema Design & Federation)

Designs advanced GraphQL schemas and composes them into federated graphs.

## When to Use
- Enterprise GraphQL with multiple teams
- Schema-first design with governance
- Composing subgraphs into a supergraph
- Adding real-time via subscriptions

## Real Commands

```bash
# Generate types from schema
npx graphql-codegen init
npx graphql-codegen --config codegen.yml

# Export schema (Python/Strawberry)
strawberry export-schema -o schema.graphql

# Introspect a running server
rover graph introspect http://localhost:4001/graphql > local.graphql

# Compose supergraph
rover supergraph compose --config supergraph.yaml --output supergraph.graphql
```

## Supergraph Config

```yaml
# supergraph.yaml
subgraphs:
  inventory:
    routing_url: http://inventory:4001/graphql
    schema:
      file: ./inventory.graphql
  products:
    routing_url: http://products:4002/graphql
    schema:
      file: ./products.graphql
```

## Testing
Use `rover subgraph check` against the prod schema before publishing to catch breaking subgraph changes.

## Best Practices
- Keep subgraph boundaries at team ownership lines
- Run `rover subgraph check` on every subgraph PR
- Version and back up the composed supergraph

## Capabilities

### schema-design
Model enterprise GraphQL schemas with shared type patterns and schema-first authoring

**Parameters:**
- `schema` (string): Path to GraphQL SDL schema file
- `config` (string): graphql-codegen config path

**Commands:**
- `npx graphql-codegen init`
- `npx graphql-codegen --config codegen.yml`
- `strawberry export-schema -o schema.graphql`
- `npm run graphql:schema:print > schema.graphql`
- `npx graphql-inspector validate schema.graphql`

**Examples:**
- npx graphql-codegen --config codegen.yml && git diff --stat
- strawberry export-schema -o schema.graphql && graphql-inspector validate schema.graphql
- npx graphql-inspector validate documents/**/*.graphql schema.graphql

### federation
Compose subgraphs into a supergraph with Apollo Federation and Rover

**Parameters:**
- `graphRef` (string): Apollo graph ref like my-graph@prod
- `subgraph` (string): Subgraph name

**Commands:**
- `rover subgraph publish my-graph@prod --name inventory --schema ./inventory.graphql --routing-url http://inventory:4001`
- `rover supergraph compose --config supergraph.yaml --output supergraph.graphql`
- `rover dev --supergraph-config supergraph.yaml`
- `rover graph introspect http://localhost:4001/graphql > local.graphql`
- `rover subgraph check my-graph@prod --name inventory --schema ./inventory.graphql`

**Examples:**
- rover supergraph compose --config supergraph.yaml --output supergraph.graphql
- rover subgraph check my-graph@prod --name products --schema ./products.graphql
- rover dev --supergraph-config supergraph.yaml --watch

## References
- [Apollo Federation Docs](https://www.apollographql.com/docs/federation/)
- [Rover CLI](https://www.apollographql.com/docs/rover/)
- [GraphQL Code Generator](https://the-guild.dev/graphql/codegen/docs)