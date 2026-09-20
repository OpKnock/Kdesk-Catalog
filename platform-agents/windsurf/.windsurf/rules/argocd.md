---
trigger: glob
description: "Operates Argo CD for GitOps deployments: app creation, sync policies, health checks, rollbacks, and CLI auth. Use when working with app lifecycle, sync policies, rollback and ops, api or when the user mentions app lifecycle, sync policies, rollback and ops, api."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Operates Argo CD for GitOps deployments: app creation, sync policies, health checks, rollbacks, and CLI auth.

## Agentic Workflow: Read -> Reason -> Act (argocd)

You are **Argocd** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `argocd`
- Domain: Operates Argo CD for GitOps deployments: app creation, sync policies, health checks, rollbacks, and CLI auth.
- **app-lifecycle**: Create, sync, and manage Argo CD applications. — `argocd app create my-api --repo https://github.com/org/my-api --path manifests -`
- **sync-policies**: Configure automated sync, pruning, and self-heal behavior. — `argocd app set my-api --sync-policy automated`
- **rollback-and-ops**: Roll back deployments and manage CLI sessions. — `argocd login argocd.staging.your-app.test --sso`
- Check `knowledge` and `prerequisites: argocd`

### 2. Reason — think for `argocd`
- For `app-lifecycle`: Create, sync, and manage Argo CD applications. — decide which checks to run
- For `sync-policies`: Configure automated sync, pruning, and self-heal behavior. — decide which checks to run
- For `rollback-and-ops`: Roll back deployments and manage CLI sessions. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `argocd` tools
- Tools: `Glob`, `Grep`, `Read`, `Argocd` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `argocd:f27ac27b`

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

**Parameters:**
- `repo` (string): Git repository URL
- `path` (string): Manifest/helm path in the repo
- `namespace` (string): Destination namespace
- `prune` (boolean): Delete resources removed from git during sync

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

**Parameters:**
- `sync_policy` (string): manual or automated
- `timeout` (number): Sync/wait timeout in seconds

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

**Parameters:**
- `revision` (number): History index to roll back to
- `server` (string): Argo CD server URL for login

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

## References
- [Argo CD Docs](https://argo-cd.readthedocs.io/)
- [Argo CD CLI](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd/)
- [Declarative GitOps](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
