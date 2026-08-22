---
name: "Stress Testing"
description: "Push APIs to their limits with ab, wrk, hey, siege, and k6. Generates sustained load, reports throughput and latency percentiles, and identifies breaking points before users encounter them. Use for capacity planning, autoscaling verification, and reproducing concurrency issues."
globs: ["**/*.java", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
alwaysApply: false
---

# Stress Testing

Push APIs to their limits with ab, wrk, hey, siege, and k6. Generates sustained load, reports throughput and latency percentiles, and identifies breaking points before users encounter them. Use for capacity planning, autoscaling verification, and reproducing concurrency issues.

## Instructions

# Stress Testing

Hand-crafted skill for pushing APIs to their limits.

## What this skill does

- Generates sustained load with ab, wrk, hey, siege, and k6
- Reports throughput, latency percentiles, and failure counts
- Finds the breaking point before users do

## When to use

- Capacity planning before a launch
- Verifying autoscaling kicks in
- Reproducing latency issues under concurrency

## Real commands

```bash
# ApacheBench: 10k requests, 100 concurrent, keep-alive
ab -n 10000 -c 100 -k http://localhost:8080/api/v1/users

# wrk: 4 threads, 100 connections, 30s
wrk -t4 -c100 -d30s http://localhost:8080/api/v1/users

# hey: 60s with 200 concurrent
hey -z 60s -c 200 http://localhost:8080/api/v1/users

# k6 with thresholds
k6 run --vus 50 --duration 2m stress.js

# siege: 100 concurrent for 60s
siege -c 100 -t 60s http://localhost:8080/api/v1/users
```

## Reading results

- Requests per second vs concurrency: find the knee
- Failed requests and socket timeouts indicate the ceiling
- Watch server CPU/mem during the run: kubectl top or top

## k6 thresholds

```javascript
export const options = {
  vus: 50,
  duration: "2m",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<800"],
  },
};
```

## Testing

```bash
ab -n 5000 -c 50 -k http://localhost:8080/health
hey -z 30s -c 100 http://localhost:8080/api/v1/users
```

## Best practices

- Warm up before measuring; cold caches skew results
- Ramp concurrency in steps and record each plateau
- Never stress production: use staging with identical sizing

## Capabilities

### load-generation
Stress APIs with ab, wrk, hey, siege, and k6

**Commands:**
- `ab -n 10000 -c 100 -k http://localhost:8080/api/v1/users`
- `wrk -t4 -c100 -d30s http://localhost:8080/api/v1/users`
- `hey -z 60s -c 200 http://localhost:8080/api/v1/users`
- `k6 run --vus 50 --duration 2m stress.js`
- `siege -c 100 -t 60s http://localhost:8080/api/v1/users`

**Examples:**
- ab -n 10000 -c 100 -k http://localhost:8080/api/v1/users
- wrk -t4 -c100 -d30s http://localhost:8080/api/v1/users
- k6 run --vus 50 --duration 2m stress.js