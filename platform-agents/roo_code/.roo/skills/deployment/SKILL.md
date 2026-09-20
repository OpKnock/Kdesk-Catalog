---
name: "deployment"
description: "Performs Kubernetes deployments and rollouts: create, update, rollback, scale, and canary traffic shifts with real kubectl commands."
---

# deployment

Performs Kubernetes deployments and rollouts: create, update, rollback, scale, and canary traffic shifts with real kubectl commands.

## Instructions

# Kubernetes Deployment Operations

Ship code to Kubernetes safely: create, update, roll back, and scale Deployments.

## What This Skill Does

- Creates Deployments from images
- Performs zero-downtime updates (RollingUpdate) and rollbacks
- Scales manually or via HorizontalPodAutoscaler
- Exposes workloads via Services
- Diagnoses rollout stalls and CrashLoopBackOff

## When to Use

- Releasing a new image version
- A deployment is failing and needs rollback or diagnosis
- Adding autoscaling to handle load

## Real Commands

```bash
# Create and update
kubectl create deployment web --image=nginx:1.25
kubectl set image deployment/web web=nginx:1.26
kubectl annotate deployment/web kubernetes.io/change-cause="bump nginx 1.26"

# Rollout control
kubectl rollout status deployment/web --timeout=120s
kubectl rollout history deployment/web
kubectl rollout undo deployment/web --to-revision=2
kubectl rollout restart deployment/web

# Scale and expose
kubectl scale deployment/web --replicas=5
kubectl autoscale deployment/web --min=2 --max=10 --cpu-percent=70
kubectl expose deployment web --type=ClusterIP --port=80 --target-port=8080
kubectl get hpa,svc,pods -l app=web
```

## Manifest Notes

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

## Best Practices

- Always add `kubernetes.io/change-cause` annotations for audit history
- Use `kubectl rollout status` with a timeout so CI fails fast
- Prefer `set image` over editing manifests in prod
- Add liveness/readiness probes before doing rollouts
- Set HPA with both CPU and custom metrics; test scale-up behavior
- Keep old revisions: bump `spec.revisionHistoryLimit` when needed

## Capabilities

### deployment-rollouts
Create and manage Deployments with rollout control, updates, and rollbacks.

**Commands:**
- `kubectl create deployment web --image=nginx:1.25`
- `kubectl set image deployment/web web=nginx:1.26`
- `kubectl rollout status deployment/web`
- `kubectl rollout history deployment/web`
- `kubectl rollout undo deployment/web`
- `kubectl rollout restart deployment/web`

**Examples:**
- kubectl set image deployment/web web=nginx:1.26
- kubectl rollout undo deployment/web --to-revision=2
- kubectl rollout status deployment/web --timeout=120s

### scaling-and-exposure
Scale replicas and expose deployments as services or ingress routes.

**Commands:**
- `kubectl scale deployment/web --replicas=5`
- `kubectl autoscale deployment/web --min=2 --max=10 --cpu-percent=70`
- `kubectl expose deployment web --type=LoadBalancer --port=80 --target-port=8080`
- `kubectl get svc -l app=web`
- `kubectl get hpa`

**Examples:**
- kubectl scale deployment/web --replicas=5
- kubectl autoscale deployment/web --min=2 --max=10 --cpu-percent=70
- kubectl expose deployment web --type=LoadBalancer --port=80
