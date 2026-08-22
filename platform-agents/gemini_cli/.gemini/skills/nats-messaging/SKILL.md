---
name: "nats-messaging"
description: "Operates NATS and JetStream: pub/sub, request-reply, streams, consumers, and key-value stores."
---

# Nats

Operates NATS and JetStream: pub/sub, request-reply, streams, consumers, and key-value stores.

## Instructions

# NATS

Fast, lightweight messaging with pub/sub and JetStream persistence.

## When to Use

- Microservices request-reply
- Edge and IoT messaging
- Lightweight stream processing

## Pub/sub

```bash
nats sub 'orders.>'
nats pub orders.created '{"id":1}'
```

`>` matches one or more tokens; `*` matches exactly one.

## Request-reply

```bash
nats request service.orders '{"action":"status"}'
nats reply service.orders '{"status":"ok"}'
```

## JetStream streams

```bash
nats stream add ORDERS --subjects 'orders.>' --storage file --retention limits --max-age 168h
nats stream info ORDERS
```

## Consumers

```bash
nats consumer add ORDERS order-worker --pull --deliver last --ack-explicit --max-deliver 5
nats consumer info ORDERS order-worker
```

Pull consumers are the norm for worker pools.

## KV store

```bash
nats kv add config
nats kv put config feature_flag '{"on":true}'
nats kv get config feature_flag
```

## Best practices

- Choose retention: limits (size/age), interest, or workqueue.
- Set max-deliver so poison messages end in the DLQ stream.
- Use subject naming convention: `<app>.<entity>.<action>`.
- Monitor stream lag: `nats stream report`.

## Testing

```bash
nats pub orders.created '{"id":1}' --count 1000
nats stream report ORDERS
```

Verify all 1000 land in the stream with zero loss.

## Capabilities

### pub-sub
Publish and subscribe to NATS subjects.

**Commands:**
- `nats sub 'orders.>'`
- `nats pub orders.created '{"id":1}'`
- `nats request service.orders '{"action":"status"}'`
- `nats pub --reply order.ack orders.created '{"id":1}'`
- `nats reply service.orders 'ack received'`

**Examples:**
- nats sub 'metrics.>' --raw
- nats request service.health '{}' --timeout 2s
- nats pub orders.created '{"id":2}' --count 100 --sleep 0.1s

### jetstream
Manage JetStream streams, consumers, and KV.

**Commands:**
- `nats stream add ORDERS --subjects 'orders.>' --storage file --retention limits --max-age 168h --max-size 10GB`
- `nats stream info ORDERS`
- `nats consumer add ORDERS order-worker --pull --deliver last --ack-explicit --max-deliver 5`
- `nats stream report ORDERS`
- `nats kv add config --history 10`

**Examples:**
- nats stream add ORDERS --subjects 'orders.>' --replicas 3
- nats consumer info ORDERS order-worker
- nats kv put config feature_flag '{"on":true}' && nats kv get config feature_flag
