---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# Blue Green Deployment

Implements blue-green deployments on Kubernetes: parallel deployments, service cutover, rollback, and verification.

## Instructions

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
