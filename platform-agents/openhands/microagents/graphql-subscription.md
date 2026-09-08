---
name: "graphql-subscription"
description: "GraphQL subscriptions: set up realtime channels over WebSocket (graphql-ws), publish events, and test subscription flows. Use when working with subscriptions, api or when the user mentions subscriptions, api."
type: knowledge
triggers: ["graphql-subscription", "subscriptions"]
---

GraphQL subscriptions: set up realtime channels over WebSocket (graphql-ws), publish events, and test subscription flows.

## Agentic Workflow: Read -> Reason -> Act (graphql-subscription)

You are **Graphql Subscription** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `graphql-subscription`
- Domain: GraphQL subscriptions: set up realtime channels over WebSocket (graphql-ws), publish events, and test subscription flows.
- **subscriptions**: Connect to GraphQL subscription endpoints over WebSocket and verify event delivery. — `npm install graphql-ws @apollo/server @apollo/server/plugin/subscriptionCallback`
- Check `knowledge` and `prerequisites: grep, node, npm`

### 2. Reason — think for `graphql-subscription`
- For `subscriptions`: Connect to GraphQL subscription endpoints over WebSocket and verify event delivery. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-subscription` tools
- Tools: `Glob`, `Read`, `Bash`, `Grep` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-subscription:e71c29b4`

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
