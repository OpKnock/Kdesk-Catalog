---
type: agent_requested
description: "Run and manage the Mosquitto MQTT broker: config, pub/sub clients, password files, and TLS listeners. Use when working with mosquitto operations, api or when the user mentions mosquitto operations, api."
---

Run and manage the Mosquitto MQTT broker: config, pub/sub clients, password files, and TLS listeners.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mosquitto -c /etc/mosquitto/mosquitto.conf`
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

# Mosquitto

Mosquitto is the reference open-source MQTT broker, ideal for small/medium deployments and local dev.

## What this skill does

- Starts and configures the mosquitto daemon
- Publishes/subscribes with the command-line clients
- Manages password files and TLS listeners

## When to use

- Local MQTT development and testing
- Small production deployments
- Teaching/verifying MQTT semantics

## Real commands

```bash
# Run broker with config
mosquitto -c /etc/mosquitto/mosquitto.conf

# Pub/sub basics
mosquitto_pub -h localhost -t sensors/temp -m "21.5"
mosquitto_sub -h localhost -t 'sensors/#' -v

# QoS 1 + retained
mosquitto_pub -h localhost -t test -m "keep" -r -q 1

# Password file
mosquitto_passwd -c /etc/mosquitto/passwd myuser

# TLS publish
mosquitto_pub -h broker.example.com -p 8883 --cafile ca.crt -t secure/topic -m hi
```

## Config essentials

```conf
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 8883
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

## Best practices

- Always disable `allow_anonymous` in production
- Use `$SYS/#` to verify broker health
- Test QoS 2 delivery with `mosquitto_sub -q 2`

## Capabilities

### mosquitto-operations
Run the mosquitto broker and use mosquitto_pub/mosquitto_sub clients with QoS, retained messages and TLS.

**Parameters:**
- `host` (string): Broker hostname or IP
- `port` (integer): Broker port (1883 plain, 8883 TLS)
- `topic` (string): Topic or topic filter with wildcards

**Commands:**
- `mosquitto -c /etc/mosquitto/mosquitto.conf`
- `mosquitto_pub -h localhost -t sensors/temp -m "21.5"`
- `mosquitto_sub -h localhost -t 'sensors/#' -v`
- `mosquitto_passwd -c /etc/mosquitto/passwd myuser`
- `mosquitto_pub -h localhost -t test -m "keep" -r -q 1`

**Examples:**
- mosquitto_sub -t '$SYS/#' -v
- mosquitto_pub -h broker.example.com -p 8883 --cafile ca.crt -t secure/topic -m hi
- mosquitto_sub -q 2 -t 'orders/+' -v

## References
- [Mosquitto Man Pages](https://mosquitto.org/man/)
- [mosquitto.conf man page](https://mosquitto.org/man/mosquitto-conf-5.html)