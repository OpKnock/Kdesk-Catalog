---
name: "api-deploy-engineer"
description: "Hands-on API deployment: kubectl rollouts, Helm upgrades, rollbacks, and Kubernetes deployment strategy operations."
type: knowledge
triggers: ["api-deploy-engineer", "kubectl-deploys", "helm-ops"]
---

# api-deploy-engineer

Hands-on API deployment: kubectl rollouts, Helm upgrades, rollbacks, and Kubernetes deployment strategy operations.

## Instructions

# API Deploy Engineer

Operates Kubernetes deployments for APIs with rollback discipline.

## When to Use
- Daily API deploys on Kubernetes
- Recovering from bad releases
- Standardizing upgrade commands

## Real Commands

```bash
# Update image
kubectl set image deployment/api api=registry.example/api:v2.0.0 -n prod
kubectl rollout status deployment/api -n prod

# Inspect history
kubectl rollout history deployment/api -n prod

# Roll back
kubectl rollout undo deployment/api -n prod --to-revision=2

# Helm path
helm upgrade api ./charts/api -n prod --set image.tag=v2.0.0
helm rollback api 3 -n prod
```

## Safe Deploy Checklist
- Readiness probe passes before traffic
- Rollout status watched to completion
- Rollback tested in staging first

## Testing
Use `kubectl rollout status` with `--watch` and verify zero errors during the window.

## Best Practices
- One image tag per release
- Keep at least 10 rollout revisions

## Capabilities

### kubectl-deploys
Roll out and roll back Kubernetes deployments safely

**Commands:**
- `kubectl rollout status deployment/api -n prod`
- `kubectl set image deployment/api api=registry.example/api:v2.0.0 -n prod`
- `kubectl rollout undo deployment/api -n prod`
- `kubectl rollout history deployment/api -n prod`
- `kubectl rollout pause deployment/api -n prod`

**Examples:**
- kubectl set image deployment/api api=registry.example/api:v2.0.0 -n prod && kubectl rollout status deployment/api -n prod
- kubectl rollout history deployment/api -n prod | head -10
- kubectl rollout undo deployment/api -n prod --to-revision=2

### helm-ops
Install, upgrade, and roll back API charts

**Commands:**
- `helm install api ./charts/api -n prod`
- `helm upgrade api ./charts/api -n prod --set image.tag=v2.0.0`
- `helm rollback api 3 -n prod`
- `helm history api -n prod`
- `helm list -n prod`

**Examples:**
- helm upgrade api ./charts/api -n prod --set image.tag=v2.0.0
- helm rollback api 3 -n prod
- helm history api -n prod
