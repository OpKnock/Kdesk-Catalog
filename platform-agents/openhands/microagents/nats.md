---
name: "nats"
description: "Publishes, subscribes, and performs request-reply over NATS subjects using the CLI. Supports wildcard patterns, queue groups enabling load balancing, and server info queries against a running instance."
type: knowledge
triggers: ["nats", "nats-core-messaging"]
---

# Nats

Publishes, subscribes, and performs request-reply over NATS subjects using the CLI. Supports wildcard patterns, queue groups enabling load balancing, and server info queries against a running instance.

## Instructions

# NATS

NATS is a lightweight, high-performance messaging system built around subjects and pub/sub.

## What this skill does

- Publishes and subscribes with subject wildcards
- Implements request-reply and queue groups
- Verifies server state and message flow

## When to use

- Service-to-service messaging without heavy brokers
- Fan-out events to many subscribers
- Simple RPC with request-reply

## Real commands

```bash
# Publish
nats pub orders.created '{"id":1}'
nats pub sensors.temp 21.5

# Subscribe with wildcards
nats sub 'orders.>' --all
nats sub 'orders.*' --raw

# Request-reply
nats req service.echo 'ping' --timeout 3s

# Queue group
nats subscribe 'tasks' --queue workers

# Server info
nats server info
```

## Subject rules

- `*` matches one token; `>` matches one or more at the end
- Publish permissions and queue groups are per-subject

## Patterns

- Fan-out: one publisher, many subscribers
- Load-balance: publisher + queue group of N workers
- RPC: request on subject, responders reply on inbox

## Best practices

- Design subject hierarchies before coding
- Use queue groups for competing consumers
- Set timeouts on all request-reply calls

## Capabilities

### nats-core-messaging
Publish, subscribe, request-reply and queue-group with the nats CLI against a running server.

**Commands:**
- `nats pub orders.created '{"id":1}'`
- `nats sub 'orders.>' --all`
- `nats req service.echo 'ping'`
- `nats subscribe 'tasks' --queue workers`
- `nats server info`

**Examples:**
- nats pub sensors.temp 21.5
- nats sub 'orders.*' --raw
- nats req service.echo 'hello' --timeout 3s
