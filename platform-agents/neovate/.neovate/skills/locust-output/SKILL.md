---
name: "locust-output"
description: "Load testing with Locust: HttpUser task files, headless runs, web UI, CSV collection, and distributed execution for large-scale tests."
---

# Locust Output

Load testing with Locust: HttpUser task files, headless runs, web UI, CSV collection, and distributed execution for large-scale tests.

## Instructions

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

**Commands:**
- `locust -f locustfile.py --headless -u 500 -r 50 --csv=results --csv-full-history -t 5m`
- `locust -f locustfile.py --master --master-bind-port=5557 --csv=dist-results`
- `locust -f locustfile.py --worker --master-host=10.0.0.10`
- `ls results_*.csv`

**Examples:**
- locust -f locustfile.py --headless -u 500 -r 50 --csv=results --csv-full-history -t 5m
- locust -f locustfile.py --worker --master-host=10.0.0.10
- ls results_*.csv
