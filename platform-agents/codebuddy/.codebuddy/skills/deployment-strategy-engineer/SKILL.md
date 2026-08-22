---
name: "deployment-strategy-engineer"
description: "Designs and executes deployment strategies: rolling, blue/green, canary, and rollback on Kubernetes."
---

# deployment-strategy-engineer

Designs and executes deployment strategies: rolling, blue/green, canary, and rollback on Kubernetes.

## Instructions

# Deployment Strategy Engineer

Rolls out changes safely: choose a strategy per risk, execute it, and keep a
rollback path ready.

## When to Use

- Selecting rolling vs canary vs blue-green for a release
- Executing a release with verification gates
- Rolling back cleanly after a bad deploy

## Real Commands

```bash
# Rolling update
sudo kubectl set image deployment/web web=repo/app:v2.1.0
sudo kubectl rollout status deployment/web --timeout=180s
sudo kubectl rollout history deployment/web

# Rollback
sudo kubectl rollout undo deployment/web

# Pause/resume for staged rollout
sudo kubectl rollout pause deployment/web
sudo kubectl rollout resume deployment/web

# Canary via separate deployment
sudo kubectl apply -f k8s/canary.yaml

# Helm release
sudo helm upgrade --install web ./chart --set image.tag=v2.1.0 --set canary.weight=10
```

## Strategy Selection

- Rolling: default; good for stateless with probes
- Blue/green: instant switch, doubled capacity cost
- Canary: riskiest traffic gets 1-10% first, progressive increase
- Recreate: downtime allowed, simplest

## Canary Config (Argo Rollouts)

```yaml
strategy:
  canary:
    steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - setWeight: 50
      - pause: {}
```

## Best Practices

- Set readiness/liveness probes; rollouts rely on them
- Use maxUnavailable/maxSurge carefully for zero-downtime
- Watch error rates during canary steps, not just HTTP 200
- Automate rollback triggers on alert thresholds
- Test the rollback path before the release

## Example Response

Executes the strategy, monitors rollout status and metrics, and if the canary
error rate spikes, rolls back and reports the root cause.

## Capabilities

### k8s-deployments
Execute and verify deployment strategies with kubectl and Helm

**Commands:**
- `kubectl set image deployment/web web=repo/app:v2.1.0`
- `kubectl rollout status deployment/web --timeout=180s`
- `kubectl rollout undo deployment/web`
- `kubectl apply -f k8s/canary.yaml`
- `helm upgrade --install web ./chart --set image.tag=v2.1.0 --set canary.weight=10`

**Examples:**
- kubectl get rs -l app=web --sort-by=.metadata.creationTimestamp
- kubectl rollout history deployment/web
- kubectl rollout pause deployment/web
