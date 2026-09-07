---
type: agent_requested
description: "Load testing with Locust: HttpUser task files, headless runs, web UI, CSV collection, and distributed execution for large-scale tests. Use when working with locust run, locust output, api or when the user mentions locust run, locust output, api."
---

Load testing with Locust: HttpUser task files, headless runs, web UI, CSV collection, and distributed execution for large-scale tests.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `locust -f locustfile.py --headless -u 1000 -r 100 --host htt`, `locust -f locustfile.py --headless -u 500 -r 50 --csv=result`
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

Load test with Python-defined user behavior.

## What this skill does

- Runs Locust with HttpUser task classes.
- Executes headless or interactive web UI runs.
- Exports CSV stats and distributes load with master/workers.

## When to use

- Simulating realistic user journeys (login, browse, checkout).
- Tests that need Python logic in the workload.
- Distributed load generation from many machines.

## Real commands

```bash
# Headless: 1000 users, spawn 100/s, 10 minutes
locust -f locustfile.py --headless -u 1000 -r 100 -t 10m \
  --host https://httpbin.org

# Web UI mode (http://localhost:8089)
locust -f locustfile.py
locust -f locustfile.py --web-port 8089

# CSV with full history
locust -f locustfile.py --headless -u 500 -r 50 \
  --csv=results --csv-full-history -t 5m

# Distributed
locust -f locustfile.py --master --master-bind-port=5557
locust -f locustfile.py --worker --master-host=10.0.0.10
```

## locustfile.py example

```python
from locust import HttpUser, task, between

class CheckoutUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def browse(self):
        self.client.get("/products")

    @task(1)
    def checkout(self):
        self.client.post("/api/orders", json={"product_id": 7, "qty": 2})
```

## Testing

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 30s   # smoke run
```

## Best practices

- Weight tasks with @task(n) to model realistic ratios.
- Use wait_time between requests; instant requests aren't realistic.
- In distributed mode, scale workers until the master's CPU stays under load.

## Capabilities

### locust-run
Run locust tests headless or with the web UI.

**Parameters:**
- `file` (string): Locustfile path.
- `users` (integer): Peak number of users (-u).
- `spawn_rate` (integer): Users spawned per second (-r).
- `time` (string): Stop time, e.g. 2m (-t).

**Commands:**
- `locust -f locustfile.py --headless -u 1000 -r 100 --host https://httpbin.org`
- `locust -f locustfile.py`
- `locust -f locustfile.py --web-port 8089`
- `locust -f locustfile.py --headless -u 200 -r 20 -t 2m`

**Examples:**
- locust -f locustfile.py --headless -u 1000 -r 100 --host https://httpbin.org
- locust -f locustfile.py
- locust -f locustfile.py --headless -u 200 -r 20 -t 2m

### locust-output
Collect CSV results and run distributed tests.

**Parameters:**
- `csv` (string): CSV output prefix.
- `csv_full_history` (boolean): Log every stats sample, not just final.
- `master_bind_port` (integer): Master port, default 5557.

**Commands:**
- `locust -f locustfile.py --headless -u 500 -r 50 --csv=results --csv-full-history -t 5m`
- `locust -f locustfile.py --master --master-bind-port=5557 --csv=dist-results`
- `locust -f locustfile.py --worker --master-host=10.0.0.10`
- `ls results_*.csv`

**Examples:**
- locust -f locustfile.py --headless -u 500 -r 50 --csv=results --csv-full-history -t 5m
- locust -f locustfile.py --worker --master-host=10.0.0.10
- ls results_*.csv

## References
- [Locust Documentation](https://docs.locust.io/en/stable/)
- [Locust Running Distributed](https://docs.locust.io/en/stable/running-distributed.html)