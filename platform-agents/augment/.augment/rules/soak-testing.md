---
type: agent_requested
description: "Runs sustained load tests for 24+ hours using k6 while monitoring resource trends. Captures memory, CPU, and connection metrics from Kubernetes pods and host-level tools to detect leaks and drift that short tests miss. Use when working with soak run, api or when the user mentions soak run, api."
---

Runs sustained load tests for 24+ hours using k6 while monitoring resource trends. Captures memory, CPU, and connection metrics from Kubernetes pods and host-level tools to detect leaks and drift that short tests miss.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `k6 run --vus 10 --duration 24h soak.js`
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

# Soak Testing

Hand-crafted skill for endurance testing long-running services.

## What this skill does

- Sustains moderate load for hours to days with k6
- Watches memory, CPU, and connection trends
- Catches leaks and drift that short tests miss

## When to use

- Before a launch where the service will run 24/7
- Investigating memory growth after a release
- Verifying HPA can hold steady state under constant load

## Real commands

```bash
# 24-hour endurance run with 10 sustained users
k6 run --vus 10 --duration 24h soak.js

# Save results for trend analysis
k6 run --vus 10 --duration 24h soak.js --out json=soak.json

# Kubernetes resource trend
kubectl top pods -l app=api -n prod

# Host-level watch
free -h && vmstat 1 10
dstat -tcdmn 10

# Autoscaling behavior
kubectl get hpa api
```

## k6 script

```javascript
export const options = {
  stages: [
    { duration: "1h", target: 10 },   // ramp
    { duration: "22h", target: 10 },  // plateau
    { duration: "1h", target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
  },
};

export default function () {
  http.get("http://localhost:8080/api/v1/users");
}
```

## Testing

```bash
k6 run --vus 10 --duration 30m soak.js --out json=short-soak.json
kubectl top pods -n prod | sort -k2 -h
```

## Best practices

- Check memory growth: RSS should plateau, never climb linearly
- Capture k6 JSON output and pod metrics at the same interval
- A 24h run is the minimum for leak confidence

## Capabilities

### soak-run
Runs sustained load tests for 24+ hours using k6 while monitoring resource trends. Captures memory, CPU, and connection metrics from Kubernetes pods and host-level tools to detect leaks and drift that short tests miss.

**Parameters:**
- `vus` (integer): Number of virtual users for sustained load
- `duration` (string): Test duration (e.g., 24h, 48h)
- `script_path` (string): Path to k6 test script

**Commands:**
- `k6 run --vus 10 --duration 24h soak.js`
- `k6 run --vus 10 --duration 24h soak.js --out json=soak.json`
- `kubectl top pods -l app=api -n prod`
- `free -h`
- `vmstat 1 10`
- `dstat -tcdmn 10`
- `kubectl get hpa api`

**Examples:**
- k6 run --vus 10 --duration 24h soak.js
- k6 run --vus 10 --duration 24h soak.js --out json=soak.json
- kubectl top pods -l app=api -n prod
- free -h && vmstat 1 10
- kubectl get hpa api

## References
- [k6 soak testing guide](https://grafana.com/docs/k6/latest/testing-guides/test-types/soak-testing/)