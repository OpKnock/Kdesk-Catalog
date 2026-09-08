---
name: "pulsar-subscriptions"
description: "Pulsar subscription types and management: Exclusive, Shared, Failover, Key_Shared plus cursor operations. Use when working with pulsar subscription mgmt, api or when the user mentions pulsar subscription mgmt, api."
type: knowledge
triggers: ["pulsar-subscriptions", "pulsar-subscription-mgmt"]
---

Pulsar subscription types and management: Exclusive, Shared, Failover, Key_Shared plus cursor operations.

## Agentic Workflow: Read -> Reason -> Act (pulsar-subscriptions)

You are **Pulsar Subscriptions** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-subscriptions`
- Domain: Pulsar subscription types and management: Exclusive, Shared, Failover, Key_Shared plus cursor operations.
- **pulsar-subscription-mgmt**: Create consumers with subscription types, list/peek/unsubscribe subscriptions, and manage cursors. — `bin/pulsar-admin topics subscriptions list my-topic`
- Check `knowledge` and `prerequisites: bin/pulsar-admin, bin/pulsar-client`

### 2. Reason — think for `pulsar-subscriptions`
- For `pulsar-subscription-mgmt`: Create consumers with subscription types, list/peek/unsubscribe subscriptions, and manage cursors. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-subscriptions` tools
- Tools: `Glob`, `Grep`, `Read`, `Bin/pulsar-admin`, `Bin/pulsar-client` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-subscriptions:a4d3305f`

# Pulsar Subscriptions

Subscriptions are named cursors on a topic; the type determines message distribution.

## What this skill does

- Explains and creates each subscription type
- Manages subscription cursors
- Peeks and clears messages

## When to use

- Choosing the right consumption model
- Debugging consumption lag

## Real commands

```bash
# Create consumers per type
bin/pulsar-client consume my-topic -s sub-a --subscription-type Exclusive --num-messages 5
bin/pulsar-client consume my-topic -s sub-s --subscription-type Shared --num-messages 5
bin/pulsar-client consume my-topic -s sub-k --subscription-type Key_Shared --num-messages 5

# List subscriptions
bin/pulsar-admin topics subscriptions list my-topic

# Peek messages without consuming
bin/pulsar-admin topics peek-messages --subscription my-sub --count 5 my-topic

# Skip / unsubscribe
bin/pulsar-admin topics subscriptions update my-topic -s my-sub -m 100
bin/pulsar-admin topics unsubscribe my-topic -s my-sub
```

## Type cheat sheet

- Exclusive: one consumer; others error
- Shared: round-robin across consumers
- Failover: one active, others standby in order
- Key_Shared: messages with same key go to the same consumer

## Best practices

- Shared for parallel workers; Failover for ordered failover
- Key_Shared for per-entity ordering (e.g. per order_id)
- Monitor backlog per subscription

## Capabilities

### pulsar-subscription-mgmt
Create consumers with subscription types, list/peek/unsubscribe subscriptions, and manage cursors.

**Parameters:**
- `topic` (string): Topic name
- `subscription` (string): Subscription name
- `sub_type` (string): Exclusive, Shared, Failover or Key_Shared

**Commands:**
- `bin/pulsar-admin topics subscriptions list my-topic`
- `bin/pulsar-admin topics peek-messages --subscription my-sub --count 5 my-topic`
- `bin/pulsar-admin topics unsubscribe my-topic -s my-sub`
- `bin/pulsar-client consume my-topic -s my-sub --subscription-type Shared --num-messages 5`
- `bin/pulsar-admin topics subscriptions update my-topic -s my-sub -m 100`

**Examples:**
- bin/pulsar-client consume my-topic -s sub-a --subscription-type Exclusive --num-messages 3
- bin/pulsar-admin topics peek-messages --subscription sub-a --count 2 my-topic
- bin/pulsar-client consume my-topic -s sub-k --subscription-type Key_Shared --num-messages 4

## References
- [Pulsar Subscription Types](https://pulsar.apache.org/docs/3.0.x/concepts-messaging/#subscription-types)
- [pulsar-admin topics](https://pulsar.apache.org/docs/3.0.x/reference-pulsar-admin-topics/)
