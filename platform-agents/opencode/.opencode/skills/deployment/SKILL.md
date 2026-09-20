---
name: "deployment"
description: "Performs Kubernetes deployments and rollouts: create, update, rollback, scale, and canary traffic shifts with real kubectl commands. Use when working with deployment rollouts, scaling and exposure, devops or when the user mentions deployment rollouts, scaling and exposure, devops."
---

Performs Kubernetes deployments and rollouts: create, update, rollback, scale, and canary traffic shifts with real kubectl commands.

## Agentic Workflow: Read -> Reason -> Act (deployment)

You are **deployment** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `deployment`
- Domain: Performs Kubernetes deployments and rollouts: create, update, rollback, scale, and canary traffic shifts with real kubectl commands.
- **deployment-rollouts**: Create and manage Deployments with rollout control, updates, and rollbacks. — `kubectl create deployment web --image=nginx:1.25`
- **scaling-and-exposure**: Scale replicas and expose deployments as services or ingress routes. — `kubectl scale deployment/web --replicas=5`
- Check `knowledge` and `prerequisites: kubectl`

### 2. Reason — think for `deployment`
- For `deployment-rollouts`: Create and manage Deployments with rollout control, updates, and rollbacks. — decide which checks to run
- For `scaling-and-exposure`: Scale replicas and expose deployments as services or ingress routes. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `deployment` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `deployment:03b85df4`

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

**Parameters:**
- `deployment` (string): Deployment name, e.g. web
- `image` (string): New container image reference
- `revision` (integer): Rollback target revision

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

**Parameters:**
- `replicas` (integer): Desired replica count
- `min` (integer): Minimum HPA replicas
- `max` (integer): Maximum HPA replicas

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

## References
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubectl Rollout Reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
