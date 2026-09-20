---
type: agent_requested
description: "Designs and executes deployment strategies: rolling, blue/green, canary, and rollback on Kubernetes. Use when working with k8s deployments or when the user mentions k8s deployments."
---

Designs and executes deployment strategies: rolling, blue/green, canary, and rollback on Kubernetes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl set image deployment/web web=repo/app:v2.1.0`
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