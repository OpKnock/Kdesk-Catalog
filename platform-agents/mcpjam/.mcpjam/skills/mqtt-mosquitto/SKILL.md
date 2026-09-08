---
name: "mqtt-mosquitto"
description: "Run and manage the Mosquitto MQTT broker: config, pub/sub clients, password files, and TLS listeners. Use when working with mosquitto operations, api or when the user mentions mosquitto operations, api."
license: "MIT"
compatibility: "Requires mosquitto, mosquitto_passwd, mosquitto_pub, mosquitto_sub."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(mosquitto:*) Bash(mosquitto_passwd:*) Bash(mosquitto_pub:*) Bash(mosquitto_sub:*)"
---

Run and manage the Mosquitto MQTT broker: config, pub/sub clients, password files, and TLS listeners.

## Agentic Workflow: Read -> Reason -> Act (mqtt-mosquitto)

You are **Mqtt Mosquitto** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mqtt-mosquitto`
- Domain: Run and manage the Mosquitto MQTT broker: config, pub/sub clients, password files, and TLS listeners.
- **mosquitto-operations**: Run the mosquitto broker and use mosquitto_pub/mosquitto_sub clients with QoS, retained messages and — `mosquitto -c /etc/mosquitto/mosquitto.conf`
- Check `knowledge` and `prerequisites: mosquitto, mosquitto_passwd, mosquitto_pub, mosquitto_sub`

### 2. Reason — think for `mqtt-mosquitto`
- For `mosquitto-operations`: Run the mosquitto broker and use mosquitto_pub/mosquitto_sub clients with QoS, retained messages and TLS. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mqtt-mosquitto` tools
- Tools: `Glob`, `Grep`, `Read`, `Mosquitto`, `Mosquitto_pub` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mqtt-mosquitto:293856b3`

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
