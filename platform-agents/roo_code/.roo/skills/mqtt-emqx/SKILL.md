---
name: "mqtt-emqx"
description: "Operate EMQX MQTT brokers: start/stop, cluster status, publish/subscribe via emqx ctl, and dashboard access."
---

# Mqtt Emqx

Operate EMQX MQTT brokers: start/stop, cluster status, publish/subscribe via emqx ctl, and dashboard access.

## Instructions

# EMQX

EMQX is a scalable open-source MQTT broker for IoT and edge workloads.

## What this skill does

- Starts/stops the broker and checks status
- Publishes and subscribes from the CLI for testing
- Inspects clusters and listeners

## When to use

- Deploying a production MQTT broker
- Verifying connectivity and message flow end-to-end
- Scaling to a multi-node EMQX cluster

## Real commands

```bash
# Start and check
emqx start
emqx ctl status

# Publish from CLI
emqx ctl broker pub test/topic "hello"
emqx ctl broker pub demo/temp "21.5" --qos 1

# Subscribe from CLI
emqx ctl broker sub test/topic --qos 1

# Cluster and listeners
emqx ctl cluster status
emqx ctl listener list
```

## Dashboard

- Web UI: `http://localhost:18083` (default admin/public)

## Config files

- `/etc/emqx/emqx.conf` - node name, listeners, auth
- Authentication: `emqx ctl authn ...`? Use built-in MQTT auth users or HTTP auth

## Best practices

- Pin EMQX version and test upgrades on staging
- Configure TLS listeners for production (`listener.ssl.external`)
- Monitor `emqx ctl broker metrics` for dropped messages

## Capabilities

### emqx-broker-operations
Control the EMQX broker daemon and inspect clusters, subscriptions and message traffic with emqx ctl.

**Commands:**
- `emqx start`
- `emqx ctl status`
- `emqx ctl broker pub test/topic "hello"`
- `emqx ctl broker sub test/topic`
- `emqx ctl cluster status`

**Examples:**
- emqx ctl broker pub demo/temp "21.5" --qos 1
- emqx ctl broker sub demo/temp --qos 1
- emqx ctl listener list
