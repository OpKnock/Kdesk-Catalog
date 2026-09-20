---
applyTo: "**/*.go **/*.r **/*.sh"
---

# Cpu Stress Testing

Stress test CPU for load, capacity planning, and chaos scenarios with stress-ng, stress, and sysbench.

## Instructions

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

**Commands:**
- `top -bn1 | head -15`
- `mpstat -P ALL 1 5`
- `stress-ng --cpu 8 --timeout 60s --metrics-brief`
- `vmstat 1 5`

**Examples:**
- top -bn1 | head -15
- mpstat -P ALL 1 3
- vmstat 1 5
