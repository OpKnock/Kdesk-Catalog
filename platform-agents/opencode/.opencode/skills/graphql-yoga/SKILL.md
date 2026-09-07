---
name: "graphql-yoga"
description: "GraphQL server with GraphQL Yoga: scaffold a server, add plugins and subscriptions, and test with the interactive playground. Use when working with yoga server, api or when the user mentions yoga server, api."
---

GraphQL server with GraphQL Yoga: scaffold a server, add plugins and subscriptions, and test with the interactive playground.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm create @graphql-yoga/init`
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

# GraphQL Yoga

## What this skill does

GraphQL Yoga is a batteries-included GraphQL server built on envelop: works on any JS runtime, includes GraphiQL, file uploads, and subscriptions over SSE/WebSocket out of the box.

## When to use

- Standing up a GraphQL server with zero config
- Cross-runtime (Node, Bun, Deno, Workers) GraphQL
- Quick demos and internal tools

## Real commands

```bash
# Scaffold and run
npm create @graphql-yoga/init
npm run dev

# Add to an existing project
npm install graphql-yoga graphql

# Query
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}' | jq

# SSE subscription
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -H 'Accept: text/event-stream' -d '{"query":"subscription { countdown }"}' | head -5
```

## Server example

```typescript
import { createSchema, createYoga } from 'graphql-yoga'
import { createServer } from 'node:http'

const schema = createSchema({
  typeDefs: `
    type Query { hello: String }
    type Subscription { countdown(from: Int!): Int! }
  `,
  resolvers: {
    Query: { hello: () => 'world' },
    Subscription: {
      countdown: {
        subscribe: async function* (_, { from }) {
          for (let i = from; i >= 0; i--) { yield { countdown: i } }
        }
      }
    }
  }
})

const yoga = createYoga({ schema })
const server = createServer(yoga)
server.listen(4000)
```

## Testing

```bash
# GraphiQL is served at the endpoint in dev
curl -s http://localhost:4000/graphql | grep -q graphiql && echo 'GraphiQL available'
```

## Best practices

- Use async generators for subscriptions (simple, memory-safe).
- Add envelop plugins for auth, rate limiting, and tracing.
- Prefer SSE for serverless targets; WebSocket for stateful servers.
- Keep resolvers in separate modules as the schema grows.
- Test subscriptions with curl + Accept: text/event-stream.

## Capabilities

### yoga-server
Create Yoga servers, run them, add plugins, and test endpoints.

**Parameters:**
- `endpoint` (string): GraphQL endpoint path
- `port` (integer): Yoga listen port
- `plugin` (string): Yoga plugin like useGraphiQL

**Commands:**
- `npm create @graphql-yoga/init`
- `npm install graphql-yoga graphql`
- `npm run dev`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}' | jq`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -H 'Accept: text/event-stream' -d '{"query":"subscription { countdown }"}' | head -5`

**Examples:**
- npm create @graphql-yoga/init && npm run dev
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}' | jq
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -H 'Accept: text/event-stream' -d '{"query":"subscription { countdown }"}' | head -5

## References
- [GraphQL Yoga docs](https://the-guild.dev/graphql/yoga-server/docs)
- [Yoga features](https://the-guild.dev/graphql/yoga-server/docs/features)
