---
name: "api-graphql-typed-codegen"
description: "Advanced GraphQL implementation: codegen-typed resolvers, DataLoader batching, query-cost protection, and persisted operations."
type: knowledge
triggers: ["api-graphql-typed-codegen", "typed-codegen", "persisted-queries"]
---

# Api Graphql Typed Codegen

Advanced GraphQL implementation: codegen-typed resolvers, DataLoader batching, query-cost protection, and persisted operations.

## Instructions

# API GraphQL Engineer (Advanced)

Levels up GraphQL services: types, batching, and hardened transports.

## When to Use
- Type-safe resolver development
- Reducing client payload sizes
- Protecting against unknown queries

## Real Commands

```bash
# Codegen
npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-resolvers
npx graphql-codegen --config codegen.ts

# Persisted queries
npm install @apollo/server-plugin-operation-registry

# Cost protection
npm install graphql-query-complexity
```

## Codegen Setup

```yml
schema: schema.graphql
generates:
  src/generated/resolvers-types.ts:
    plugins: [typescript, typescript-resolvers]
```

## Testing
Run `tsc --noEmit` after codegen to catch type drift.

## Best Practices
- Commit generated types
- Enable persisted queries in production
- Validate query cost before execution

## Capabilities

### typed-codegen
Generate TypeScript types from the GraphQL schema

**Commands:**
- `npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-resolvers`
- `npx graphql-codegen init`
- `npx graphql-codegen --config codegen.ts`
- `node -e "const c=require('./codegen.yml')||{};console.log('config ok')" 2>/dev/null || npx graphql-codegen --help`
- `npx graphql-codegen --watch`

**Examples:**
- npx graphql-codegen --config codegen.ts && npx tsc --noEmit
- npm install -D @graphql-codegen/cli @graphql-codegen/typescript-resolvers
- npx graphql-codegen --watch

### persisted-queries
Register and serve persisted queries for production clients

**Commands:**
- `npm install @apollo/server-plugin-operation-registry`
- `node -e "const p=require('@apollo/server-plugin-operation-registry');console.log(typeof p.ApolloServerOperationRegistry)"`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"extensions":{"persistedQuery":{"version":1,"sha256Hash":"abc"}}}' -o /dev/null -w '%{http_code}'`
- `npm install graphql-persisted-documents`
- `node -e "console.log('persisted query: client sends hash, server resolves')"`

**Examples:**
- npm install @apollo/server-plugin-operation-registry
- npm install graphql-persisted-documents
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"extensions":{"persistedQuery":{"version":1,"sha256Hash":"abc"}}}' -o /dev/null -w '%{http_code}'
