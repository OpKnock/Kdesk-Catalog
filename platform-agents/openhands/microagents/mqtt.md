---
name: "mqtt"
description: "Core MQTT protocol expertise: pub/sub semantics, QoS levels, retained messages, wildcards, and client tooling. Use when working with mqtt protocol, api or when the user mentions mqtt protocol, api."
type: knowledge
triggers: ["mqtt", "mqtt-protocol"]
---

Core MQTT protocol expertise: pub/sub semantics, QoS levels, retained messages, wildcards, and client tooling.

## Agentic Workflow: Read -> Reason -> Act (mqtt)

You are **Mqtt** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mqtt`
- Domain: Core MQTT protocol expertise: pub/sub semantics, QoS levels, retained messages, wildcards, and client tooling.
- **mqtt-protocol**: Work with MQTT fundamentals using mosquitto clients: QoS, retained messages, wildcard subscriptions  — `mosquitto_pub -t sensors/temp -m "21.5"`
- Check `knowledge` and `prerequisites: mosquitto_pub, mosquitto_sub`

### 2. Reason — think for `mqtt`
- For `mqtt-protocol`: Work with MQTT fundamentals using mosquitto clients: QoS, retained messages, wildcard subscriptions and will messages. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mqtt` tools
- Tools: `Glob`, `Grep`, `Read`, `Mosquitto_pub`, `Mosquitto_sub` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mqtt:8689fb8a`

# MQTT

MQTT is a lightweight pub/sub messaging protocol for constrained networks and IoT.

## What this skill does

- Explains and exercises core protocol features
- Publishes and subscribes with the reference clients
- Demonstrates QoS, retained, wildcards and will messages

## When to use

- Designing topic hierarchies for a system
- Choosing QoS for delivery guarantees
- Debugging message flows on a broker

## Real commands

```bash
# Basic pub/sub
mosquitto_pub -t sensors/temp -m "21.5"
mosquitto_sub -t 'sensors/#' -v

# QoS 2 with retain
mosquitto_pub -t alarms/device1 -m "on" -q 2 -r

# Single-level wildcard +
mosquitto_sub -t 'orders/+/status' -v

# Retained status and will message
mosquitto_pub -t status -m online -r
mosquitto_pub -t gate/lastwill -m "x" --will-topic gate/status --will-payload "dead"

# Everything
mosquitto_sub -t '#' -v
```

## Topic design

- Hierarchy: `domain/device/sensor` (e.g. `factory/line1/robot3/temp`)
- `#` multi-level wildcard, `+` single level
- `$SYS` topics are broker-internal

## QoS cheat sheet

- 0: at most once (fire and forget)
- 1: at least once (duplicates possible)
- 2: exactly once (2-way handshake)

## Best practices

- Design topics before writing clients
- Use retain only for state that must survive restarts
- Prefer QoS 1 unless exactly-once is contractually required

## Capabilities

### mqtt-protocol
Work with MQTT fundamentals using mosquitto clients: QoS, retained messages, wildcard subscriptions and will messages.

**Parameters:**
- `topic` (string): Topic with optional + or # wildcards
- `qos` (integer): QoS level 0, 1, or 2
- `retain` (boolean): Keep the last message on the topic for new subscribers

**Commands:**
- `mosquitto_pub -t sensors/temp -m "21.5"`
- `mosquitto_sub -t 'sensors/#' -v`
- `mosquitto_pub -t alarms/device1 -m "on" -q 2 -r`
- `mosquitto_sub -t 'orders/+/status' -v`
- `mosquitto_pub -t gate/lastwill -m "offline" --will-topic gate/status --will-payload "dead"`

**Examples:**
- mosquitto_pub -t 'sensors/+/temp' -m 21.5 -q 1
- mosquitto_sub -t '#' -v
- mosquitto_pub -t status -m online -r

## References
- [MQTT.org](https://mqtt.org/)
- [MQTT Essentials](https://www.hivemq.com/blog/mqtt-essentials-part-1-introducing-mqtt/)
