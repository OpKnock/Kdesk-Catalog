---
name: "helm-charts"
description: "Helm chart authoring and lifecycle: chart scaffolding, linting, template rendering, installs, upgrades, rollbacks, and values management. Use when working with chart lifecycle, api or when the user mentions chart lifecycle, api."
---

Helm chart authoring and lifecycle: chart scaffolding, linting, template rendering, installs, upgrades, rollbacks, and values management.

## Agentic Workflow: Read -> Reason -> Act (helm-charts)

You are **Helm Charts** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `helm-charts`
- Domain: Helm chart authoring and lifecycle: chart scaffolding, linting, template rendering, installs, upgrades, rollbacks, and values management.
- **chart-lifecycle**: Create, lint, render, install, upgrade, and roll back Helm charts. — `helm create mychart`
- Check `knowledge` and `prerequisites: helm`

### 2. Reason — think for `helm-charts`
- For `chart-lifecycle`: Create, lint, render, install, upgrade, and roll back Helm charts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `helm-charts` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `helm-charts:eb3c1e4d`

# Helm Charts

Author and operate Kubernetes applications with Helm.

## What this skill does

- Scaffolds charts with standard directory structure.
- Lints charts and renders templates for review.
- Installs, upgrades, and rolls back releases.
- Manages values across environments.

## When to use

- Packaging an application for repeatable deployment.
- Parameterizing manifests per environment.
- Auditing what a chart will actually create before install.

## Real commands

```bash
# Scaffold a chart
helm create mychart

# Lint
helm lint ./mychart

# Render templates (no cluster needed)
helm template ./mychart
helm template ./mychart --values values-prod.yaml

# Install
helm install myapp ./mychart -n default

# Upgrade with values
helm upgrade --install myapp ./mychart --set image.tag=v2 --namespace default

# Roll back and list
helm rollback myapp 1 -n default
helm list -n default
```

## Chart layout

```text
mychart/
  Chart.yaml
  values.yaml
  charts/
  templates/
    deployment.yaml
    service.yaml
    _helpers.tpl
```

## Example values

```yaml
replicaCount: 3
image:
  repository: nginx
  tag: 1.27
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
resources:
  limits:
    cpu: 500m
    memory: 512Mi
```

## Testing

```bash
helm lint ./mychart && helm template ./mychart --dry-run
helm install myapp ./mychart -n default --dry-run --debug
```

## Best practices

- Use `helm template` + `kubectl diff` before every prod upgrade.
- Never edit a release's live manifests; always `helm upgrade`.
- Pin images via values, not hardcoded tags in templates.
- Add dependency charts with `helm dependency update` and commit Chart.lock.

## Example exchange

```
User: Preview what mychart would deploy with prod values.
Agent: helm template ./mychart --values values-prod.yaml | kubectl diff -f -
```

## Capabilities

### chart-lifecycle
Create, lint, render, install, upgrade, and roll back Helm charts.

**Parameters:**
- `chart_path` (string): Path to the chart directory.
- `release_name` (string): Release name for install/upgrade.
- `values_file` (string): YAML values file to merge.

**Commands:**
- `helm create mychart`
- `helm lint ./mychart`
- `helm template ./mychart`
- `helm install myapp ./mychart -n default`
- `helm upgrade --install myapp ./mychart --set image.tag=v2 --namespace default`

**Examples:**
- helm template ./mychart --values values-prod.yaml | kubectl apply --dry-run=client -f -
- helm rollback myapp 1 -n default
- helm list -n default

## References
- [Helm Docs](https://helm.sh/docs/)
- [Chart Template Guide](https://helm.sh/docs/chart_template_guide/)
