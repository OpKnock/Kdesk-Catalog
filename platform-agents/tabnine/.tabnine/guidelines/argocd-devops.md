# argocd-devops

GitOps with Argo CD: app registration, syncs, rollbacks, and sync policies for Kubernetes.

## Instructions

# Argo CD

GitOps continuous delivery: apps defined in git, synced to Kubernetes automatically
with drift detection.

## When to Use

- Declarative, auditable deployments
- Multi-cluster app promotion
- Automated sync with rollback safety

## Real Commands

```bash
# Login
sudo argocd login argocd.example.com --sso

# Create an app
sudo argocd app create guestbook \
  --repo https://github.com/org/repo \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default

# Sync
sudo argocd app sync guestbook --prune

# Status / diff
sudo argocd app get guestbook
sudo argocd app diff guestbook

# Rollback
sudo argocd app rollback guestbook 2

# Automate
sudo argocd app set guestbook --sync-policy automated --auto-prune --self-heal

# List and delete
sudo argocd app list
sudo argocd app delete guestbook --yes
```

## Declarative App (CR)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
spec:
  source:
    repoURL: https://github.com/org/repo
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Best Practices

- Use automated sync + self-heal for mature services
- Review `argocd app diff` before manual syncs
- Pin the git revision in promotions; use tags
- Set prune carefully: it deletes live resources
- Prefer app-of-apps pattern for many services

## Example Response

For a drift: diffs the app, explains the mismatch, syncs, and verifies
application health is Healthy/Synced.

## Capabilities

### argocd-apps
Manage Argo CD applications and their sync lifecycle

**Commands:**
- `argocd login argocd.example.com --sso`
- `argocd app create guestbook --repo https://github.com/org/repo --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default`
- `argocd app sync guestbook`
- `argocd app get guestbook`
- `argocd app rollback guestbook 2`

**Examples:**
- argocd app list
- argocd app diff guestbook
- argocd app set guestbook --sync-policy automated --auto-prune