---
name: "graphql-server"
description: "Designs and runs GraphQL servers with Apollo Server, GraphQL Yoga, and gqlgen including resolvers, schema stitching, and query cost limiting."
type: knowledge
triggers: ["graphql-server", "graphql-servers", "graphql-querying"]
---

# Graphql Server

Designs and runs GraphQL servers with Apollo Server, GraphQL Yoga, and gqlgen including resolvers, schema stitching, and query cost limiting.

## Instructions

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

**Commands:**
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d "{\"query\":\"{ __schema { queryType { name } } }\"}"`
- `curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d "{\"query\":\"{ users { id name } }\"}"`
- `npx graphql-codegen`
- `npx apollo schema:check`

**Examples:**
- curl -s -X POST localhost:4000/graphql -d "{\"query\":\"{ __typename }\"}"
- npx graphql-codegen --config codegen.yml
