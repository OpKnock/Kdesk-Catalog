---
name: "Load Testing Scenario Profiles"
description: "Advanced load testing scenarios: k6 executors, vegeta histograms, distributed locust, and Gatling simulations for realistic workload profiles. Use when working with scenario profiles, distributed load, api or when the user mentions scenario profiles, distributed load, api."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Advanced load testing scenarios: k6 executors, vegeta histograms, distributed locust, and Gatling simulations for realistic workload profiles.

## Agentic Workflow: Read -> Reason -> Act (load-testing-scenario-profiles)

You are **Load Testing Scenario Profiles** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `load-testing-scenario-profiles`
- Domain: Advanced load testing scenarios: k6 executors, vegeta histograms, distributed locust, and Gatling simulations for realistic workload profiles.
- **scenario-profiles**: Run realistic profiles: spikes, soak, and arrival-rate tests. — `k6 run --scenario spike scenarios.js`
- **distributed-load**: Run distributed load with locust master/workers. — `locust -f locustfile.py --headless -u 500 -r 50 -t 3m --host https://httpbin.org`
- Check `knowledge` and `prerequisites: gatling.sh, locust, vegeta`

### 2. Reason — think for `load-testing-scenario-profiles`
- For `scenario-profiles`: Run realistic profiles: spikes, soak, and arrival-rate tests. — decide which checks to run
- For `distributed-load`: Run distributed load with locust master/workers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `load-testing-scenario-profiles` tools
- Tools: `Glob`, `Grep`, `Read`, `K6`, `Vegeta` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `load-testing-scenario-profiles:1e04c823`

# Load Testing (Advanced Scenarios)

Realistic workload profiles and distributed load generation.

## What this skill does

- Runs spike, soak, and arrival-rate scenarios with k6 executors.
- Builds latency histograms with vegeta.
- Distributes load across locust master/workers.

## When to use

- Validating autoscaling with spike patterns.
- Finding memory leaks with soak tests.
- Reproducing production traffic shapes.

## Real commands

```bash
# k6 scenario runs
k6 run --scenario spike scenarios.js
k6 run --scenario soak scenarios.js

# Vegeta histogram
vegeta attack -rate=50/1s -duration=2m -targets=targets.txt \
  | vegeta report -type=hist[0,50ms,100ms,200ms,500ms]

# Gatling simulation
gatling.sh -s simulations.SpikeSimulation

# Locust headless
locust -f locustfile.py --headless -u 500 -r 50 -t 3m \
  --host https://httpbin.org

# Distributed: master + workers
locust -f locustfile.py --master --master-bind-port=5557
locust -f locustfile.py --worker --master-host=10.0.0.10

# k6 with tight trend stats
k6 run --quiet --summary-trend-stats='avg,p(99.9)' soak.js
```

## k6 scenarios.js example

```js
export const options = {
  scenarios: {
    spike: {
      executor: 'constant-arrival-rate',
      duration: '2m',
      rate: 200,
      preAllocatedVUs: 50,
    },
    soak: {
      executor: 'ramping-vus',
      stages: [
        { duration: '5m', target: 100 },
        { duration: '55m', target: 100 },
        { duration: '5m', target: 0 },
      ],
    },
  },
  thresholds: { http_req_failed: ['rate<0.01'] },
};
```

## Testing

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 30s   # verify the file works
```

## Best practices

- Keep soak tests close to production hours with monitoring attached.
- Use arrival-rate executors when modeling real user concurrency.
- Record the exact profile (rate, duration, stages) with every result.

## Capabilities

### scenario-profiles
Run realistic profiles: spikes, soak, and arrival-rate tests.

**Parameters:**
- `scenario` (string): k6 scenario name (spike, soak, ramp).
- `rate` (string): Arrival rate like 50/1s.
- `simulation` (string): Gatling simulation class.

**Commands:**
- `k6 run --scenario spike scenarios.js`
- `k6 run --scenario soak scenarios.js`
- `vegeta attack -rate=50/1s -duration=2m -targets=targets.txt | vegeta report -type=hist[0,50ms,100ms,200ms,500ms]`
- `gatling.sh -s simulations.SpikeSimulation`

**Examples:**
- k6 run --scenario spike scenarios.js
- vegeta attack -rate=50/1s -duration=2m -targets=targets.txt | vegeta report -type=hist[0,50ms,100ms,200ms,500ms]
- gatling.sh -s simulations.SpikeSimulation

### distributed-load
Run distributed load with locust master/workers.

**Parameters:**
- `users` (integer): Total simulated users.
- `spawn_rate` (integer): Users spawned per second.
- `time` (string): Test duration, e.g. 3m.
- `master_host` (string): Locust master address for workers.

**Commands:**
- `locust -f locustfile.py --headless -u 500 -r 50 -t 3m --host https://httpbin.org`
- `locust -f locustfile.py --master --master-bind-port=5557`
- `locust -f locustfile.py --worker --master-host=10.0.0.10`
- `k6 run --quiet --summary-trend-stats='avg,p(99.9)' soak.js`

**Examples:**
- locust -f locustfile.py --headless -u 500 -r 50 -t 3m --host https://httpbin.org
- locust -f locustfile.py --worker --master-host=10.0.0.10
- k6 run --quiet --summary-trend-stats='avg,p(99.9)' soak.js

## References
- [k6 Executors](https://grafana.com/docs/k6/using-k6/scenarios/executors/)
- [Locust Docs](https://docs.locust.io/en/stable/)
- [Gatling Docs](https://docs.gatling.io/)