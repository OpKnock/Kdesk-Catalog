Hands-on API deployment: kubectl rollouts, Helm upgrades, rollbacks, and Kubernetes deployment strategy operations.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl rollout status deployment/api -n prod`, `helm install api ./charts/api -n prod`
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

**Parameters:**
- `deployment` (string): Deployment name
- `image` (string): Image tag to deploy
- `namespace` (string): Kubernetes namespace

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

**Parameters:**
- `chart` (string): Chart path
- `release` (string): Release name
- `revision` (string): Rollback revision

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

## References
- [kubectl Rollout](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Helm Docs](https://helm.sh/docs/)