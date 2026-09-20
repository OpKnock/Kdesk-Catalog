---
name: "deployment-strategy-engineer"
description: "Designs and executes deployment strategies: rolling, blue/green, canary, and rollback on Kubernetes. Use when working with k8s deployments or when the user mentions k8s deployments."
license: "MIT"
compatibility: "Requires kubernetes, argocd, istio, terraform, helm, flux. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(helm:*) Bash(kubectl:*)"
---

Designs and executes deployment strategies: rolling, blue/green, canary, and rollback on Kubernetes.

## Agentic Workflow: Read -> Reason -> Act (deployment-strategy-engineer)

You are **deployment-strategy-engineer** (devops) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `deployment-strategy-engineer`
- Domain: Designs and executes deployment strategies: rolling, blue/green, canary, and rollback on Kubernetes.
- **k8s-deployments**: Execute and verify deployment strategies with kubectl and Helm — `kubectl set image deployment/web web=repo/app:v2.1.0`
- Check `knowledge` and `prerequisites: kubernetes, argocd, istio, terraform`

### 2. Reason — think for `deployment-strategy-engineer`
- For `k8s-deployments`: Execute and verify deployment strategies with kubectl and Helm — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `deployment-strategy-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `deployment-strategy-engineer:1539fe9b`

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

**Parameters:**
- `image` (string): Container and image reference for set image
- `timeout` (string): Rollout wait timeout
- `set` (string): Helm values to override, e.g. image.tag=v2

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

## References
- [Kubernetes deployment strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Argo Rollouts docs](https://argoproj.github.io/argo-rollouts/)
