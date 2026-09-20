---
applyTo: "**/*.r **/*.sh"
---

# Mqtt Vernemq

Operate VerneMQ brokers: start/stop, vmq-admin inspection, clustering, and session/retainer management.

## Instructions

# VerneMQ

VerneMQ is a high-performance MQTT broker written in Erlang, built for clustering and scale.

## What this skill does

- Starts/stops the broker and runs the interactive console
- Inspects listeners, sessions, subscriptions and retained messages
- Manages clusters with vmq-admin

## When to use

- High-throughput MQTT workloads
- Multi-node MQTT clusters
- Brokers that must handle millions of retained messages

## Real commands

```bash
# Daemon lifecycle
vernemq start
vernemq stop
vernemq console   # foreground Erlang console

# Status and listeners
vmq-admin status
vmq-admin listener show

# Sessions and subscriptions
vmq-admin session show --client-id test-client
vmq-admin topic subscription add --client-id cli --topic sensors/#

# Retained messages
vmq-admin retainer show

# Cluster
vmq-admin cluster show
```

## Configuration

- `/etc/vernemq/vernemq.conf` - listeners, allow_anonymous, plugins
- Listener ports: 1883 plain, 8883 TLS, 8080 websockets

## Best practices

- Check `vmq-admin status` before and after restarts
- Monitor session counts for leaked persistent sessions
- Configure `allow_anonymous=off` for production

## Capabilities

### vernemq-operations
Control the VerneMQ daemon and inspect nodes, listeners, sessions, and retained messages via vmq-admin.

**Commands:**
- `vernemq start`
- `vernemq console`
- `vmq-admin status`
- `vmq-admin listener show`
- `vmq-admin session show --client-id test-client`

**Examples:**
- vmq-admin cluster show
- vmq-admin topic subscription add --client-id cli --topic sensors/#
- vmq-admin retainer show
