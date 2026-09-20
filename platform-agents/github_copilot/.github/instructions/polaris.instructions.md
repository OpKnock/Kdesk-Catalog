---
applyTo: "**/*.go **/*.html **/*.r **/*.sh **/*.{yaml,yml}"
---

Audits Kubernetes workloads against best-practice checks and runs an in-cluster dashboard with Fairwinds Polaris.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `polaris audit --audit-path .`, `polaris dashboard --port 8080`
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

**Parameters:**
- `auditPath` (string): Path to manifests or kubeconfig for live audit
- `config` (string): Custom configuration YAML path
- `output` (string): Report format: json, html, sarif, score

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

**Parameters:**
- `port` (string): Dashboard listen port
- `namespace` (string): Namespace of the dashboard service

**Commands:**
- `polaris dashboard --port 8080`
- `kubectl port-forward svc/polaris-dashboard 8080:80 -n polaris`
- `helm install polaris fairwinds-stable/polaris`
- `polaris dashboard --audit-path . --port 8080`

**Examples:**
- polaris dashboard --port 8080
- helm install polaris fairwinds-stable/polaris
- kubectl port-forward svc/polaris 8080:80 -n polaris

## References
- [Polaris Documentation](https://polaris.docs.fairwinds.com/)
- [Fairwinds Polaris GitHub](https://github.com/FairwindsOps/polaris)
