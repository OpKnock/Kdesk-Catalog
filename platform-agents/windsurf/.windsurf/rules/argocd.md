---
trigger: glob
description: "Operates Argo CD for GitOps deployments: app creation, sync policies, health checks, rollbacks, and CLI auth."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Argocd

Operates Argo CD for GitOps deployments: app creation, sync policies, health checks, rollbacks, and CLI auth.

## Instructions

# Argo CD

## What this skill does

Operates Argo CD for GitOps: creating apps from git repos, controlling sync (manual/automated, prune, self-heal), inspecting sync/health state, rolling back to prior revisions, and CLI auth.

## When to use

- Deploying an API's manifests to Kubernetes from git
- Fixing a bad deploy fast via rollback
- Debugging why the cluster drifts from git

## Real commands

```bash
argocd login argocd.staging.your-app.test --sso

argocd app create my-api --repo https://github.com/org/my-api --path manifests --dest-server https://kubernetes.default.svc --dest-namespace prod

argocd app sync my-api --prune --timeout 300

argocd app set my-api --sync-policy automated --auto-prune --self-heal

argocd app get my-api
argocd app history my-api
argocd app rollback my-api 3
```

## Declarative Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-api
spec:
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
  source:
    repoURL: https://github.com/org/my-api
    path: manifests
    targetRevision: main
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Testing

- Run `argocd app diff my-api` to preview drift
- Wait for health with `argocd app wait my-api --health`

## Best practices

- Prefer declarative Applications in git
- Pin targetRevision (tags, not main) for production
- Enable prune+selfHeal only after diff tooling is in place

## Capabilities

### app-lifecycle
Create, sync, and manage Argo CD applications.

**Commands:**
- `argocd app create my-api --repo https://github.com/org/my-api --path manifests --dest-server https://kubernetes.default.svc --dest-namespace prod`
- `argocd app list`
- `argocd app sync my-api`
- `argocd app get my-api`
- `argocd app delete my-api`

**Examples:**
- argocd app create my-api --repo https://github.com/org/my-api --path charts/api --dest-server https://kubernetes.default.svc --dest-namespace prod --helm-set image.tag=v1.2.0
- argocd app sync my-api --prune --timeout 300
- argocd app get my-api -o wide

### sync-policies
Configure automated sync, pruning, and self-heal behavior.

**Commands:**
- `argocd app set my-api --sync-policy automated`
- `argocd app set my-api --auto-prune`
- `argocd app set my-api --self-heal`
- `argocd app get my-api --show-operation`
- `argocd app wait my-api --health`

**Examples:**
- argocd app set my-api --sync-policy automated --auto-prune --self-heal
- argocd app wait my-api --timeout 300
- argocd app get my-api --refresh

### rollback-and-ops
Roll back deployments and manage CLI sessions.

**Commands:**
- `argocd login argocd.staging.your-app.test --sso`
- `argocd app rollback my-api 3`
- `argocd app history my-api`
- `argocd app terminate-op my-api`
- `argocd account get-user-info`

**Examples:**
- argocd login argocd.staging.your-app.test --username admin --insecure
- argocd app history my-api | head -5
- argocd app rollback my-api 2 --prune
