# Graphql Yoga

GraphQL server with GraphQL Yoga: scaffold a server, add plugins and subscriptions, and test with the interactive playground.

## Instructions

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