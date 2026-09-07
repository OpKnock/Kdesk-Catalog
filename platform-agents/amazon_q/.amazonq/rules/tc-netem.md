Simulate network faults with the Linux tc netem qdisc to test API client resilience. Injects latency with jitter, packet loss, duplication, and corruption on any interface, then measures the impact with ping or curl timing. Removes faults instantly after testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tc qdisc add dev eth0 root netem delay 100ms 20ms distributi`
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

# tc netem

Hand-crafted skill for network fault injection with the netem qdisc.

## What this skill does

- Adds latency with jitter to a network interface
- Drops, duplicates, and corrupts packets at a configurable rate
- Removes the fault instantly to restore normal traffic

## When to use

- Testing timeouts in API clients under delay
- Verifying retry logic when packets drop
- Chaos drills: does the app survive a flaky network?

## Real commands

```bash
# 100ms latency with 20ms jitter (normal distribution)
tc qdisc add dev eth0 root netem delay 100ms 20ms distribution normal

# Drop 10% of packets
tc qdisc change dev eth0 root netem loss 10%

# Duplicate and corrupt
tc qdisc add dev eth0 root netem duplicate 2% corrupt 1%

# Reorder with delay
tc qdisc add dev eth0 root netem delay 50ms reorder 25% gap 3

# Inspect the active qdisc
tc qdisc show dev eth0

# Measure the impact
ping -c 10 192.168.1.1

# Remove all netem rules
tc qdisc del dev eth0 root
```

## Test recipe

```bash
tc qdisc add dev eth0 root netem delay 200ms
curl -s -o /dev/null -w 'total: %{time_total}s\n' https://api.example.com/health
tc qdisc del dev eth0 root
```

## Best practices

- Always pair tests with ping or curl timing to measure the injection
- Remove the qdisc after the test: del dev eth0 root
- Prefer a dedicated test VM; netem affects all traffic on the host

## Capabilities

### netem-injection
Simulate network faults with tc netem qdiscs

**Parameters:**
- `delay_ms` (integer): Base latency in milliseconds
- `loss_percent` (float): Packet loss percentage
- `jitter_ms` (integer): Delay variation around the base

**Commands:**
- `tc qdisc add dev eth0 root netem delay 100ms 20ms distribution normal`
- `tc qdisc change dev eth0 root netem loss 10%`
- `tc qdisc add dev eth0 root netem duplicate 2% corrupt 1%`
- `tc qdisc show dev eth0`
- `tc qdisc del dev eth0 root`
- `ping -c 10 192.168.1.1`

**Examples:**
- tc qdisc change dev eth0 root netem loss 25%
- tc qdisc add dev eth0 root netem delay 200ms
- tc qdisc del dev eth0 root

## References
- [tc-netem man page](https://man7.org/linux/man-pages/man8/tc-netem.8.html)
- [Linux tc man page](https://man7.org/linux/man-pages/man8/tc.8.html)