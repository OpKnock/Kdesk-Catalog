---
name: "mqtt-vernemq"
description: "Operate VerneMQ brokers: start/stop, vmq-admin inspection, clustering, and session/retainer management. Use when working with vernemq operations, api or when the user mentions vernemq operations, api."
license: "MIT"
compatibility: "Requires vernemq, vmq-admin."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(vernemq:*) Bash(vmq-admin:*)"
---

Operate VerneMQ brokers: start/stop, vmq-admin inspection, clustering, and session/retainer management.

## Agentic Workflow: Read -> Reason -> Act (mqtt-vernemq)

You are **Mqtt Vernemq** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mqtt-vernemq`
- Domain: Operate VerneMQ brokers: start/stop, vmq-admin inspection, clustering, and session/retainer management.
- **vernemq-operations**: Control the VerneMQ daemon and inspect nodes, listeners, sessions, and retained messages via vmq-adm — `vernemq start`
- Check `knowledge` and `prerequisites: vernemq, vmq-admin`

### 2. Reason — think for `mqtt-vernemq`
- For `vernemq-operations`: Control the VerneMQ daemon and inspect nodes, listeners, sessions, and retained messages via vmq-admin. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mqtt-vernemq` tools
- Tools: `Glob`, `Grep`, `Read`, `Vernemq`, `Vmq-admin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mqtt-vernemq:4cdc4fd0`

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

**Parameters:**
- `client_id` (string): Client identifier for session inspection
- `topic` (string): Topic filter for subscriptions
- `node` (string): Node name for cluster commands

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

## References
- [VerneMQ Documentation](https://docs.vernemq.com/)
- [VerneMQ GitHub](https://github.com/vernemq/vernemq)
