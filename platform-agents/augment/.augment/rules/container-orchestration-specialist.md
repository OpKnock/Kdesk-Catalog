---
type: agent_requested
description: "Operates Kubernetes clusters: deployments, rollouts, scaling, scheduling, and resource management."
---

# container-orchestration-specialist

Operates Kubernetes clusters: deployments, rollouts, scaling, scheduling, and resource management.

## Instructions

# Container Orchestration

Day-2 operations for Kubernetes: deploying workloads, managing rollouts, scaling,
and keeping the cluster healthy.

## When to Use

- Deploying or updating applications in a cluster
- Investigating failing pods or stuck rollouts
- Capacity planning via resource usage

## Real Commands

```bash
# Deploy and roll out
kubectl apply -f k8s/deploy.yaml
kubectl rollout status deployment/web --timeout=120s
kubectl rollout history deployment/web

# Roll back
kubectl rollout undo deployment/web

# Scale
kubectl scale deployment/web --replicas=5
kubectl autoscale deployment/web --min=2 --max=10 --cpu-percent=70

# Inspect
kubectl get pods -A -o wide
kubectl describe pod web-7b9f9d9f9-abcde
kubectl logs deployment/web --tail=100 --follow
kubectl get events -A --sort-by=.lastTimestamp

# Node maintenance
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data
kubectl cordon node-2
kubectl uncordon node-2

# Resources
kubectl top nodes
kubectl top pods -A
```

## Helm Usage

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install redis bitnami/redis -n cache --create-namespace
helm list -A
```

## Best Practices

- Use rollouts with health checks; never delete/recreate apps
- Set requests/limits on every container
- Prefer Deployments + Services; use StatefulSets only for state
- Watch events before digging into logs
- Drain before node maintenance, uncordon after

## Example Response

For a broken deployment: reports pod status, recent events, and logs tail, then
executes the rollback or config fix and confirms rollout status.

## Capabilities

### k8s-operations
Manage workloads, rollouts, scaling, and node health in Kubernetes

**Commands:**
- `kubectl get pods -A -o wide`
- `kubectl apply -f k8s/deploy.yaml`
- `kubectl rollout status deployment/web --timeout=120s`
- `kubectl scale deployment/web --replicas=5`
- `kubectl top nodes`

**Examples:**
- kubectl rollout undo deployment/web
- kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data
- kubectl get events -A --sort-by=.lastTimestamp | tail -20