---
trigger: glob
description: "Implements blue-green deployments on Kubernetes: parallel deployments, service cutover, rollback, and verification. Use when working with deploy flow, traffic switch, rollback verify, api or when the user mentions deploy flow, traffic switch, rollback verify, api."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Implements blue-green deployments on Kubernetes: parallel deployments, service cutover, rollback, and verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl apply -f app-blue.yaml`, `kubectl patch service my-api -p '{"spec":{"selector":{"versi`
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

# Blue-Green Deployment

## What this skill does

Implements blue-green deployments on Kubernetes: running two full deployments (blue/green), switching the service selector to cut traffic, verifying the active color, and rolling back by flipping the selector again.

## When to use

- Zero-downtime releases with instant rollback
- Deploying versions that cannot be mixed
- Compliance-driven 'keep old version ready until verified'

## Real commands

```bash
# Deploy both colors
kubectl apply -f app-blue.yaml
kubectl apply -f app-green.yaml
kubectl rollout status deployment/my-api-blue

# Switch traffic to green
kubectl patch service my-api -p '{"spec":{"selector":{"version":"green"}}}'

# Verify endpoints flipped
kubectl get endpoints my-api
kubectl get svc my-api -o wide

# Smoke test
curl -s http://localhost:8080/version

# Rollback: flip back to blue
kubectl patch service my-api -p '{"spec":{"selector":{"version":"blue"}}}'
```

## Manifests

Deployments differ only by `version: blue` vs `version: green` labels; the Service selector points at the active one.

## Testing

- After switch, assert endpoints contain only green pod IPs
- Run smoke tests against the service during the switch window

## Best practices

- Keep both colors resource-budgeted so switchover is instant
- Automate the selector patch in the release pipeline
- After a soak period, scale down the old color or delete it

## Capabilities

### deploy-flow
Deploy blue/green versions and switch traffic.

**Parameters:**
- `version` (string): blue or green
- `manifest` (string): Deployment manifest path

**Commands:**
- `kubectl apply -f app-blue.yaml`
- `kubectl apply -f app-green.yaml`
- `kubectl rollout status deployment/my-api-blue`
- `kubectl get deployments -l app=my-api`
- `kubectl get pods -l version=green`

**Examples:**
- kubectl apply -f app-blue.yaml && kubectl rollout status deployment/my-api-blue --timeout=300s
- kubectl get pods -l version=green -o wide
- kubectl describe deployment my-api-green | grep -E 'Replicas|Ready'

### traffic-switch
Point the service selector at the active version.

**Parameters:**
- `service` (string): Service name
- `selector` (string): Label selector value, e.g. version=green

**Commands:**
- `kubectl patch service my-api -p '{"spec":{"selector":{"version":"green"}}}'`
- `kubectl get endpoints my-api`
- `kubectl get svc my-api -o wide`
- `kubectl rollout undo deployment/my-api-blue`
- `curl -s http://localhost:8080/version`

**Examples:**
- kubectl patch service my-api -p '{"spec":{"selector":{"version":"green"}}}' && kubectl get endpoints my-api
- kubectl patch service my-api -p '{"spec":{"selector":{"version":"blue"}}}'
- kubectl get endpoints my-api -o jsonpath='{.subsets[*].addresses[*].ip}'

### rollback-verify
Roll back to the previous color and verify.

**Parameters:**
- `deployment` (string): Deployment name
- `replicas` (number): Scale count

**Commands:**
- `kubectl rollout status deployment/my-api-green`
- `kubectl logs -l version=green --tail=50`
- `kubectl get events --sort-by=.lastTimestamp | tail -20`
- `kubectl scale deployment my-api-blue --replicas=0`
- `kubectl get pods -l version=green -o wide --field-selector status.phase=Running`

**Examples:**
- kubectl rollout status deployment/my-api-green && kubectl logs -l version=green --tail=50
- kubectl scale deployment my-api-blue --replicas=0
- kubectl get pods -l version=blue -o wide

## References
- [Blue Green Deployment (Martin Fowler)](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
