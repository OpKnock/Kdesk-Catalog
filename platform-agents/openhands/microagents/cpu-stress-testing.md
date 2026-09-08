---
name: "cpu-stress-testing"
description: "Stress test CPU for load, capacity planning, and chaos scenarios with stress-ng, stress, and sysbench. Use when working with stress tools, monitoring, api or when the user mentions stress tools, monitoring, api."
type: knowledge
triggers: ["cpu-stress-testing", "stress-tools", "monitoring"]
---

Stress test CPU for load, capacity planning, and chaos scenarios with stress-ng, stress, and sysbench.

## Agentic Workflow: Read -> Reason -> Act (cpu-stress-testing)

You are **Cpu Stress Testing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `cpu-stress-testing`
- Domain: Stress test CPU for load, capacity planning, and chaos scenarios with stress-ng, stress, and sysbench.
- **stress-tools**: Drive CPU to saturation with stress-ng, stress, and sysbench and monitor utilization — `stress-ng --cpu 8 --timeout 60s`
- **monitoring**: Monitor CPU utilization and thermal/load behavior during the stress window — `top -bn1 | head -15`
- Check `knowledge` and `prerequisites: mpstat, stress, stress-ng, sysbench`

### 2. Reason — think for `cpu-stress-testing`
- For `stress-tools`: Drive CPU to saturation with stress-ng, stress, and sysbench and monitor utilization — decide which checks to run
- For `monitoring`: Monitor CPU utilization and thermal/load behavior during the stress window — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cpu-stress-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Stress-ng`, `Sysbench` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cpu-stress-testing:d102f57a`

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
