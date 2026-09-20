---
name: "bulkhead-pattern"
description: "Designs bulkhead isolation for services: resource partitioning, thread pool sizing, connection limits, and failure containment."
type: knowledge
triggers: ["bulkhead-pattern", "capacity-planning", "pool-isolation", "failure-test"]
---

# Bulkhead Pattern

Designs bulkhead isolation for services: resource partitioning, thread pool sizing, connection limits, and failure containment.

## Instructions

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

**Commands:**
- `ab -n 5000 -c 200 http://localhost:8080/api/slow`
- `curl -s -o /dev/null -w "%{http_code} %{time_total}\n" http://localhost:8080/api/fast`
- `watch -n1 'curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/fast'`
- `top -b -n 3 -p $(pgrep -f my-api)`

**Examples:**
- ab -n 5000 -c 200 http://localhost:8080/api/slow; curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/fast
- watch -n1 'curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/fast'
- top -b -n 3 -p $(pgrep -f app.jar) | tail -12
