---
trigger: glob
description: "HTTP load generation with hey: concurrency sweeps, fixed-duration tests, POST payloads, custom headers, and latency report interpretation."
globs: ["**/*.r", "**/*.sh"]
---

# Hey

HTTP load generation with hey: concurrency sweeps, fixed-duration tests, POST payloads, custom headers, and latency report interpretation.

## Instructions

# hey

HTTP load generation with the hey CLI.

## What this skill does

- Blasts an endpoint with N requests at C concurrency.
- Runs time-boxed tests with -z.
- Sends custom methods, headers, and bodies.
- Produces latency percentiles, throughput, and CSV output.

## When to use

- Quick smoke load tests before full suites (see load-testing skills).
- Comparing two versions of an API under identical load.
- Reproducing latency reports from incident alerts.

## Real commands

```bash
# 10k requests, 100 concurrent
hey -n 10000 -c 100 http://localhost:8080/api

# 30 second run with POST body
hey -z 30s -c 200 -m POST -d '{"x":1}' http://localhost:8080/api

# Custom header
hey -n 1000 -c 10 -H "Authorization: Bearer tok" http://localhost:8080/private

# Disable keepalive (worst-case connection churn)
hey -disable-keepalive -c 50 http://localhost:8080/api

# CSV output for analysis
hey -n 10000 -c 100 -o csv http://localhost:8080/api > results.csv
```

## Reading the report

```text
Summary:
  Total:        15.0212 secs
  Slowest:      0.8421 secs
  Fastest:      0.0021 secs
  Average:      0.0481 secs
  Requests/sec: 665.7272

Latency distribution:
  10% in 0.0024 secs
  50% in 0.0312 secs
  90% in 0.0987 secs
  99% in 0.4012 secs

Status code distribution:
  [200] 10000 responses
```

## Testing

```bash
# Fail when p99 exceeds 500ms
hey -n 10000 -c 100 http://localhost:8080/api | awk '/99%/{ if ($4 > 0.5) exit 1 }'
```

## Best practices

- Run at least 5k requests for stable percentiles.
- Compare p50/p95/p99, not just average.
- Sweep concurrency: 10, 50, 100, 200 to find the knee point.
- Always record the load parameters with the report for reproducibility.

## Example exchange

```
User: Is /api fast enough at 100 concurrent users?
Agent: hey -n 10000 -c 100 http://localhost:8080/api
       # p99 under 500ms and 0 errors means yes
```

## Capabilities

### hey-load
Generate HTTP load and read hey's latency/throughput reports.

**Commands:**
- `hey -n 10000 -c 100 http://localhost:8080/api`
- `hey -z 30s -c 200 -m POST -d '{"x":1}' http://localhost:8080/api`
- `hey -n 1000 -c 10 -H "Authorization: Bearer tok" http://localhost:8080/private`
- `hey -disable-keepalive -c 50 http://localhost:8080/api`
- `hey -n 10000 -c 100 -o csv http://localhost:8080/api > results.csv`

**Examples:**
- hey -z 60s -c 50 -c 100 http://localhost:8080/api
- hey -n 5000 -c 20 -T application/json -d '{"x":1}' http://localhost:8080/api
- hey -t 10 -n 1000 http://localhost:8080/slow
