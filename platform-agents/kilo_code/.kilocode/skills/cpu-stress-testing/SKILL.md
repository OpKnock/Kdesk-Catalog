---
name: "cpu-stress-testing"
description: "Stress test CPU for load, capacity planning, and chaos scenarios with stress-ng, stress, and sysbench. Use when working with stress tools, monitoring, api or when the user mentions stress tools, monitoring, api."
license: "MIT"
compatibility: "Requires mpstat, stress, stress-ng, sysbench, top, vmstat."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(mpstat:*) Bash(stress:*) Bash(stress-ng:*) Bash(sysbench:*) Bash(top:*) Bash(vmstat:*)"
---

Stress test CPU for load, capacity planning, and chaos scenarios with stress-ng, stress, and sysbench.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `stress-ng --cpu 8 --timeout 60s`, `top -bn1 | head -15`
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

# CPU Stress Testing

Saturate CPU in a controlled way to validate capacity and resilience.

## When to Use

- Capacity planning for API servers
- Testing autoscaling and CPU alerts
- Chaos scenarios: CPU spike during deployments

## Install

```bash
# Debian/Ubuntu
sudo apt install stress-ng sysbench stress
# macOS
brew install stress-ng
```

## Stress Runs

```bash
# All cores, 60 seconds
stress-ng --cpu 8 --timeout 60s

# 80% load on 4 cores
stress-ng --cpu 4 --cpu-load 80 --timeout 30s

# Classic stress
stress --cpu 4 --timeout 60

# sysbench prime test
sysbench cpu --cpu-max-prime=20000 --threads=4 run
```

## Metrics

```bash
stress-ng --cpu 8 --timeout 60s --metrics-brief
mpstat -P ALL 1 5
vmstat 1 5
top -bn1 | head -15
```

## Measuring Saturation

stress-ng reports bogo-ops per second as a throughput proxy; sysbench reports total time and events per second.

## Testing

```bash
# Verify alert fires at 90%+ utilization during the window
stress-ng --cpu 4 --cpu-load 95 --timeout 120s
```

## Best Practices

- Never run stress tests on production without approval
- Use --cpu-load to simulate realistic partial saturation
- Run a baseline before the test
- Pair with monitoring to correlate latency and CPU
- Set hard timeouts to avoid runaway load
- Use --metrics-brief for machine-readable results
- Check thermal throttling on physical hosts

## Capabilities

### stress-tools
Drive CPU to saturation with stress-ng, stress, and sysbench and monitor utilization

**Parameters:**
- `workers` (string): Number of CPU workers
- `timeout` (string): Duration such as 60s or 1m

**Commands:**
- `stress-ng --cpu 8 --timeout 60s`
- `stress-ng --cpu 4 --cpu-load 80 --timeout 30s`
- `sysbench cpu --cpu-max-prime=20000 --threads=4 run`
- `stress --cpu 4 --timeout 60`

**Examples:**
- stress-ng --cpu 8 --timeout 60s
- stress-ng --cpu 4 --cpu-load 75 --timeout 120s --metrics-brief
- sysbench cpu --cpu-max-prime=10000 --threads=1 run

### monitoring
Monitor CPU utilization and thermal/load behavior during the stress window

**Parameters:**
- `interval` (string): Sample interval in seconds

**Commands:**
- `top -bn1 | head -15`
- `mpstat -P ALL 1 5`
- `stress-ng --cpu 8 --timeout 60s --metrics-brief`
- `vmstat 1 5`

**Examples:**
- top -bn1 | head -15
- mpstat -P ALL 1 3
- vmstat 1 5

## References
- [stress-ng reference](https://manpages.ubuntu.com/manpages/trusty/man1/stress-ng.1.html)
- [sysbench documentation](https://github.com/akopytov/sysbench)
