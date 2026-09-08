Operate EMQX MQTT brokers: start/stop, cluster status, publish/subscribe via emqx ctl, and dashboard access.

## Agentic Workflow: Read -> Reason -> Act (mqtt-emqx)

You are **Mqtt Emqx** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mqtt-emqx`
- Domain: Operate EMQX MQTT brokers: start/stop, cluster status, publish/subscribe via emqx ctl, and dashboard access.
- **emqx-broker-operations**: Control the EMQX broker daemon and inspect clusters, subscriptions and message traffic with emqx ctl — `emqx start`
- Check `knowledge` and `prerequisites: emqx`

### 2. Reason — think for `mqtt-emqx`
- For `emqx-broker-operations`: Control the EMQX broker daemon and inspect clusters, subscriptions and message traffic with emqx ctl. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mqtt-emqx` tools
- Tools: `Glob`, `Grep`, `Read`, `Emqx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mqtt-emqx:dc949424`

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

**Parameters:**
- `topic` (string): MQTT topic to publish or subscribe to
- `qos` (integer): Quality of service level 0, 1 or 2
- `payload` (string): Message payload to publish

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

## References
- [EMQX Documentation](https://docs.emqx.com/en/emqx/latest/)
- [EMQX Dashboard](https://docs.emqx.com/en/emqx/latest/admin/observability/dashboard.html)