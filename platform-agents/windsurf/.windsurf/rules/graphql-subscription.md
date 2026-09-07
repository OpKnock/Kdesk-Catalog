---
trigger: glob
description: "GraphQL subscriptions: set up realtime channels over WebSocket (graphql-ws), publish events, and test subscription flows. Use when working with subscriptions, api or when the user mentions subscriptions, api."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.scala", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
---

GraphQL subscriptions: set up realtime channels over WebSocket (graphql-ws), publish events, and test subscription flows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install graphql-ws @apollo/server @apollo/server/plugin/`
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

# GraphQL Subscriptions

## What this skill does

Subscriptions push realtime updates over WebSocket using the graphql-ws protocol. Servers publish via PubSub; clients subscribe with a subscription document and receive events as they happen.

## When to use

- Live order boards, chat, and presence
- Push notifications from mutations
- Replacing polling with event-driven updates

## Real commands

```bash
# What subscriptions does the schema offer?
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __type(name: \"Subscription\") { fields { name } } }"}' | jq '.data.__type.fields[].name'

# Subscribe via graphql-ws from Node
node -e "const {createClient}=require('graphql-ws');const c=createClient({url:'ws://localhost:4000/graphql'});c.subscribe({query:'subscription { orderUpdated { id status } }'},{next:d=>console.log(d.data),error:e=>console.error(e)});setTimeout(()=>c.dispose(),15000)"

# Find the pubsub wiring
 grep -rn 'pubsub\|PubSub' src/ | head -10
```

## Server example (Apollo)

```javascript
const { PubSub } = require('graphql-subscriptions')
const pubsub = new PubSub()

const typeDefs = `
  type Subscription { orderUpdated: Order }
  type Mutation { placeOrder: Order }
`

// in the mutation resolver:
await pubsub.publish('ORDER_UPDATED', { orderUpdated: order })

// in the subscription resolver:
Subscription: { orderUpdated: { subscribe: () => pubsub.asyncIterator('ORDER_UPDATED') } }
```

## Testing

```bash
# Terminal A: subscribe; Terminal B: mutate; watch the push
node -e "const {createClient}=require('graphql-ws');const c=createClient({url:'ws://localhost:4000/graphql'});c.subscribe({query:'subscription { orderUpdated { id } }'},{next:d=>console.log('pushed',d.data)});setTimeout(()=>c.dispose(),30000)"
# terminal B:
curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"mutation{ placeOrder { orderId } }"}' | jq
```

## Best practices

- Filter subscription events by context (user/tenant) inside resolvers.
- Always dispose clients on disconnect to free the socket.
- Prefer small payloads over the wire; fetch details via query.
- Add heartbeat/keepalive handling to clients.
- Use a scalable pubsub (Redis) when scaling horizontally.

## Capabilities

### subscriptions
Connect to GraphQL subscription endpoints over WebSocket and verify event delivery.

**Parameters:**
- `subscription-query` (string): Subscription document
- `ws-url` (string): WebSocket endpoint URL
- `event-topic` (string): PubSub topic emitting the event

**Commands:**
- `npm install graphql-ws @apollo/server @apollo/server/plugin/subscriptionCallback`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __type(name: \"Subscription\") { fields { name } } }"}' | jq '.data.__type.fields[].name'`
- `node -e "const {createClient}=require('graphql-ws');const c=createClient({url:'ws://localhost:4000/graphql'});c.subscribe({query:'subscription { orderUpdated { id status } }'},{next:d=>console.log(d.data),error:e=>console.error(e)});setTimeout(()=>c.dispose(),15000)"`
- `grep -rn 'pubsub\|PubSub' src/ | head -10`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"mutation{ placeOrder { orderId } }"}' | jq`

**Examples:**
- node -e "const {createClient}=require('graphql-ws');const c=createClient({url:'ws://localhost:4000/graphql'});c.subscribe({query:'subscription { orderUpdated { id status } }'},{next:d=>console.log(d.data),error:e=>console.error(e)});setTimeout(()=>c.dispose(),15000)"
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __type(name: \"Subscription\") { fields { name } } }"}' | jq '.data.__type.fields[].name'
- grep -rn 'pubsub\|PubSub' src/ | head -10

## References
- [graphql-ws docs](https://the-guild.dev/graphql/ws)
- [Apollo subscriptions](https://www.apollographql.com/docs/apollo-server/data/subscriptions/)
