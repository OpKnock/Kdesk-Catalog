---
trigger: glob
description: "General HTTP load testing with ab, wrk, hey, vegeta, and jmeter: quick benchmarks, target files, and baseline reports. Use when working with quick bench, vegeta jmeter, api or when the user mentions quick bench, vegeta jmeter, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

General HTTP load testing with ab, wrk, hey, vegeta, and jmeter: quick benchmarks, target files, and baseline reports.

## Agentic Workflow: Read -> Reason -> Act (load-testing)

You are **Load Testing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `load-testing`
- Domain: General HTTP load testing with ab, wrk, hey, vegeta, and jmeter: quick benchmarks, target files, and baseline reports.
- **quick-bench**: Run quick benchmarks with ab, wrk, and hey. — `ab -n 1000 -c 50 http://localhost:8080/`
- **vegeta-jmeter**: Run scripted attacks with vegeta and JMeter plans. — `vegeta attack -duration=30s -rate=100 -targets=api-targets.txt | vegeta report`
- Check `knowledge` and `prerequisites: hey, jmeter, vegeta, wrk`

### 2. Reason — think for `load-testing`
- For `quick-bench`: Run quick benchmarks with ab, wrk, and hey. — decide which checks to run
- For `vegeta-jmeter`: Run scripted attacks with vegeta and JMeter plans. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `load-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Ab`, `Wrk` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `load-testing:100aedb4`

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

**Parameters:**
- `url` (string): Target URL.
- `requests` (integer): Total requests (ab/hey).
- `concurrency` (integer): Concurrent connections.
- `duration` (string): Duration for wrk, e.g. 30s.

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

**Parameters:**
- `rate` (integer): Requests per second (vegeta).
- `targets` (string): Vegeta targets file (e.g., api-targets.txt).
- `jmx` (string): JMeter plan file (e.g., test-plan.jmx).

**Commands:**
- `vegeta attack -duration=30s -rate=100 -targets=api-targets.txt | vegeta report`
- `vegeta attack -targets=api-targets.txt -duration=1m | vegeta report -type=json > report.json`
- `jmeter -n -t test-plan.jmx -l results.jtl -Jthreads=50`
- `cat results.bin | vegeta report -type=hist[0,100ms,200ms,500ms]`

**Examples:**
- vegeta attack -duration=30s -rate=100 -targets=api-targets.txt | vegeta report
- jmeter -n -t test-plan.jmx -l results.jtl -Jthreads=50
- cat results.bin | vegeta report -type=hist[0,100ms,200ms,500ms]

## References
- [Vegeta](https://github.com/tsenart/vegeta)
- [Apache Bench](https://httpd.apache.org/docs/2.4/programs/ab.html)
- [wrk](https://github.com/wg/wrk)
