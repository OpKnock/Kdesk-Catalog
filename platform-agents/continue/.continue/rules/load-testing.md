---
name: "Load Testing"
description: "General HTTP load testing with ab, wrk, hey, vegeta, and jmeter: quick benchmarks, target files, and baseline reports."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Load Testing

General HTTP load testing with ab, wrk, hey, vegeta, and jmeter: quick benchmarks, target files, and baseline reports.

## Instructions

# Load Testing (General)

Benchmark HTTP services with the standard load testing toolkit.

## What this skill does

- Runs quick benchmarks with ab, wrk, and hey.
- Runs scripted attacks with vegeta and JMeter.
- Produces baseline reports for later comparisons.

## When to use

- Smoke benchmarks after deployments.
- Capacity baselining before tuning.
- Choosing the right tool for a scenario.

## Real commands

```bash
# ab: 1000 requests, 50 concurrent
ab -n 1000 -c 50 http://localhost:8080/

# ab keep-alive with header
ab -n 1000 -c 50 -k -H 'Accept: application/json' http://localhost:8080/api

# wrk: 8 threads, 200 connections, 30s
wrk -t8 -c200 -d30s http://localhost:8080/

# hey: 10k requests, 200 workers
hey -n 10000 -c 200 http://localhost:8080/

# vegeta: 100 rps for 30s
echo 'GET http://localhost:8080/' | vegeta attack -duration=30s -rate=100 | vegeta report

# vegeta from targets file
vegeta attack -duration=1m -rate=100 -targets=api-targets.txt | vegeta report -type=json > report.json

# JMeter non-GUI
jmeter -n -t test-plan.jmx -l results.jtl -Jthreads=50

# Histogram from binary results
cat results.bin | vegeta report -type=hist[0,100ms,200ms,500ms]
```

## api-targets.txt example

```text
GET http://localhost:8080/
POST http://localhost:8080/api/orders
Content-Type: application/json

{"id":1}
```

## Testing

```bash
hey -n 100 -c 10 http://localhost:8080/healthz   # smoke before the real run
```

## Best practices

- Warm up the service before measuring; first requests skew results.
- Record the exact command+flags with results for reproducibility.
- Use keep-alive for realistic persistent connections.

## Capabilities

### quick-bench
Run quick benchmarks with ab, wrk, and hey.

**Commands:**
- `ab -n 1000 -c 50 http://localhost:8080/`
- `wrk -t8 -c200 -d30s http://localhost:8080/`
- `hey -n 10000 -c 200 http://localhost:8080/`
- `ab -n 1000 -c 50 -k -H 'Accept: application/json' http://localhost:8080/api`

**Examples:**
- ab -n 1000 -c 50 http://localhost:8080/
- wrk -t8 -c200 -d30s http://localhost:8080/
- hey -n 10000 -c 200 http://localhost:8080/

### vegeta-jmeter
Run scripted attacks with vegeta and JMeter plans.

**Commands:**
- `vegeta attack -duration=30s -rate=100 -targets=api-targets.txt | vegeta report`
- `vegeta attack -targets=api-targets.txt -duration=1m | vegeta report -type=json > report.json`
- `jmeter -n -t test-plan.jmx -l results.jtl -Jthreads=50`
- `cat results.bin | vegeta report -type=hist[0,100ms,200ms,500ms]`

**Examples:**
- vegeta attack -duration=30s -rate=100 -targets=api-targets.txt | vegeta report
- jmeter -n -t test-plan.jmx -l results.jtl -Jthreads=50
- cat results.bin | vegeta report -type=hist[0,100ms,200ms,500ms]