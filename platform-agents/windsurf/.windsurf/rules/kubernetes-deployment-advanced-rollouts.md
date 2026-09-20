---
trigger: glob
description: "Advanced Kubernetes deployment strategies: canary and blue/green rollouts, rollbacks to revisions, and rollout pausing/resuming."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Kubernetes Deployment Advanced Rollouts

Advanced Kubernetes deployment strategies: canary and blue/green rollouts, rollbacks to revisions, and rollout pausing/resuming.

## Instructions

# Kubernetes Deployments (Advanced)

Progressive delivery: canaries, blue/green, and controlled rollbacks.

## What this skill does

- Inspects rollout history and rolls back to prior revisions.
- Pauses/resumes rollouts for manual verification gates.
- Runs canary and blue/green patterns with services.

## When to use

- Gradual feature rollouts with traffic shaping.
- Instant rollback on regression without image rebuilds.
- Zero-downtime upgrades across versions.

## Real commands

```bash
# History
kubectl rollout history deployment/nginx
kubectl rollout history deployment/nginx --revision=3

# Rollback
kubectl rollout undo deployment/nginx
kubectl rollout undo deployment/nginx --to-revision=2

# Pause/resume (canary verification window)
kubectl rollout pause deployment/nginx
kubectl rollout resume deployment/nginx

# Canary: separate deployment with track label
kubectl apply -f canary-deployment.yaml
kubectl scale deployment nginx-canary --replicas=1

# Blue/green: flip service selector
kubectl apply -f green-deployment.yaml
kubectl patch service nginx -p '{"spec":{"selector":{"track":"green"}}}'
```

## Canary YAML example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
      track: canary
  template:
    metadata:
      labels:
        app: nginx
        track: canary
    spec:
      containers:
        - name: nginx
          image: nginx:1.29
```

## Testing

```bash
# Route 10% via an ingress weight, or a second service:
kubectl get svc nginx-canary
curl -H 'Host: nginx-canary' http://<ingress>/ | grep Server
```

## Best practices

- Use rollout undo --to-revision=N instead of manual image reverts.
- Keep a few old revisions (revisionHistoryLimit) for quick rollbacks.
- Combine canaries with metrics gates (Argo Rollouts) for automation.

## Capabilities

### advanced-rollouts
Manage revisions: history, rollback, pause, and resume.

**Commands:**
- `kubectl rollout history deployment/nginx`
- `kubectl rollout history deployment/nginx --revision=3`
- `kubectl rollout undo deployment/nginx`
- `kubectl rollout undo deployment/nginx --to-revision=2`
- `kubectl rollout pause deployment/nginx`
- `kubectl rollout resume deployment/nginx`

**Examples:**
- kubectl rollout history deployment/nginx
- kubectl rollout undo deployment/nginx --to-revision=2
- kubectl rollout pause deployment/nginx

### canary-bluegreen
Implement canary and blue/green release patterns with labels and services.

**Commands:**
- `kubectl apply -f canary-deployment.yaml`
- `kubectl get deployments -l app=nginx --show-labels`
- `kubectl scale deployment nginx-canary --replicas=1`
- `kubectl apply -f blue-deployment.yaml && kubectl apply -f green-deployment.yaml`
- `kubectl patch service nginx -p '{"spec":{"selector":{"track":"green"}}}'`

**Examples:**
- kubectl apply -f canary-deployment.yaml
- kubectl scale deployment nginx-canary --replicas=1
- kubectl patch service nginx -p '{"spec":{"selector":{"track":"green"}}}'
