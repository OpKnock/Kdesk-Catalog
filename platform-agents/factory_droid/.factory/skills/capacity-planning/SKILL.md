---
name: "capacity-planning"
description: "Plans infrastructure capacity: load testing, headroom analysis, autoscaling rules, and cost-aware sizing for services. Use when working with load testing, sizing analysis or when the user mentions load testing, sizing analysis."
license: "MIT"
compatibility: "Requires prometheus, grafana, aws, terraform, kubernetes. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "sre"}
allowed-tools: "Glob Grep Read Bash(ab:*) Bash(docker:*) Bash(hey:*) Bash(k6:*) Bash(kubectl:*) Bash(psutil::*) Bash(wrk:*)"
---

Plans infrastructure capacity: load testing, headroom analysis, autoscaling rules, and cost-aware sizing for services.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ab -n 10000 -c 100 http://localhost:8000/api`, `kubectl top pod -l app=myapp`
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

# Capacity Planning

Size infrastructure for real load, not guesses.

## When to Use

- Before major launches or traffic campaigns
- When p95 latency degrades under expected peak
- Right-sizing costs in cloud budgets
- Validating autoscaling rules

## Method

1. Baseline current usage (RPS, p95 latency, CPU, memory)
2. Load test 1x, 2x, 5x expected peak
3. Find the saturation point per instance
4. Add headroom: 2x peak for steady services
5. Set autoscaling thresholds from real numbers

## Commands

```bash
# Load generation
ab -n 10000 -c 100 http://localhost:8000/api
wrk -t4 -c200 -d30s http://localhost:8000/api
hey -n 5000 -c 50 http://localhost:8000/api
k6 run --vus 100 --duration 5m load-test.js

# Current utilization
kubectl top pod -l app=myapp
kubectl top node
kubectl get hpa myapp
docker stats --no-stream
```

## HPA Example

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```

## Best Practices

- Test at 2-3x expected peak with realistic request mixes
- Watch p95 latency, not just throughput
- Plan for failure of one instance, zone, or region
- Pre-scale before known events, autoscale during them
- Revisit numbers quarterly; traffic changes fast

## Capabilities

### load-testing
Generate load and measure service capacity.

**Parameters:**
- `concurrency` (integer): Concurrent connections
- `requests` (integer): Total requests
- `duration` (string): Test duration

**Commands:**
- `ab -n 10000 -c 100 http://localhost:8000/api`
- `wrk -t4 -c200 -d30s http://localhost:8000/api`
- `k6 run load-test.js`
- `hey -n 5000 -c 50 http://localhost:8000/api`

**Examples:**
- wrk -t8 -c400 -d60s -s latency.lua http://localhost:8000/
- k6 run --vus 100 --duration 5m load-test.js
- ab -n 10000 -c 100 -k http://localhost:8000/api

### sizing-analysis
Analyze headroom and set scaling rules.

**Parameters:**
- `target-utilization` (integer): HPA target %
- `metric` (string): cpu, memory, or latency

**Commands:**
- `kubectl top pod -l app=myapp`
- `kubectl top node`
- `kubectl get hpa myapp`
- `docker stats --no-stream`
- `psutil: python -c "import psutil; print(psutil.cpu_percent(interval=1))"`

**Examples:**
- kubectl top pod -l app=myapp --containers
- kubectl get hpa myapp -o yaml | grep -A5 spec
- docker stats $(docker ps -q) --no-stream

## References
- [k6 Docs](https://grafana.com/docs/k6/latest/)
- [HPA Docs](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
