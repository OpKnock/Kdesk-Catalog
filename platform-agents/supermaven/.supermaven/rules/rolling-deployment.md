# Rolling Deployment

Expert Kubernetes rolling deployment skill covering set image, rollout status/history, undo, pause/resume, and canary verification with kubectl.

## Instructions

# Rolling Deployment

Expert skill for safe Kubernetes rolling deployments.

## What this skill does

- Swaps container images on a Deployment with zero downtime
- Watches rollout progress and knows when it is complete or failed
- Rolls back instantly to a known-good revision

## When to use

- Shipping a new API version without downtime
- Recovering from a bad release quickly
- Validating progressive rollouts with pause/resume

## Real commands

```bash
# Update the image (triggers a new ReplicaSet)
kubectl set image deployment/api api=ghcr.io/your-org/api:v2.1

# Wait until the rollout completes or times out
kubectl rollout status deployment/api --timeout=180s

# Review revision history with images
kubectl rollout history deployment/api
kubectl rollout history deployment/api --revision=3

# Roll back (latest by default, or pick a revision)
kubectl rollout undo deployment/api
kubectl rollout undo deployment/api --to-revision=3

# Canary-style: pause, verify, resume
kubectl rollout pause deployment/api
kubectl get pods -l app=api -w
kubectl rollout resume deployment/api
```

## Deployment strategy

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

## Testing

```bash
kubectl rollout status deployment/api --timeout=180s
kubectl get replicasets -l app=api
kubectl get pods -l app=api -w
```

## Best practices

- Set maxUnavailable: 0 to keep capacity during the swap
- Verify readinessProbes before the new pods take traffic
- Have a rollback runbook: one kubectl rollout undo away

## Capabilities

### k8s-rolling-deploy
Roll out and roll back Kubernetes Deployments safely

**Commands:**
- `kubectl set image deployment/api api=ghcr.io/your-org/api:v2.1`
- `kubectl rollout status deployment/api --timeout=180s`
- `kubectl rollout history deployment/api`
- `kubectl rollout undo deployment/api`
- `kubectl rollout pause deployment/api`
- `kubectl rollout resume deployment/api`

**Examples:**
- kubectl rollout status deployment/api --timeout=180s
- kubectl rollout undo deployment/api --to-revision=3
- kubectl get pods -l app=api -w