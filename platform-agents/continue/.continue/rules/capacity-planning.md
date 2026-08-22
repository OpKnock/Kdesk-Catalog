---
name: "capacity-planning"
description: "Plans infrastructure capacity: load testing, headroom analysis, autoscaling rules, and cost-aware sizing for services."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# capacity-planning

Plans infrastructure capacity: load testing, headroom analysis, autoscaling rules, and cost-aware sizing for services.

## Instructions

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