---
applyTo: "**/*.go **/*.r **/*.sh **/*.{yaml,yml}"
---

Expert Kubernetes rolling deployment skill covering set image, rollout status/history, undo, pause/resume, and canary verification with kubectl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl set image deployment/api api=ghcr.io/your-org/api:v2`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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

**Parameters:**
- `deployment` (string): Deployment name, e.g. deployment/api
- `image` (string): New image reference, e.g. ghcr.io/your-org/api:v2.1
- `timeout` (string): Rollout wait timeout, e.g. 180s

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

## References
- [K8s Deployment docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [kubectl rollout reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
