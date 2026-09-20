---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.{js,ts,jsx,tsx} **/*.{ts,tsx}"
---

# Graphql Apollo

Apollo GraphQL ecosystem: set up Apollo Server and Client, run codegen, and manage the schema registry with the Apollo CLI.

## Instructions

# GraphQL Apollo

## What this skill does

The Apollo ecosystem covers server (Apollo Server), client (Apollo Client), and tooling (codegen, schema registry). This skill covers setup, introspection, and typed codegen.

## When to use

- Standing up a GraphQL server with a polished toolkit
- Generating typed clients from the schema
- Introspecting a running endpoint

## Real commands

```bash
# Server scaffold
npm install @apollo/server graphql
npx apollo server:init

# Introspect a running endpoint
curl -s -X POST http://localhost:4000/ -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types[0].name'

# Typed codegen for the client
npx apollo codegen:generate --target=typescript --outputFlat src/__generated__
```

## Server example

```javascript
const { ApolloServer } = require('@apollo/server')
const { startStandaloneServer } = require('@apollo/server/standalone')

const server = new ApolloServer({
  typeDefs: `type Query { hello: String }`,
  resolvers: { Query: { hello: () => 'world' } }
})

startStandaloneServer(server, { listen: { port: 4000 } })
```

## Testing

```bash
# Smoke the server before wiring the client
curl -s -X POST http://localhost:4000/ -H 'Content-Type: application/json' -d '{"query":"{ hello }"}' | jq
```

## Best practices

- Keep resolvers thin; delegate to services.
- Use context for auth and data source injection.
- Run codegen against the schema artifact, not a live server, in CI.
- Enable persisted queries for production caching.
- Version the schema via the registry before rolling client changes.

## Capabilities

### apollo-tooling
Scaffold Apollo Server, introspect schemas, and run codegen.

**Commands:**
- `npm install @apollo/server graphql`
- `npx apollo server:init`
- `curl -s -X POST http://localhost:4000/ -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types[0].name'`
- `npx apollo codegen:generate --target=typescript --outputFlat src/__generated__`
- `node -e "const {ApolloServer}=require('@apollo/server');const s=new ApolloServer({typeDefs:'type Query{hello:String}',resolvers:{Query:{hello:()=>'hi'}}});console.log(s)"`

**Examples:**
- curl -s -X POST http://localhost:4000/ -H 'Content-Type: application/json' -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types[0].name'
- npx apollo codegen:generate --target=typescript --outputFlat src/__generated__
- npm install @apollo/server graphql && node index.js
