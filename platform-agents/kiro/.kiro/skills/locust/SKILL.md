---
name: "locust"
description: "Runs distributed load tests with Locust user classes, headless mode, HTML reports, and master/worker clusters. Use when working with locust runs, reporting, distributed mode, testing or when the user mentions locust runs, reporting, distributed mode, testing."
license: "MIT"
compatibility: "Requires locust."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(locust:*)"
---

Runs distributed load tests with Locust user classes, headless mode, HTML reports, and master/worker clusters.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `locust -f locustfile.py`, `locust --headless -u 100 -r 10 -t 1m --html report.html -f l`
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

# Locust

Python-based load testing with realistic user scenarios.

## What This Skill Does

- Defines user behaviors with HttpUser classes
- Runs headless with user ramps and durations
- Generates HTML and CSV reports
- Scales with master/worker clusters

## When to Use

- Scenario-based load tests with complex flows
- Distributed load generation
- Long-running soak tests

## Real Commands

```bash
# Local UI
locust -f locustfile.py

# Headless
locust --headless -u 100 -r 10 -t 30s -f locustfile.py
locust --headless -u 50 -r 5 --run-time 5m --host https://api.example.com

# Reports
locust --headless -u 100 -r 10 -t 1m --html report.html -f locustfile.py
locust --headless -u 100 -r 10 --csv stats -t 1m -f locustfile.py

# Distributed
locust --master -f locustfile.py
locust --worker --master-host=localhost -f locustfile.py
locust --master --expect-workers=4 -u 400 -r 40 -t 5m
```

## Sample Locustfile

```python
from locust import HttpUser, task, between

class CatalogUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def browse(self):
        self.client.get("/v1/products")

    @task(3)
    def view_product(self):
        self.client.get("/v1/products/42")
```

## Best Practices

- Weight tasks by real user frequency
- Ramp spawn rate gradually to observe degradation
- Keep scenarios deterministic for reproducibility
- Use distributed mode beyond a single machine's limits
- Export CSV/HTML for every run and archive them

## Capabilities

### locust-runs
Run Locust locally and headless.

**Parameters:**
- `file` (string): Locustfile path
- `users` (number): Peak number of users (-u)
- `spawnRate` (number): Users spawned per second (-r)

**Commands:**
- `locust -f locustfile.py`
- `locust --headless -u 100 -r 10 -t 30s -f locustfile.py`
- `locust -f locustfile.py --web-port 8090`
- `locust --headless -u 100 -r 10 --host http://localhost:8080`
- `locust --headless --users 50 --spawn-rate 5 --run-time 5m -f locustfile.py`

**Examples:**
- locust --headless -u 100 -r 10 -t 30s -f locustfile.py
- locust -f locustfile.py --web-port 8090
- locust --headless -u 50 -r 5 --run-time 5m -f locustfile.py

### reporting
Export HTML reports and stats.

**Parameters:**
- `html` (string): HTML report output path
- `csv` (string): CSV stats prefix

**Commands:**
- `locust --headless -u 100 -r 10 -t 1m --html report.html -f locustfile.py`
- `locust --headless -u 100 -r 10 --csv stats -t 1m -f locustfile.py`
- `locust --headless -u 100 -r 10 --csv-full-history --csv stats -t 2m -f locustfile.py`

**Examples:**
- locust --headless -u 100 -r 10 -t 1m --html report.html -f locustfile.py
- locust --headless -u 100 -r 10 --csv stats -t 1m -f locustfile.py

### distributed-mode
Run master/worker clusters.

**Parameters:**
- `masterHost` (string): Master host for workers
- `expectWorkers` (number): Workers to wait for before starting

**Commands:**
- `locust --master -f locustfile.py`
- `locust --worker --master-host=localhost -f locustfile.py`
- `locust --worker --master-host=10.0.0.5 --master-port=5557 -f locustfile.py`
- `locust --master --expect-workers=4 -u 400 -r 40 -t 5m -f locustfile.py`

**Examples:**
- locust --master -f locustfile.py
- locust --worker --master-host=localhost -f locustfile.py
- locust --master --expect-workers=4 -u 400 -r 40 -t 5m

## References
- [Locust Documentation](https://docs.locust.io/en/stable/)
- [Locust Quickstart](https://docs.locust.io/en/stable/quickstart.html)
