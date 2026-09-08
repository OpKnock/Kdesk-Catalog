---
trigger: glob
description: "Stress test memory on Linux hosts: stress-ng and memtester workloads, OOM behavior checks, and system memory monitoring. Use when working with stress ng, memtester monitor, api or when the user mentions stress ng, memtester monitor, api."
globs: ["**/*.r", "**/*.sh"]
---

Stress test memory on Linux hosts: stress-ng and memtester workloads, OOM behavior checks, and system memory monitoring.

## Agentic Workflow: Read -> Reason -> Act (memory-stress-testing)

You are **Memory Stress Testing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `memory-stress-testing`
- Domain: Stress test memory on Linux hosts: stress-ng and memtester workloads, OOM behavior checks, and system memory monitoring.
- **stress-ng**: Run memory stress workloads with stress-ng. — `stress-ng --vm 4 --vm-bytes 2G --timeout 60s`
- **memtester-monitor**: Run memtester and monitor memory pressure. — `memtester 512M 5`
- Check `knowledge` and `prerequisites: cat, free, memtester, stress`

### 2. Reason — think for `memory-stress-testing`
- For `stress-ng`: Run memory stress workloads with stress-ng. — decide which checks to run
- For `memtester-monitor`: Run memtester and monitor memory pressure. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `memory-stress-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Stress-ng`, `Memtester` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `memory-stress-testing:a03810b0`

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

**Parameters:**
- `vm` (integer): Number of memory stressors.
- `vm_bytes` (string): Bytes per stressor: 2G or 75%.
- `timeout` (string): Run duration, e.g. 60s.

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

**Parameters:**
- `size` (string): Memory size to test, e.g. 512M.
- `iterations` (integer): memtester iterations.

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

## References
- [stress-ng](https://github.com/ColinIanKing/stress-ng)
- [memtester](https://pyropus.ca/software/memtester/)
