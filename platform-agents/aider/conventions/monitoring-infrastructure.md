Baseline host monitoring on Linux: CPU, memory, disk, and network telemetry with top, vmstat, iostat, and sar.

## Agentic Workflow: Read -> Reason -> Act (monitoring-infrastructure)

You are **monitoring-infrastructure** (infrastructure/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `monitoring-infrastructure`
- Domain: Baseline host monitoring on Linux: CPU, memory, disk, and network telemetry with top, vmstat, iostat, and sar.
- **host-metrics**: Collect instant host utilization snapshots. — `uptime`
- **history**: Review historical utilization with sysstat sar. — `sar -u 1 3`
- Check `knowledge` and `prerequisites: free, iostat, sar, top`

### 2. Reason — think for `monitoring-infrastructure`
- For `host-metrics`: Collect instant host utilization snapshots. — decide which checks to run
- For `history`: Review historical utilization with sysstat sar. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `monitoring-infrastructure` tools
- Tools: `Glob`, `Grep`, `Read`, `Uptime`, `Vmstat` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `monitoring-infrastructure:490ef6b9`

# Host Monitoring

Measure host health with the standard Linux toolbox.

## When to Use

- Investigating a slow host or application
- Checking whether a problem is CPU, memory, disk, or network
- Baseline capacity for autoscaling decisions

## Quick triage

```bash
uptime
free -h
vmstat 1 5
```

`uptime` load averages vs CPU count tells you if the box is oversubscribed.

## CPU

```bash
vmstat 1 5   # us, sy, id, wa columns
sar -u 1 3
```

High `wa` = disk-bound; high `sy` = system call overhead.

## Memory

```bash
free -h
sar -r 1 3
```

Watch `available`, not just `free` - caches reclaim gracefully.

## Disk

```bash
iostat -x 1 3
df -h | grep -v tmpfs
```

`%util` near 100% with long `await` means the disk is saturated.

## Network

```bash
sar -n DEV 1 3
```

## Saturation signals

- CPU: run queue length > cores for sustained periods
- Memory: sustained swapping in `si`/`so`
- Disk: `%util` saturation or high `await`
- Network: dropped packets in `/proc/net/dev`

## Best practices

- Keep sysstat enabled so you can answer "what changed at 02:00?"
- Correlate metrics with deploys; most incidents follow releases.
- Feed these into Prometheus exporters for alerting.
- Record a baseline after each major release.

## Testing

```bash
sar -u 1 5 && vmstat 1 3
```

Generate load and confirm metrics move - otherwise the collector is broken.

## Capabilities

### host-metrics
Collect instant host utilization snapshots.

**Parameters:**
- `interval` (number): Sample interval in seconds
- `count` (number): Number of samples
- `extended` (string): -x extended statistics for iostat

**Commands:**
- `uptime`
- `vmstat 1 5`
- `free -h`
- `iostat -x 1 3`
- `top -b -n 1 | head -25`

**Examples:**
- vmstat 2 10
- iostat -x -d 1 3 | grep -E 'Device|sda'
- free -h && df -h | grep -v tmpfs

### history
Review historical utilization with sysstat sar.

**Parameters:**
- `report` (string): Report type: -u CPU, -r memory, -d disk, -n network, -q load
- `interval` (number): Sample interval
- `file` (string): Historical sa file with -f

**Commands:**
- `sar -u 1 3`
- `sar -r 1 3`
- `sar -d 1 3`
- `sar -n DEV 1 3`
- `sar -q 1 3`

**Examples:**
- sar -u -f /var/log/sysstat/sa10
- sar -n TCP 1 5
- sar -q 1 5

## References
- [sysstat (sar/iostat)](https://github.com/sysstat/sysstat)
- [vmstat man page](https://man7.org/linux/man-pages/man8/vmstat.8.html)
- [Linux Performance](https://www.brendangregg.com/linuxperf.html)
