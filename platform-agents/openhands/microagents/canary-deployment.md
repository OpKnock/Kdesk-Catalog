---
name: "canary-deployment"
description: "Implements canary releases on Kubernetes with Argo Rollouts: weighted traffic splitting, analysis, and promotion/rollback."
type: knowledge
triggers: ["canary-deployment", "argo-rollouts", "weighted-traffic", "analysis"]
---

# Canary Deployment

Implements canary releases on Kubernetes with Argo Rollouts: weighted traffic splitting, analysis, and promotion/rollback.

## Instructions

# Canary Deployment

## What this skill does

Implements canary releases with Argo Rollouts: weighted traffic steps, pauses for observation, metric analysis gates, and manual promote/abort.

## When to use

- Rolling out a risky change to a small traffic slice
- Gating promotion on error-rate/latency metrics
- Fast rollback by aborting the canary

## Real commands

```bash
# Apply the canary rollout
kubectl apply -f rollout-canary.yaml

# Watch the rollout
kubectl argo rollouts get rollout my-api
kubectl argo rollouts status rollout my-api --timeout 300

# Promote a paused canary
kubectl argo rollouts promote rollout my-api

# Abort a bad canary
kubectl argo rollouts abort rollout my-api

# Inspect analysis
kubectl get analysisrun -l rollout=my-api
```

## Rollout spec (steps)

```yaml
strategy:
  canary:
    steps:
      - setWeight: 10
      - pause: {duration: 60}
      - analysis:
          templates:
            - templateName: error-rate
      - setWeight: 50
      - pause: {}
```

## Testing

- Verify traffic split via kubectl get pods/weight annotations
- Force an analysis failure and confirm abort

## Best practices

- Start at 5-10% weight with a pause for observation
- Pair with analysis templates on real metrics
- Never promote during known incident windows

## Capabilities

### argo-rollouts
Manage canary Rollouts and traffic weights.

**Commands:**
- `kubectl argo rollouts get rollout my-api`
- `kubectl argo rollouts status rollout my-api`
- `kubectl argo rollouts promote rollout my-api`
- `kubectl argo rollouts abort rollout my-api`
- `kubectl get rollout my-api -o yaml`

**Examples:**
- kubectl argo rollouts get rollout my-api
- kubectl argo rollouts status rollout my-api --timeout 300
- kubectl argo rollouts promote rollout my-api --full

### weighted-traffic
Configure weighted canary steps.

**Commands:**
- `kubectl apply -f rollout-canary.yaml`
- `kubectl patch rollout my-api --type=merge -p '{"spec":{"strategy":{"canary":{"steps":[{"setWeight":10},{"pause":{"duration":60}}]}}}}'`
- `kubectl get service my-api -o jsonpath='{.spec.selector}'`
- `kubectl get pods -l app=my-api -o wide`
- `kubectl get analysisrun`

**Examples:**
- kubectl apply -f rollout-canary.yaml && kubectl argo rollouts status rollout my-api
- kubectl get pods -l app=my-api -o custom-columns=NAME:.metadata.name,READY:.status.conditions[0].status
- kubectl get analysisrun -l rollout=my-api

### analysis
Run metric analysis jobs that gate promotion.

**Commands:**
- `kubectl get analysisrun -n app`
- `kubectl get analysisrun canary-1 --namespace app -o yaml`
- `kubectl describe analysisrun -l app=my-api | grep -E 'Status|Failed'`
- `kubectl argo rollouts promote rollout my-api`
- `kubectl argo rollouts abort rollout my-api`

**Examples:**
- kubectl get analysisrun -n app -o custom-columns=NAME:.metadata.name,PHASE:.status.phase
- kubectl describe analysisrun -l app=my-api | grep -E 'Status|Failed'
- kubectl argo rollouts abort rollout my-api
