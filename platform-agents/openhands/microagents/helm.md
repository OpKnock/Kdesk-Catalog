---
name: "helm"
description: "Packages, installs, and manages Kubernetes applications with Helm: charts, repos, releases, values, linting, and rollbacks."
type: knowledge
triggers: ["helm", "releases", "chart-development"]
---

# helm

Packages, installs, and manages Kubernetes applications with Helm: charts, repos, releases, values, linting, and rollbacks.

## Instructions

# Helm Package Management

Package and deploy Kubernetes apps with Helm charts and releases.

## What This Skill Does

- Creates, lints, and packages charts
- Installs and upgrades releases with values files
- Manages chart repositories and dependencies
- Rolls back failed releases
- Renders manifests with helm template for review

## When to Use

- Deploying a third-party app from a public chart (nginx, postgres, kafka)
- Releasing your own application as a chart
- Debugging why a rendered manifest differs from expectations

## Real Commands

```bash
# Repos and search
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/nginx --versions

# Install / upgrade
helm install myapp bitnami/nginx --namespace app --create-namespace
helm upgrade --install myapp ./chart --values prod.yaml --set image.tag=1.2.0
helm list -A
helm status myapp

# Safety
helm template myapp ./chart --debug | less
helm lint ./chart
helm diff upgrade myapp ./chart --values prod.yaml    # with helm-diff plugin
helm rollback myapp 2
helm uninstall myapp
```

## Chart Structure

```
mychart/
  Chart.yaml          # apiVersion, name, version, dependencies
  values.yaml         # defaults
  templates/
    deployment.yaml
    service.yaml
    _helpers.tpl      # named templates
  charts/             # vendored dependencies
```

## Best Practices

- Always run `helm lint` and `helm template` before install
- Store values per environment (dev.yaml, prod.yaml), never edit defaults inline
- Use `--atomic` on upgrades so failures auto-rollback
- Pin chart versions with `--version`; use OCI registries when possible
- Verify with `helm list` and `helm status` after any operation

## Capabilities

### releases
Install, upgrade, rollback, and uninstall chart releases.

**Commands:**
- `helm install myapp ./chart`
- `helm upgrade --install myapp ./chart --values prod.yaml --namespace app`
- `helm list -A`
- `helm status myapp`
- `helm rollback myapp 2`
- `helm uninstall myapp`

**Examples:**
- helm upgrade --install myapp ./chart --values prod.yaml
- helm rollback myapp 2
- helm status myapp

### chart-development
Create, lint, template, and package charts, plus manage repos.

**Commands:**
- `helm create mychart`
- `helm lint ./mychart`
- `helm template myapp ./mychart --debug`
- `helm package ./mychart --version 1.2.0`
- `helm repo add bitnami https://charts.bitnami.com/bitnami`
- `helm search repo bitnami/nginx`
- `helm dependency update ./mychart`

**Examples:**
- helm create mychart
- helm template myapp ./mychart --debug
- helm package ./mychart --version 1.2.0
