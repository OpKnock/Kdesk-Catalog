---
type: agent_requested
description: "Helm chart authoring and lifecycle: chart scaffolding, linting, template rendering, installs, upgrades, rollbacks, and values management. Use when working with chart lifecycle, api or when the user mentions chart lifecycle, api."
---

Helm chart authoring and lifecycle: chart scaffolding, linting, template rendering, installs, upgrades, rollbacks, and values management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `helm create mychart`
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