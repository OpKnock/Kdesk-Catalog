---
name: "network-partition-testing"
description: "Injects network faults with tc netem for latency and packet loss, drops traffic via iptables, and captures packets with tcpdump to validate service resilience under partitions. Use when working with network fault injection, api or when the user mentions network fault injection, api."
license: "MIT"
compatibility: "Requires iptables, tcpdump."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(iptables:*) Bash(tc:*) Bash(tcpdump:*)"
---

Injects network faults with tc netem for latency and packet loss, drops traffic via iptables, and captures packets with tcpdump to validate service resilience under partitions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tc qdisc add dev eth0 root netem loss 100%`
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

# Network Partition Testing

Verify that services survive partitions, latency and packet loss before they happen in production.

## What this skill does

- Emulates packet loss/latency with tc netem
- Drops traffic selectively with iptables
- Captures traffic to confirm behavior

## When to use

- Chaos engineering for distributed systems
- Validating retries, timeouts and circuit breakers

## Real commands

```bash
# Full partition: drop all packets on the link
 tc qdisc add dev eth0 root netem loss 100%

# Partial failure: 10% loss + 200ms latency
 tc qdisc change dev eth0 root netem loss 10% latency 200ms

# Restore
 tc qdisc del dev eth0 root

# Drop all traffic from one host (test cluster isolation)
 iptables -A INPUT -s 10.0.0.2 -j DROP
 iptables -D INPUT -s 10.0.0.2 -j DROP   # undo

# Capture for verification
 tcpdump -i eth0 -c 20 host 10.0.0.2 -w capture.pcap
```

## Verify impact

```bash
ping -c 5 10.0.0.2
curl -s -o /dev/null -w "%{time_total}\n" http://10.0.0.2:8080/health
```

## Best practices

- Start with small loss percentages, then escalate
- Always schedule automatic revert (tc qdisc del)
- Run against staging, never production without care

## Capabilities

### network-fault-injection
Inject link loss/latency with tc netem, drop traffic with iptables, and capture traffic with tcpdump.

**Parameters:**
- `interface` (string): Network interface to modify
- `loss_percent` (integer): Packet loss percentage
- `target_host` (string): Host IP for iptables/tcpdump rules

**Commands:**
- `tc qdisc add dev eth0 root netem loss 100%`
- `tc qdisc change dev eth0 root netem loss 10% latency 200ms`
- `tc qdisc del dev eth0 root`
- `iptables -A INPUT -s 10.0.0.2 -j DROP`
- `tcpdump -i eth0 -c 20 host 10.0.0.2 -w capture.pcap`

**Examples:**
- tc qdisc add dev eth0 root netem delay 500ms 100ms distribution normal
- iptables -D INPUT -s 10.0.0.2 -j DROP
- tc qdisc show dev eth0

## References
- [tc-netem man page](https://man7.org/linux/man-pages/man8/tc-netem.8.html)
- [tcpdump man page](https://man7.org/linux/man-pages/man8/tcpdump.8.html)
