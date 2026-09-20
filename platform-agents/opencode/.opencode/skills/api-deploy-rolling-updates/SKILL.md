---
name: "api-deploy-rolling-updates"
description: "Implements standard deployment pipelines: rolling updates with health gates, versioned releases, and staged rollouts. Use when working with rolling updates, staged rollout or when the user mentions rolling updates, staged rollout."
---

Implements standard deployment pipelines: rolling updates with health gates, versioned releases, and staged rollouts.

## Agentic Workflow: Read -> Reason -> Act (api-deploy-rolling-updates)

You are **Api Deploy Rolling Updates** (devops) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `api-deploy-rolling-updates`
- Domain: Implements standard deployment pipelines: rolling updates with health gates, versioned releases, and staged rollouts.
- **rolling-updates**: Configure rolling updates with readiness and liveness gates — `kubectl rollout restart deployment/api -n prod`
- **staged-rollout**: Roll out through dev, staging, then production with promotion checks — `kubectl apply -f deploy/dev/api.yaml --record`
- Check `knowledge` and `prerequisites: kubernetes, argocd, istio`

### 2. Reason — think for `api-deploy-rolling-updates`
- For `rolling-updates`: Configure rolling updates with readiness and liveness gates — decide which checks to run
- For `staged-rollout`: Roll out through dev, staging, then production with promotion checks — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-deploy-rolling-updates` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-deploy-rolling-updates:20c997f3`

# API Deploy (Implementation)

Implements standard, repeatable deployment pipelines for APIs.

## When to Use
- Standardizing deploy steps
- Adding health-gated updates
- Rolling out environment-by-environment

## Real Commands

```bash
# Rolling update
kubectl rollout restart deployment/api -n prod
kubectl rollout status deployment/api -n prod --watch

# Check strategy
kubectl get deployment api -n prod -o yaml | grep -A5 strategy

# Staged rollout
kubectl apply -f deploy/dev/api.yaml --record
kubectl apply -f deploy/staging/api.yaml --record
kubectl rollout status deployment/api -n staging --timeout 120s
kubectl apply -f deploy/prod/api.yaml --record

# Rollback
kubectl rollout undo deployment/api -n prod
```

## Health Gates
- readinessProbe: /health endpoint
- livenessProbe: /healthz
- maxUnavailable: 25%

## Testing
Watch rollout status during a deploy and verify old pods drain before new ones serve.

## Best Practices
- Record every apply (`--record`)
- Promote only after staging gates pass

## Capabilities

### rolling-updates
Configure rolling updates with readiness and liveness gates

**Parameters:**
- `deployment` (string): Deployment name
- `namespace` (string): Namespace

**Commands:**
- `kubectl rollout restart deployment/api -n prod`
- `kubectl rollout status deployment/api -n prod --watch`
- `kubectl set resources deployment/api -n prod --limits=cpu=500m,memory=512Mi`
- `kubectl get deployment api -n prod -o yaml | grep -A5 strategy`
- `kubectl rollout undo deployment/api -n prod`

**Examples:**
- kubectl rollout restart deployment/api -n prod && kubectl rollout status deployment/api -n prod --watch
- kubectl get deployment api -n prod -o yaml | grep -A5 strategy
- kubectl rollout undo deployment/api -n prod

### staged-rollout
Roll out through dev, staging, then production with promotion checks

**Parameters:**
- `environment` (string): Target environment
- `manifest` (string): Manifest path

**Commands:**
- `kubectl apply -f deploy/dev/api.yaml --record`
- `kubectl apply -f deploy/staging/api.yaml --record`
- `kubectl apply -f deploy/prod/api.yaml --record`
- `kubectl rollout status deployment/api -n staging --timeout 120s`
- `kubectl describe deployment api -n staging | grep -E 'Replicas|Conditions'`

**Examples:**
- kubectl apply -f deploy/dev/api.yaml --record && kubectl apply -f deploy/staging/api.yaml --record
- kubectl rollout status deployment/api -n staging --timeout 120s
- kubectl describe deployment api -n staging | grep -E 'Replicas|Conditions'

## References
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Rollout Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
