---
trigger: glob
description: "Audits Kubernetes workloads against best-practice checks and runs an in-cluster dashboard with Fairwinds Polaris."
globs: ["**/*.go", "**/*.html", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# polaris

Audits Kubernetes workloads against best-practice checks and runs an in-cluster dashboard with Fairwinds Polaris.

## Instructions

# Polaris

Audit Kubernetes workloads against security and best-practice checks.

## What This Skill Does

- Audits manifests or live clusters against built-in checks
- Returns scores per workload and category
- Gates CI with --set-exit-code-below-score
- Runs a visual dashboard for remediation tracking

## When to Use

- Workload hardening before rollout
- Enforcing minimum scores on manifests in CI
- Reviewing cluster-wide workload hygiene

## Real Commands

```bash
# Audit manifests
polaris audit --audit-path .

# Score gate in CI
polaris audit --audit-path . --set-exit-code-below-score 80

# Custom config
polaris audit --audit-path . --config polaris.yaml

# Targeted checks
polaris audit --audit-path . --only-checks resources,healthchecks

# Reports
polaris audit --audit-path . --output report.html
polaris audit --audit-path . --output sarif

# Dashboard
polaris dashboard --port 8080
```

## Sample Config

```yaml
checks:
  resources:
    cpuRequestsMissing:
      successMessage: CPU requests set
      severity: warning
  security:
    runAsRootAllowed:
      severity: error
```

## Best Practices

- Start with audit-only, then enforce score gates
- Customize severities in config; don't delete checks silently
- Run per-chart manifests to catch Helm template output issues
- Pair with resource limit admission policies for hard enforcement
- Track scores over time in CI artifacts

## Capabilities

### polaris-audit
Audit manifests or live clusters with exit-code gating.

**Commands:**
- `polaris audit --audit-path .`
- `polaris audit --audit-path manifests/ --set-exit-code-below-score 80`
- `polaris audit --audit-path . --config polaris.yaml`
- `polaris audit --audit-path . --only-checks resources`
- `polaris audit --audit-path . --output sarif`

**Examples:**
- polaris audit --audit-path . --set-exit-code-below-score 75
- polaris audit --audit-path . --only-checks healthchecks
- polaris audit --audit-path manifests/ --output report.html

### dashboard
Run the Polaris web dashboard in-cluster.

**Commands:**
- `polaris dashboard --port 8080`
- `kubectl port-forward svc/polaris-dashboard 8080:80 -n polaris`
- `helm install polaris fairwinds-stable/polaris`
- `polaris dashboard --audit-path . --port 8080`

**Examples:**
- polaris dashboard --port 8080
- helm install polaris fairwinds-stable/polaris
- kubectl port-forward svc/polaris 8080:80 -n polaris
