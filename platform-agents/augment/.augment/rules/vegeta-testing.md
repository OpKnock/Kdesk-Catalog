---
type: agent_requested
description: "Load-tests HTTP endpoints with Vegeta attack/plot/report pipelines and encoded result files. Use when working with vegeta attacks, vegeta reports, vegeta plots, testing or when the user mentions vegeta attacks, vegeta reports, vegeta plots, testing."
---

Load-tests HTTP endpoints with Vegeta attack/plot/report pipelines and encoded result files.

## Agentic Workflow: Read -> Reason -> Act (vegeta-testing)

You are **vegeta-testing** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `vegeta-testing`
- Domain: Load-tests HTTP endpoints with Vegeta attack/plot/report pipelines and encoded result files.
- **vegeta-attacks**: Generate load with targets and rate controls. — `echo 'GET http://localhost:8080' | vegeta attack -duration=30s -rate=100 > resul`
- **vegeta-reports**: Report metrics and histograms from results. — `vegeta report results.bin`
- **vegeta-plots**: Generate latency plots and encode results. — `vegeta plot results.bin > plot.html`
- Check `knowledge` and `prerequisites: echo, vegeta`

### 2. Reason — think for `vegeta-testing`
- For `vegeta-attacks`: Generate load with targets and rate controls. — decide which checks to run
- For `vegeta-reports`: Report metrics and histograms from results. — decide which checks to run
- For `vegeta-plots`: Generate latency plots and encode results. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `vegeta-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Echo`, `Vegeta` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `vegeta-testing:fb778498`

# Vegeta

HTTP load testing with a composable pipeline.

## What This Skill Does

- Generates fixed-rate load with attack
- Reports percentiles and histograms
- Plots latency over time to HTML
- Encodes results for further analysis

## When to Use

- Throughput and latency benchmarking
- Comparing releases under identical load
- Capacity checks with exact rates

## Real Commands

```bash
# Attack
echo 'GET http://localhost:8080' | vegeta attack -duration=30s -rate=100 > results.bin
vegeta attack -targets=targets.txt -rate=200 -duration=2m > results.bin

# Report
vegeta report results.bin
vegeta report -type=hist[0,100ms,200ms,300ms] results.bin
vegeta report -type=json results.bin

# Plot and encode
vegeta plot results.bin > plot.html
vegeta encode -format=json < results.bin | jq .
```

## Targets File

```text
GET http://localhost:8080/products
POST http://localhost:8080/api/orders
Content-Type: application/json

{"sku": "A-1", "qty": 2}
```

## Best Practices

- Keep results.bin as the single source of truth
- Use histogram reports for latency distribution
- Attack with -rate=0 for unconstrained throughput tests
- Compare plots across releases for regressions
- Script the full pipeline into CI on staging

## Capabilities

### vegeta-attacks
Generate load with targets and rate controls.

**Parameters:**
- `rate` (number): Requests per second
- `duration` (string): Attack duration
- `targets` (string): Targets file path

**Commands:**
- `echo 'GET http://localhost:8080' | vegeta attack -duration=30s -rate=100 > results.bin`
- `echo 'POST http://localhost:8080/api' | vegeta attack -duration=1m -rate=50 -body post.json -header 'Content-Type: application/json' > results.bin`
- `vegeta attack -targets=targets.txt -rate=200 -duration=2m > results.bin`
- `echo 'GET http://localhost:8080/health' | vegeta attack -rate=0 -max-workers=20 -duration=30s > results.bin`

**Examples:**
- echo 'GET http://localhost:8080' | vegeta attack -duration=30s -rate=100 > results.bin
- vegeta attack -targets=targets.txt -rate=200 -duration=2m > results.bin
- echo 'POST http://localhost:8080/api' | vegeta attack -duration=1m -rate=50 -body post.json > results.bin

### vegeta-reports
Report metrics and histograms from results.

**Parameters:**
- `type` (string): Report type: text, json, hist
- `every` (string): Periodic report interval

**Commands:**
- `vegeta report results.bin`
- `vegeta report -type=hist[0,100ms,200ms,300ms] results.bin`
- `vegeta report -type=json results.bin`
- `vegeta report -every=10s results.bin`

**Examples:**
- vegeta report results.bin
- vegeta report -type=hist[0,100ms,200ms,300ms] results.bin
- vegeta report -type=json results.bin

### vegeta-plots
Generate latency plots and encode results.

**Parameters:**
- `format` (string): Encode format: json, gob, csv
- `title` (string): Plot title

**Commands:**
- `vegeta plot results.bin > plot.html`
- `vegeta encode -format=json < results.bin | jq .`
- `vegeta encode -format=gob demo-results-bin results.gob`
- `vegeta plot -title="Release 1.2" results.bin > release.html`

**Examples:**
- vegeta plot results.bin > plot.html
- vegeta encode -format=json < results.bin | jq .
- vegeta plot -title="Release 1.2" results.bin > release.html

## References
- [Vegeta GitHub](https://github.com/tsenart/vegeta)
- [Vegeta Docs](https://github.com/tsenart/vegeta/tree/master/docs)