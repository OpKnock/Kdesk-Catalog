---
name: "Fortio"
description: "Load testing with Fortio: run HTTP load tests, generate reports, and inspect latency percentiles and errors from the CLI."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Fortio

Load testing with Fortio: run HTTP load tests, generate reports, and inspect latency percentiles and errors from the CLI.

## Instructions

# Fortio

## What this skill does

Fortio is Istio's load testing tool: it runs HTTP/HTTPS/gRPC load tests with precise rate control, collects latency histograms, and writes JSON reports.

## When to use

- Validating SLOs under controlled QPS
- Comparing latency across service versions
- Pre-launch capacity checks

## Real commands

```bash
# Fixed rate test: 50 conns, 500 qps, 30s
fortio load -c 50 -t 30s -qps 500 http://localhost:8080/api/orders

# Max throughput (no rate cap)
fortio load -c 10 -n 1000 -httpbuffered=false http://localhost:8080/health

# With headers
fortio load -H 'Authorization: Bearer token' -c 20 -t 10s http://localhost:8080/api/orders/1

# JSON report for CI
fortio load -c 50 -t 60s -json result.json http://localhost:8080/

# Browse the last report
fortio report
```

## Reading the report

```bash
fortio load -c 50 -t 60s -json result.json http://localhost:8080/ | jq '{qps: .ActualQPS, p50: .DurationHistogram.Percentiles[0].Value, p99: .DurationHistogram.Percentiles[4].Value, errors: .RetCodes}'
```

## Best practices

- Use `-qps` to test at the expected production rate; unthrottled only for max-capacity runs.
- Save `-json` reports and diff percentiles across releases.
- Run a warmup burst (short -n) before timed runs.
- Watch both P99 and error codes; a low P99 with 5xx is still failure.
- Use `-httpbuffered=false` for latency-sensitive keep-alive workloads.

## Capabilities

### fortio-load
Run HTTP load tests with configurable rate, connections, and duration.

**Commands:**
- `fortio load -c 50 -t 30s -qps 500 http://localhost:8080/api/orders`
- `fortio load -c 10 -n 1000 -httpbuffered=false http://localhost:8080/health`
- `fortio load -H 'Authorization: Bearer token' -c 20 -t 10s http://localhost:8080/api/orders/1`
- `fortio report`
- `fortio load -c 50 -t 60s -json result.json http://localhost:8080/ | jq '.DurationHistogram.Percentiles'`

**Examples:**
- fortio load -c 50 -t 30s -qps 500 http://localhost:8080/api/orders
- fortio load -c 50 -t 60s -json result.json http://localhost:8080/ | jq '.DurationHistogram.Percentiles'
- fortio report