---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.{js,ts,jsx,tsx} **/*.{ts,tsx}"
---

Apollo GraphQL ecosystem: set up Apollo Server and Client, run codegen, and manage the schema registry with the Apollo CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @apollo/server graphql`
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

**Parameters:**
- `endpoint` (string): GraphQL endpoint URL
- `target-language` (string): codegen target: typescript, swift, etc
- `output-dir` (string): Codegen output directory

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

## References
- [Apollo Server docs](https://www.apollographql.com/docs/apollo-server/)
- [Apollo Client docs](https://www.apollographql.com/docs/react/)
