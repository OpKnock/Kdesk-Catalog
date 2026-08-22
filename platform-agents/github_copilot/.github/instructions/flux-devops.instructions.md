---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# flux-devops

Implements GitOps with Flux CD: bootstrap clusters from git, manage Kustomizations and HelmReleases, and reconcile on demand.

## Instructions

# Flux CD GitOps

Drive cluster state from git using Flux: sources, Kustomizations, and Helm releases.

## What This Skill Does

- Bootstraps Flux into a cluster (kustomization controller + source controller + Helm)
- Connects GitRepository sources and watches branches
- Applies Kustomizations with pruning (drift removal)
- Manages HelmReleases through charts
- Triggers manual reconciliation and shows sync state

## When to Use

- Moving from kubectl apply to GitOps
- Multi-cluster config management from one repo
- Auditable deployments with automatic drift correction

## Real Commands

```bash
# Preflight + bootstrap
flux check --pre
flux bootstrap github --owner=myorg --repository=fleet   --branch=main --path=./clusters/prod --personal

# Sources
flux create source git app --url=https://github.com/myorg/app --branch=main
flux get sources git
flux reconcile source git app

# Kustomizations
flux create kustomization apps --source=GitRepository/app   --path=./apps --prune=true --interval=5m --wait
flux reconcile kustomization apps

# Helm
flux create helmrelease nginx --source=HelmRepository/bitnami   --chart=nginx --target-namespace=web
flux get helmreleases -A

# Debug
flux events -A
kubectl get kustomization apps -o yaml | yq .status
```

## Best Practices

- Use `--prune=true` so deleted git files are removed from the cluster
- Set `--wait` in CI to fail on drifted applies
- Separate app config from cluster config with path prefixes
- Use `flux events -A` for near-real-time sync issues
- Enable image automation (ImagePolicy) for tag-based delivery

## Capabilities

### flux-bootstrap
Bootstrap Flux into a cluster and create Git sources for repositories.

**Commands:**
- `flux check --pre`
- `flux bootstrap github --owner=myorg --repository=fleet --branch=main --path=./clusters/prod`
- `flux install`
- `flux create source git app --url=https://github.com/myorg/app --branch=main`
- `flux get sources git`

**Examples:**
- flux bootstrap github --owner=myorg --repository=fleet --branch=main --path=./clusters/prod
- flux create source git app --url=https://github.com/myorg/app
- flux check --pre

### kustomizations-and-helm
Define Kustomizations and HelmReleases, and trigger reconciliations.

**Commands:**
- `flux create kustomization apps --source=GitRepository/app --path=./apps --prune=true --interval=5m`
- `flux create helmrelease nginx --source=HelmRepository/bitnami --chart=nginx --target-namespace=web`
- `flux reconcile kustomization apps`
- `flux reconcile source git app`
- `flux get kustomizations`
- `flux get helmreleases -A`

**Examples:**
- flux create kustomization apps --source=GitRepository/app --path=./apps --prune=true
- flux reconcile kustomization apps
- flux get helmreleases -A
