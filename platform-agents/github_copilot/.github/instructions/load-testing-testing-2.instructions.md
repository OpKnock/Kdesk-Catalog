---
applyTo: "**/*.r **/*.sh"
---

# load-testing-testing-2

Load-tests HTTP services with hey, ApacheBench, and wrk for quick throughput and latency measurements.

## Instructions

# Load Testing

Quick, reproducible load tests with lightweight CLI tools.

## What This Skill Does

- Generates high concurrency with hey, ab, and wrk
- Measures throughput, latency, and error rates
- Compares results against baselines
- Tests with headers, methods, and payloads

## When to Use

- Sanity-checking capacity before releases
- Comparing performance between versions
- Verifying config changes under load

## Real Commands

```bash
# hey
hey -n 10000 -c 100 https://api.example.com/v1/users
hey -z 30s -c 50 -m POST -d '{"q":"x"}' https://api.example.com/v1/search

# ApacheBench
ab -n 10000 -c 100 -k https://api.example.com/v1/health

# wrk
wrk -t4 -c100 -d30s https://api.example.com/v1/users

# Baseline comparison
wrk -t4 -c100 -d30s https://api.example.com/v1/users > baseline.txt
wrk -t4 -c100 -d30s https://api.example.com/v1/users | grep -E 'Requests/sec|Latency'
```

## Reading Results

- Requests/sec: throughput under the given concurrency
- Latency distribution: p50/p90/p99 skew reveals tail latency
- Non-2xx responses: error rate under load
- Connection timeouts at high concurrency indicate pool exhaustion

## Best Practices

- Warm up the service before measuring
- Use keep-alive (-k) for realistic HTTP/1.1 behavior
- Test both small and payload-heavy requests
- Record baselines per release for regression detection
- Never load-test production without authorization

## Capabilities

### quick-load-tools
Generate load with hey, ab, and wrk.

**Commands:**
- `hey -n 10000 -c 100 http://localhost:8080/v1/users`
- `ab -n 10000 -c 100 http://localhost:8080/v1/users`
- `wrk -t4 -c100 -d30s http://localhost:8080/v1/users`
- `hey -z 30s -c 50 -m POST -d '{"q":"x"}' http://localhost:8080/v1/search`
- `ab -n 5000 -c 50 -k http://localhost:8080/v1/health`

**Examples:**
- hey -n 10000 -c 100 http://localhost:8080/v1/users
- ab -n 10000 -c 100 -k http://localhost:8080/v1/health
- wrk -t4 -c100 -d30s http://localhost:8080/v1/users

### result-analysis
Parse and compare load-test results.

**Commands:**
- `hey -n 1000 -c 50 http://localhost:8080/v1/users | grep -E 'Requests|Total|Average|p99'`
- `wrk -t4 -c100 -d30s http://localhost:8080/v1/users > baseline.txt`
- `diff <(wrk -t4 -c100 -d30s http://localhost:8080/v1/users) baseline.txt`
- `hey -n 1000 -c 50 -disable-compression http://localhost:8080/v1/users | grep 'status code'`

**Examples:**
- hey -n 1000 -c 50 http://localhost:8080/v1/users | grep -E 'Average|p99'
- wrk -t4 -c100 -d30s http://localhost:8080/v1/users > baseline.txt
- diff <(wrk -t4 -c100 -d30s http://localhost:8080/v1/users) baseline.txt
