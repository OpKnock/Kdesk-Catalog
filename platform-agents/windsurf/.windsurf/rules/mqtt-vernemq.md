---
trigger: glob
description: "Operate VerneMQ brokers: start/stop, vmq-admin inspection, clustering, and session/retainer management. Use when working with vernemq operations, api or when the user mentions vernemq operations, api."
globs: ["**/*.r", "**/*.sh"]
---

Operate VerneMQ brokers: start/stop, vmq-admin inspection, clustering, and session/retainer management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `vernemq start`
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
