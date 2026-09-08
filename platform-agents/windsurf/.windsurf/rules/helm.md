---
trigger: glob
description: "Packages, installs, and manages Kubernetes applications with Helm: charts, repos, releases, values, linting, and rollbacks. Use when working with releases, chart development, devops or when the user mentions releases, chart development, devops."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Packages, installs, and manages Kubernetes applications with Helm: charts, repos, releases, values, linting, and rollbacks.

## Agentic Workflow: Read -> Reason -> Act (helm)

You are **helm** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `helm`
- Domain: Packages, installs, and manages Kubernetes applications with Helm: charts, repos, releases, values, linting, and rollbacks.
- **releases**: Install, upgrade, rollback, and uninstall chart releases. — `helm install myapp ./chart`
- **chart-development**: Create, lint, template, and package charts, plus manage repos. — `helm create mychart`
- Check `knowledge` and `prerequisites: helm`

### 2. Reason — think for `helm`
- For `releases`: Install, upgrade, rollback, and uninstall chart releases. — decide which checks to run
- For `chart-development`: Create, lint, template, and package charts, plus manage repos. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `helm` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `helm:ec201c91`

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

**Parameters:**
- `release` (string): Release name
- `chart` (string): Chart path, repo/chart, or URL
- `values` (string): Values file path

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

**Parameters:**
- `version` (string): Chart or app version
- `repo` (string): Repository name for search/add

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

## References
- [Helm Documentation](https://helm.sh/docs/)
- [Helm Charts Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Artifact Hub](https://artifacthub.io/)
