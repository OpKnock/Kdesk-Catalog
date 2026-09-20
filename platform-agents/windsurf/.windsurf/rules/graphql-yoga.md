---
trigger: glob
description: "GraphQL server with GraphQL Yoga: scaffold a server, add plugins and subscriptions, and test with the interactive playground. Use when working with yoga server, api or when the user mentions yoga server, api."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
---

GraphQL server with GraphQL Yoga: scaffold a server, add plugins and subscriptions, and test with the interactive playground.

## Agentic Workflow: Read -> Reason -> Act (graphql-yoga)

You are **Graphql Yoga** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `graphql-yoga`
- Domain: GraphQL server with GraphQL Yoga: scaffold a server, add plugins and subscriptions, and test with the interactive playground.
- **yoga-server**: Create Yoga servers, run them, add plugins, and test endpoints. — `npm create @graphql-yoga/init`
- Check `knowledge` and `prerequisites: npm`

### 2. Reason — think for `graphql-yoga`
- For `yoga-server`: Create Yoga servers, run them, add plugins, and test endpoints. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-yoga` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-yoga:735ff0e8`

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
