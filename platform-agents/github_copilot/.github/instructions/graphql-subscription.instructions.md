---
applyTo: "**/*.java **/*.json **/*.r **/*.scala **/*.sh **/*.{js,ts,jsx,tsx}"
---

# Graphql Subscription

GraphQL subscriptions: set up realtime channels over WebSocket (graphql-ws), publish events, and test subscription flows.

## Instructions

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
