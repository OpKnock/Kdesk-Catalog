---
name: "gremlin"
description: "Gremlin chaos engineering platform operations: launching and halting CPU, disk, memory, and network attacks against production and staging hosts."
---

# Gremlin

Gremlin chaos engineering platform operations: launching and halting CPU, disk, memory, and network attacks against production and staging hosts.

## Instructions

# Gremlin

Real chaos engineering experiments using the `gremlin` CLI.

## What this skill does

- Launches targeted attacks (CPU, memory, disk, network, process) on hosts or containers.
- Runs and manages failure scenarios across teams and infrastructure.
- Halts attacks before they reach the blast radius limit.
- Resolves host IDs and API key configuration for the CLI.

## When to use

- A team wants to verify autoscaling or failover behavior under load.
- An incident review asks: what happens if a node loses network or disk fills up.
- Validating SLOs and retry logic with real failure injection.

## Real commands

```bash
# Install and authenticate
curl -sSL https://www.gremlin.com/install | bash
sudo gremlin service install
sudo gremlin service start
gremlin api-key set abcd1234-your-api-key

# CPU attack: peg all cores for 2 minutes
sudo gremlin i attack -t "cpu" -a cpu=100 -a duration=120 -a cores=4

# Memory attack: consume 90% of RAM for 30s
sudo gremlin i attack -t "memory" -a memory=90 -a duration=30

# Disk attack: write to /data until 50% full
sudo gremlin i attack -t "disk" -a disk=50 -a path=/data -a duration=60

# Network attack: drop 50% of packets
sudo gremlin i attack -t "network" -a device=eth0 -a latency=0 -a packet_loss=50 -a duration=60

# Shutdown an attack immediately
sudo gremlin i shutdown

# List running and past attacks
sudo gremlin attack list
sudo gremlin scenario list
```

## Configuration

Team IDs and API keys come from the Gremlin web console:

```bash
gremlin api-key set <API_KEY>
sudo gremlin init --team_id <team-id>
```

Scenarios are declared in YAML:

```yaml
scenarios:
  - name: failover-test
    attacks:
      - type: cpu
        args: ["-a", "cpu=100", "-a", "duration=60"]
      - type: network
        args: ["-a", "packet_loss=30"]
```

## Testing

- Run a short 10s CPU attack in staging and verify the target app recovers.
- Confirm `gremlin i shutdown` ends attacks: `gremlin attack list` should then be empty.
- Check `gremlin i attack --help` before running a new attack type.

## Best practices

- Always set `-a duration`; default attacks can run 10 minutes.
- Start with the smallest blast radius: one host, one attack type.
- Pair the attack with a validation check (e.g., HTTP 200 after 30s).
- Run a scheduled shutdown as a safety net in CI.
- Never run unauthenticated attacks: verify `gremlin attack list` shows the team first.

## Example exchange

```
User: Start a 5-minute CPU attack on the prod-web host, halt after 2 minutes.
Agent: sudo gremlin i attack -t "cpu" -a cpu=100 -a duration=300 -a host_id=prod-web
       # after 120s of observing: sudo gremlin i shutdown
```

## Capabilities

### attack-management
Create, list, and halt chaos attacks and scenarios via the Gremlin CLI and API.

**Commands:**
- `gremlin i attack -t "disk" -a disk=50 -a path=/`
- `gremlin i shutdown`
- `gremlin attack list`
- `gremlin scenario list`
- `gremlin api-key set demo-key`

**Examples:**
- sudo gremlin i attack -t "cpu" -a cpu=100 -a duration=60 -a cores=4
- sudo gremlin i attack -t "memory" -a memory=90 -a duration=30
- sudo gremlin i shutdown
