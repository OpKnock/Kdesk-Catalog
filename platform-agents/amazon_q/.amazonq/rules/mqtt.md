Core MQTT protocol expertise: pub/sub semantics, QoS levels, retained messages, wildcards, and client tooling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mosquitto_pub -t sensors/temp -m "21.5"`
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