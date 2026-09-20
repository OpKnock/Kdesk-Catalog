---
name: "graphql-server"
description: "Designs and runs GraphQL servers with Apollo Server, GraphQL Yoga, and gqlgen including resolvers, schema stitching, and query cost limiting. Use when working with graphql servers, graphql querying, backend or when the user mentions graphql servers, graphql querying, backend."
license: "MIT"
compatibility: "Requires node, npm, npx. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(go:*) Bash(node:*) Bash(npm:*) Bash(npx:*)"
---

Designs and runs GraphQL servers with Apollo Server, GraphQL Yoga, and gqlgen including resolvers, schema stitching, and query cost limiting.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @apollo/server graphql`, `curl -X POST http://localhost:4000/graphql -H "Content-Type:`
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

# GraphQL Server

Design and operate GraphQL APIs.

## When to Use

- Clients need to fetch nested data in one round trip
- Many consumers with divergent data needs
- Schema-first development where the contract is the source of truth
- Aggregating multiple services behind one API layer

## Core Concepts

- Schema: type definitions that define the API contract
- Resolvers: functions that fetch each field
- Query vs Mutation: reads vs writes
- Federation/stitching: combining multiple schemas
- Query complexity: cost of a query to prevent abuse

## Commands

```bash
# Apollo Server (Node)
npm install @apollo/server graphql
node server.js

# GraphQL Yoga
npm install graphql-yoga

# gqlgen (Go)
go run github.com/99designs/gqlgen/cmd/gqlgen@latest init

# Introspect the schema
curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { name } } }"}'

# Run a query
curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" \
  -d '{"query":"{ users { id name } }"}'
```

## Schema Example

```graphql
type Query {
  user(id: ID!): User
}

type User {
  id: ID!
  name: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
}
```

## Best Practices

- Always define a __typename-friendly schema with unique type names
- Cap query depth and complexity to avoid nested-DoS attacks
- Batch data fetches with DataLoader to avoid N+1 resolvers
- Use persisted queries for stable, cacheable clients
- Run schema checks (apollo schema:check) in CI before releasing

## Capabilities

### graphql-servers
Scaffold and run popular GraphQL server frameworks.

**Parameters:**
- `port` (integer): Server listen port
- `framework` (string): apollo, yoga, or gqlgen

**Commands:**
- `npm install @apollo/server graphql`
- `npx apollo init`
- `node index.js`
- `npm install graphql-yoga`
- `go run github.com/99designs/gqlgen/cmd/gqlgen@latest init`

**Examples:**
- npx @graphql-codegen/cli init
- npx gqlgen init
- npm start

### graphql-querying
Run introspection and test queries against a server.

**Parameters:**
- `query` (string): GraphQL query string
- `endpoint` (string): GraphQL endpoint URL

**Commands:**
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d "{\"query\":\"{ __schema { queryType { name } } }\"}"`
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d "{\"query\":\"{ users { id name } }\"}"`
- `npx graphql-codegen`
- `npx apollo schema:check`

**Examples:**
- curl -s -X POST localhost:4000/graphql -d "{\"query\":\"{ __typename }\"}"
- npx graphql-codegen --config codegen.yml

## References
- [GraphQL Spec](https://spec.graphql.org)
- [Apollo Server Docs](https://www.apollographql.com/docs/apollo-server/)
- [gqlgen Docs](https://gqlgen.com)
