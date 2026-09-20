---
type: agent_requested
description: "Inject network latency and packet loss with Linux tc netem: add/change/remove qdisc rules and measure the impact with ping and curl."
---

# Latency Injection

Inject network latency and packet loss with Linux tc netem: add/change/remove qdisc rules and measure the impact with ping and curl.

## Instructions

# Latency Injection

Emulate network conditions (latency, jitter, loss) with Linux tc netem.

## What this skill does

- Adds netem qdisc rules with delay, jitter, and loss.
- Changes rules live and removes them cleanly.
- Measures the impact with ping, curl, and mtr.

## When to use

- Chaos/resilience testing for cross-datacenter flows.
- Testing timeouts and retry logic in clients.
- Validating SLO behavior under degraded networks.

## Real commands

```bash
# Add 200ms delay
sudo tc qdisc add dev eth0 root netem delay 200ms

# Delay with jitter (200ms +/- 50ms, normal distribution)
sudo tc qdisc change dev eth0 root netem delay 200ms 50ms distribution normal

# Packet loss 5%
sudo tc qdisc change dev eth0 root netem loss 5%

# Combined rule
sudo tc qdisc add dev eth0 root netem delay 200ms loss 2% duplicate 1%

# Show current rule
tc qdisc show dev eth0

# Measure impact
ping -c 10 10.0.0.5 | tail -3
curl -s -o /dev/null -w 'total: %{time_total}s\n' http://10.0.0.5/
mtr -r -c 10 10.0.0.5 | tail -5

# Remove the rule (restore normal networking)
sudo tc qdisc del dev eth0 root netem
```

## Testing

```bash
# Before/after comparison
ping -c 5 10.0.0.5 | tail -2   # baseline
sudo tc qdisc add dev eth0 root netem delay 300ms
ping -c 5 10.0.0.5 | tail -2   # injected
sudo tc qdisc del dev eth0 root netem
```

## Best practices

- Inject on the test path only; never on production interfaces without change control.
- Always pair injection with cleanup (tc qdisc del) in a trap/finally block.
- Start with small values (50-100ms) and scale up gradually.

## Capabilities

### netem-rules
Add, change, and remove latency/loss rules on interfaces.

**Commands:**
- `tc qdisc add dev eth0 root netem delay 200ms`
- `tc qdisc change dev eth0 root netem delay 200ms 50ms distribution normal`
- `tc qdisc change dev eth0 root netem loss 5%`
- `tc qdisc add dev eth0 root netem delay 200ms loss 2% duplicate 1%`
- `tc qdisc del dev eth0 root netem`

**Examples:**
- tc qdisc add dev eth0 root netem delay 200ms
- tc qdisc change dev eth0 root netem delay 200ms 50ms distribution normal
- tc qdisc del dev eth0 root netem

### impact-measure
Measure latency and application impact after injection.

**Commands:**
- `tc qdisc show dev eth0`
- `ping -c 10 10.0.0.5 | tail -3`
- `curl -s -o /dev/null -w 'total: %{time_total}s\n' http://10.0.0.5/`
- `mtr -r -c 10 10.0.0.5 | tail -5`

**Examples:**
- ping -c 10 10.0.0.5 | tail -3
- curl -s -o /dev/null -w 'total: %{time_total}s\n' http://10.0.0.5/
- tc qdisc show dev eth0