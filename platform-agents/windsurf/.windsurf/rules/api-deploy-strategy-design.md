---
trigger: glob
description: "Designs zero-downtime API deployment strategies \u2014 canary, blue-green, rolling \u2014 with Argo Rollouts, Istio traffic splitting, and automated rollback."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Api Deploy Strategy Design

Designs zero-downtime API deployment strategies — canary, blue-green, rolling — with Argo Rollouts, Istio traffic splitting, and automated rollback.

## Instructions

# API Deploy (Strategy Design)

Designs deployment strategies that keep APIs available during releases and roll back automatically on failure.

## When to Use
- Zero-downtime releases
- Canary releases with metric analysis
- Blue-green switching with instant rollback
- Meeting availability SLAs

## Real Commands

```bash
# Install Argo Rollouts controller
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl argo rollouts version

# Watch a rollout
kubectl argo rollouts get rollout api -n prod --watch

# Promote / abort
kubectl argo rollouts promote api -n prod
kubectl argo rollouts abort api -n prod
```

## Canary with Istio

```yaml
# virtual-service.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata: {name: api-canary}
spec:
  hosts: [api]
  http:
    - route:
        - destination: {host: api, subset: stable, weight: 90}
        - destination: {host: api, subset: canary, weight: 10}
```

```bash
kubectl apply -f virtual-service.yaml
istioctl analyze -n prod
```

## Testing
Run `kubectl argo rollouts get rollout --watch` and verify the analysis step pauses on bad metrics.

## Best Practices
- Always define an abort/promote gate
- Verify health checks before traffic shift
- Monitor error rate during rollout

## Capabilities

### strategy-design
Select and model deployment strategies for API services with readiness gates and traffic weights

**Commands:**
- `kubectl apply -f rollout.yaml`
- `kubectl argo rollouts get rollout api -n prod`
- `kubectl argo rollouts promote api -n prod`
- `kubectl argo rollouts abort api -n prod`
- `istioctl analyze -n prod`

**Examples:**
- kubectl argo rollouts get rollout api --watch -n prod
- kubectl argo rollouts promote api -n prod
- istioctl analyze --context prod-cluster -n prod

### traffic-splitting
Route canary traffic with Istio VirtualServices and destination rules

**Commands:**
- `kubectl apply -f virtual-service.yaml`
- `kubectl apply -f destination-rule.yaml`
- `istioctl proxy-status`
- `kubectl get virtualservice -n prod`
- `kubectl describe virtualservice api-canary -n prod`

**Examples:**
- kubectl apply -f canary/virtual-service.yaml -f canary/destination-rule.yaml
- istioctl proxy-status | grep api
- kubectl get virtualservice -n prod -o yaml
