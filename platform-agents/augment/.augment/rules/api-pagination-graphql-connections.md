---
type: agent_requested
description: "Implements Relay-style cursor connections for GraphQL APIs: edges/nodes/pageInfo contracts, opaque cursors, schema linting, and schema diffing on changes. Use when working with graphql connections, schema introspection or when the user mentions graphql connections, schema introspection."
---

Implements Relay-style cursor connections for GraphQL APIs: edges/nodes/pageInfo contracts, opaque cursors, schema linting, and schema diffing on changes.

## Agentic Workflow: Read -> Reason -> Act (api-pagination-graphql-connections)

You are **Api Pagination Graphql Connections** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-pagination-graphql-connections`
- Domain: Implements Relay-style cursor connections for GraphQL APIs: edges/nodes/pageInfo contracts, opaque cursors, schema linting, and schema diffing on changes.
- **graphql-connections**: Build Relay connection types with cursor pagination — `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json`
- **schema-introspection**: Snapshot and verify the live GraphQL schema — `npx @graphql-inspector/cli coverage --schema schema.graphql --queries 'src/**/*.`
- Check `knowledge` and `prerequisites: node.js, python, postgresql`

### 2. Reason — think for `api-pagination-graphql-connections`
- For `graphql-connections`: Build Relay connection types with cursor pagination — decide which checks to run
- For `schema-introspection`: Snapshot and verify the live GraphQL schema — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-pagination-graphql-connections` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-pagination-graphql-connections:e3d8b05c`

# API Pagination v3 - GraphQL Connections

Relay cursor connections for GraphQL.

## What This Skill Does
- Exposes connections with edges/cursor/node/pageInfo
- Pages with opaque cursors via first/after and last/before
- Protects the schema with linting and diffing

## When to Use
- GraphQL APIs with Relay or Apollo clients
- Large lists that need stable cursor paging
- Adding pagination to existing list fields

## Real Commands

```bash
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ users(first: 10, after: \"Y3Vyc29yOjEw\") { edges { cursor node { id } } pageInfo { hasNextPage endCursor } } }"}'
npx graphql-schema-linter schema.graphql --rules=relay-connection-types
npx @graphql-inspector/cli diff schema-old.graphql schema-new.graphql
```

## Connection Type

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}
type UserEdge {
  cursor: String!
  node: User!
}
```

## Testing
- Assert hasNextPage flips correctly at the boundary
- Verify cursors survive reordering by the database
- Diff schemas in CI to block breaking changes

## Best Practices
- Enforce max first/before server-side
- Base cursors on stable sort keys, not offsets
- Preload edges in a single batched query

## Capabilities

### graphql-connections
Build Relay connection types with cursor pagination

**Parameters:**
- `first` (integer): Items to fetch forward from the cursor
- `after` (string): Opaque cursor to start from
- `maxPageSize` (integer): Server-enforced cap on first

**Commands:**
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ users(first: 10, after: \"Y3Vyc29yOjEw\") { edges { cursor node { id } } pageInfo { hasNextPage endCursor } } }"}' | jq '.data.users.pageInfo'`
- `npx graphql-schema-linter schema.graphql --rules=relay-connection-types`
- `npx @graphql-inspector/cli diff schema-old.graphql schema-new.graphql`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types | length'`

**Examples:**
- first/after arguments page through a connection
- graphql-schema-linter enforces Relay connection type rules
- graphql-inspector diff shows breaking schema changes

### schema-introspection
Snapshot and verify the live GraphQL schema

**Commands:**
- `npx @graphql-inspector/cli coverage --schema schema.graphql --queries 'src/**/*.graphql'`
- `npx @graphql-inspector/cli introspect http://localhost:4000/graphql schema.graphql`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types | length'`

**Examples:**
- coverage reports unused schema fields
- introspect snapshots the live schema
- __schema query lists registered types

## References
- [Relay Cursor Connections Spec](https://relay.dev/graphql/connections.htm)
- [GraphQL Inspector](https://the-guild.dev/graphql/inspector/docs)