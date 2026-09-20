---
name: "load-testing-scenario-profiles"
description: "Advanced load testing scenarios: k6 executors, vegeta histograms, distributed locust, and Gatling simulations for realistic workload profiles."
---

# Load Testing Scenario Profiles

Advanced load testing scenarios: k6 executors, vegeta histograms, distributed locust, and Gatling simulations for realistic workload profiles.

## Instructions

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

**Commands:**
- `locust -f locustfile.py --headless -u 500 -r 50 -t 3m --host https://httpbin.org`
- `locust -f locustfile.py --master --master-bind-port=5557`
- `locust -f locustfile.py --worker --master-host=10.0.0.10`
- `k6 run --quiet --summary-trend-stats='avg,p(99.9)' soak.js`

**Examples:**
- locust -f locustfile.py --headless -u 500 -r 50 -t 3m --host https://httpbin.org
- locust -f locustfile.py --worker --master-host=10.0.0.10
- k6 run --quiet --summary-trend-stats='avg,p(99.9)' soak.js
