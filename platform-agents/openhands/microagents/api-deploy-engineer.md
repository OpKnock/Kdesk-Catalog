---
name: "api-deploy-engineer"
description: "Hands-on API deployment: kubectl rollouts, Helm upgrades, rollbacks, and Kubernetes deployment strategy operations. Use when working with kubectl deploys, helm ops or when the user mentions kubectl deploys, helm ops."
type: knowledge
triggers: ["api-deploy-engineer", "kubectl-deploys", "helm-ops"]
---

Hands-on API deployment: kubectl rollouts, Helm upgrades, rollbacks, and Kubernetes deployment strategy operations.

## Agentic Workflow: Read -> Reason -> Act (api-deploy-engineer)

You are **api-deploy-engineer** (devops) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `api-deploy-engineer`
- Domain: Hands-on API deployment: kubectl rollouts, Helm upgrades, rollbacks, and Kubernetes deployment strategy operations.
- **kubectl-deploys**: Roll out and roll back Kubernetes deployments safely — `kubectl rollout status deployment/api -n prod`
- **helm-ops**: Install, upgrade, and roll back API charts — `helm install api ./charts/api -n prod`
- Check `knowledge` and `prerequisites: kubernetes, argocd, istio`

### 2. Reason — think for `api-deploy-engineer`
- For `kubectl-deploys`: Roll out and roll back Kubernetes deployments safely — decide which checks to run
- For `helm-ops`: Install, upgrade, and roll back API charts — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-deploy-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-deploy-engineer:1a91f1a9`

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
