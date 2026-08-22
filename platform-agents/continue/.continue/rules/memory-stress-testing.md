---
name: "Memory Stress Testing"
description: "Stress test memory on Linux hosts: stress-ng and memtester workloads, OOM behavior checks, and system memory monitoring."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

# Memory Stress Testing

Stress test memory on Linux hosts: stress-ng and memtester workloads, OOM behavior checks, and system memory monitoring.

## Instructions

# Memory Stress Testing

Stress and validate memory subsystems on Linux hosts.

## What this skill does

- Runs memory stressors with stress-ng (allocation, dirtying, hang).
- Tests RAM correctness with memtester.
- Monitors pressure with free, vmstat, and /proc/meminfo.

## When to use

- Validating VM sizing before production load.
- Hunting OOM-killer surprises under high allocation.
- Verifying memory cgroup limits behave.

## Real commands

```bash
# 4 stressors, 2G each, 60s
stress-ng --vm 4 --vm-bytes 2G --timeout 60s

# 75% of available RAM, all methods
stress-ng --vm 2 --vm-bytes 75% --vm-method all --timeout 30s

# Allocate and hold (swap-test)
stress-ng --vm 1 --vm-bytes 1G --vm-hang 10 --timeout 60s

# With metrics summary
stress-ng --vm 4 --vm-bytes 2G --metrics-brief --timeout 60s

# RAM correctness test (512 MiB, 5 passes)
memtester 512M 5

# Classic stress
stress --vm 2 --vm-bytes 1G --vm-hang 0 --timeout 120

# Monitor
free -h
vmstat 1 10
cat /proc/meminfo | head -8
```

## Testing

```bash
# Watch swap and OOM behavior while stressing
stress-ng --vm 4 --vm-bytes 2G --timeout 60s &
vmstat 1 10
dmesg --level=err | grep -i 'out of memory' || echo 'no OOM'
```

## Best practices

- Never stress memory on production boxes without change control.
- Use --vm-method all for thorough fault coverage in staging.
- Combine with swap limits (ulimit -v) to test graceful degradation.

## Capabilities

### stress-ng
Run memory stress workloads with stress-ng.

**Commands:**
- `stress-ng --vm 4 --vm-bytes 2G --timeout 60s`
- `stress-ng --vm 2 --vm-bytes 75% --vm-method all --timeout 30s`
- `stress-ng --vm 1 --vm-bytes 1G --vm-hang 10 --timeout 60s`
- `stress-ng --vm 4 --vm-bytes 2G --metrics-brief --timeout 60s`

**Examples:**
- stress-ng --vm 4 --vm-bytes 2G --timeout 60s
- stress-ng --vm 2 --vm-bytes 75% --vm-method all --timeout 30s
- stress-ng --vm 4 --vm-bytes 2G --metrics-brief --timeout 60s

### memtester-monitor
Run memtester and monitor memory pressure.

**Commands:**
- `memtester 512M 5`
- `free -h`
- `vmstat 1 10`
- `cat /proc/meminfo | head -8`
- `stress --vm 2 --vm-bytes 1G --vm-hang 0 --timeout 120`

**Examples:**
- memtester 512M 5
- free -h
- vmstat 1 10