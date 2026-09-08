---
name: "iot-backend"
description: "Builds IoT backends: MQTT brokers with mosquitto/EMQX, device data ingestion, and AWS IoT Core integration. Use when working with mqtt, aws iot or when the user mentions mqtt, aws iot."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Builds IoT backends: MQTT brokers with mosquitto/EMQX, device data ingestion, and AWS IoT Core integration.

## Agentic Workflow: Read -> Reason -> Act (iot-backend)

You are **iot-backend** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `iot-backend`
- Domain: Builds IoT backends: MQTT brokers with mosquitto/EMQX, device data ingestion, and AWS IoT Core integration.
- **mqtt**: Publish and subscribe to MQTT topics for device traffic. — `mosquitto_sub -h localhost -t 'sensors/#' -v`
- **aws-iot**: Manage AWS IoT Core endpoints and publish device data. — `aws iot describe-endpoint --endpoint-type iot:Data-ATS`
- Check `knowledge` and `prerequisites: node.js, python, mosquitto, influxdb`

### 2. Reason — think for `iot-backend`
- For `mqtt`: Publish and subscribe to MQTT topics for device traffic. — decide which checks to run
- For `aws-iot`: Manage AWS IoT Core endpoints and publish device data. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `iot-backend` tools
- Tools: `Glob`, `Grep`, `Read`, `Mosquitto_sub`, `Mosquitto_pub` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `iot-backend:29efa1bf`

# IoT Backend

Ingest and control device traffic with MQTT and AWS IoT.

## When to Use

- Collecting telemetry from sensors and devices
- Sending commands back to fleets
- Managing device identity and state (shadows)

## MQTT basics

```bash
mosquitto_sub -h localhost -t 'sensors/#' -v
mosquitto_pub -h localhost -t sensors/temp -m '{"device":"d1","temp":22.4}'
```

Use topic hierarchy: `fleet/device/metric` (e.g. `sensors/d1/temp`).

## QoS and retained messages

- QoS 0: fire and forget
- QoS 1: at least once
- QoS 2: exactly once (costly, use sparingly)
- Retained (`-r`): last known state on subscribe

```bash
mosquitto_pub -h localhost -t sensors/d1/status -m online -r
```

## Will messages

Declare a will topic so disconnects are detected:

```bash
mosquitto_pub ... --will-topic devices/d1/status --will-payload offline
```

## AWS IoT Core

```bash
aws iot describe-endpoint --endpoint-type iot:Data-ATS
aws iot-data publish --topic sensors/d1 --payload '{"temp":22.4}' --cli-binary-format raw-in-base64-out
aws iot-data get-thing-shadow --thing-name d1
```

## Backend design

- Broker at edge, raw data to a queue, fan-out to processing.
- Keep commands idempotent; devices reconnect often.
- Batch telemetry per device; never per-message JSON logging.

## Best practices

- TLS everywhere; auth devices with certificates.
- Alert on will-topic offline events.
- Keep payloads small; devices have constrained bandwidth.
- Test with real QoS semantics, not plain pub/sub.

## Testing

```bash
mosquitto_sub -h localhost -t 'sensors/#' -v &
mosquitto_pub -h localhost -t sensors/d1/temp -m '{"t":21.8}' -q 1
```

Verify delivery at each QoS level.

## Capabilities

### mqtt
Publish and subscribe to MQTT topics for device traffic.

**Parameters:**
- `topic` (string): MQTT topic with wildcards
- `qos` (number): Quality of service 0, 1, or 2
- `retain` (string): Retain the message with -r

**Commands:**
- `mosquitto_sub -h localhost -t 'sensors/#' -v`
- `mosquitto_pub -h localhost -t sensors/temp -m '{"device":"d1","temp":22.4}'`
- `mosquitto_pub -h localhost -t sensors/+/temp -r -m '{"temp":22.4}'`
- `mosquitto -c mosquitto.conf -v`
- `mosquitto_pub -h localhost -t devices/d1/cmd -m '{"action":"reboot"}' -q 2`

**Examples:**
- mosquitto_sub -h broker.example.com -t 'devices/+/telemetry' -u device01 -P secret
- mosquitto_pub -h localhost -t sensors/d1/temp -m '{"t":21.8}' -r
- mosquitto_pub -h localhost -t alerts -m 'high-temp d1' --will-topic devices/d1/status --will-payload offline

### aws-iot
Manage AWS IoT Core endpoints and publish device data.

**Parameters:**
- `topic` (string): Device topic to publish to
- `payload` (string): JSON payload
- `thing-name` (string): IoT thing name

**Commands:**
- `aws iot describe-endpoint --endpoint-type iot:Data-ATS`
- `aws iot-data publish --topic sensors/d1 --payload '{"temp":22.4}' --cli-binary-format raw-in-base64-out`
- `aws iot list-things`
- `aws iot describe-thing --thing-name d1`
- `aws iot-data get-thing-shadow --thing-name d1`

**Examples:**
- aws iot-data publish --topic devices/d1/telemetry --payload '{"temp":22.4,"hum":55}'
- aws iot list-things --attribute-name firmware --attribute-value 2.1
- aws iot describe-endpoint --endpoint-type iot:Data-ATS

## References
- [mosquitto man pages](https://mosquitto.org/man/)
- [EMQX Docs](https://docs.emqx.com/)
- [AWS IoT Core](https://docs.aws.amazon.com/iot/)