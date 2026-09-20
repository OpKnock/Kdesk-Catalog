---
name: "bulkhead-pattern"
description: "Designs bulkhead isolation for services: resource partitioning, thread pool sizing, connection limits, and failure containment. Use when working with capacity planning, pool isolation, failure test, api or when the user mentions capacity planning, pool isolation, failure test, api."
---

Designs bulkhead isolation for services: resource partitioning, thread pool sizing, connection limits, and failure containment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ps -o nlwp,pcpu,pmem,rss -p $(pgrep -f my-api)`, `java -XX:+PrintFlagsFinal -version | grep -i threads`
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

# Bulkhead Pattern

## What this skill does

Designs bulkhead isolation so one service partition cannot exhaust shared resources: sizing thread/connection pools, partitioning by dependency or tenant, and verifying failure containment with load tests.

## When to use

- One slow dependency is starving the whole service
- Multi-tenant APIs need isolated quotas
- Adding capacity planning for thread pools

## Real commands

```bash
# Measure current capacity
ps -o nlwp,pcpu,pmem,rss -p $(pgrep -f my-api)
ss -s
ulimit -n

# Inspect pool usage (JVM)
jstack $(pgrep -f app.jar) | grep -c '"pool-'
curl -s http://localhost:8080/actuator/metrics/executor.active

# Failure containment test
ab -n 5000 -c 200 http://localhost:8080/api/slow
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/fast
```

## Design rules

- One pool per dependency/tenant group: pool-a, pool-b
- Pool size = max concurrent calls the dependency can serve
- Queue lengths bounded; overflow rejects fast (503)

## Testing

- Saturate one partition with ab; assert the other partition stays healthy
- Watch thread counts with top/jstack during the test

## Best practices

- Separate pools for CPU vs I/O work
- Set short queue timeouts so rejection is immediate
- Monitor pool utilization and size alerts on saturation

## Capabilities

### capacity-planning
Measure and size bulkhead partitions.

**Parameters:**
- `pid` (string): Process ID or pgrep pattern
- `fd_limit` (number): File descriptor limit

**Commands:**
- `ps -o nlwp,pcpu,pmem,rss -p $(pgrep -f my-api)`
- `ulimit -n`
- `ss -s`
- `docker stats --no-stream`
- `vmstat 1 5`

**Examples:**
- ps -o nlwp,pcpu,pmem -p $(pgrep -f my-api)
- ss -s | grep -E 'estab|total'
- docker stats --no-stream $(docker ps -q) | column -t

### pool-isolation
Configure isolated thread pools and connection pools.

**Parameters:**
- `pool_name` (string): Thread pool name
- `pool_size` (number): Pool size

**Commands:**
- `java -XX:+PrintFlagsFinal -version | grep -i threads`
- `jstack $(pgrep -f my-api) | grep -c 'pool-'`
- `jcmd $(pgrep -f my-api) Thread.print | grep -A2 'pool-'`
- `curl -s http://localhost:8080/actuator/metrics/executor.active`

**Examples:**
- jstack $(pgrep -f app.jar) | grep -c '"pool-'
- curl -s http://localhost:8080/actuator/metrics/executor.active | jq '.measurements'
- jcmd $(pgrep -f app.jar) Thread.print > threads.txt

### failure-test
Verify a partition failure does not exhaust shared resources.

**Parameters:**
- `slow_endpoint` (string): Endpoint under failure
- `fast_endpoint` (string): Endpoint that must stay healthy

**Commands:**
- `ab -n 5000 -c 200 http://localhost:8080/api/slow`
- `curl -s -o /dev/null -w "%{http_code} %{time_total}\n" http://localhost:8080/api/fast`
- `watch -n1 'curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/fast'`
- `top -b -n 3 -p $(pgrep -f my-api)`

**Examples:**
- ab -n 5000 -c 200 http://localhost:8080/api/slow; curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/fast
- watch -n1 'curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/fast'
- top -b -n 3 -p $(pgrep -f app.jar) | tail -12

## References
- [Bulkhead Pattern (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead)
- [Resilience4j Bulkhead](https://resilience4j.readme.io/docs/bulkhead)
- [Isolation (Istio)](https://istio.io/latest/docs/tasks/traffic-management/circuit-breaking/)
