---
trigger: glob
description: "Diagnoses cluster health and configuration hygiene with Popeye, scanning live clusters for best-practice violations and dead resources. Use when working with cluster sanitize, reporting, security or when the user mentions cluster sanitize, reporting, security."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Diagnoses cluster health and configuration hygiene with Popeye, scanning live clusters for best-practice violations and dead resources.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `popeye`, `popeye --save`
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

# Popeye

Cluster sanitizer: find misconfigurations and dead weight in live clusters.

## What This Skill Does

- Scans live clusters for best-practice violations
- Detects unused resources, duplicate config, and risky settings
- Produces scores and reports per resource type
- Gated CI runs with exit codes and score thresholds

## When to Use

- Regular cluster hygiene reviews
- Pre-upgrade cleanup of dead resources
- Auditing workload configuration consistency

## Real Commands

```bash
# Scan the current cluster
popeye

# Scope the scan
popeye -n kube-system
popeye --context prod
popeye -s pod,svc,deploy

# Reports
popeye --out json --output-file report.json
popeye --out txt
popeye --save

# CI gate
popeye --exit-code 3 --score 80
```

## Best Practices

- Run against a staging cluster copy first to avoid API churn
- Set score gates in CI; investigate every ERROR-level finding
- Use --context explicitly to avoid scanning the wrong cluster
- Pair with Popeye's fix suggestions before manual remediation
- Archive reports per release for trend analysis

## Capabilities

### cluster-sanitize
Sanitize live clusters and export reports.

**Parameters:**
- `context` (string): Kubeconfig context to scan
- `sections` (string): Comma-separated resource types to scan (pod, svc, deploy...)
- `out` (string): Output format: standard, json, yaml, junit

**Commands:**
- `popeye`
- `popeye -n kube-system`
- `popeye --context prod`
- `popeye -s pod`
- `popeye --out txt`

**Examples:**
- popeye
- popeye -n kube-system
- popeye --out json

### reporting
Save scan reports to files and enforce score gates.

**Parameters:**
- `outputFile` (string): Report destination path
- `score` (number): Minimum acceptable score before exit-code triggers
- `exitCode` (number): Exit code to emit when the gate fails

**Commands:**
- `popeye --save`
- `popeye --out json --output-file report.json`
- `popeye --exit-code 3 --score 80`
- `popeye --pull`

**Examples:**
- popeye --save
- popeye --out json --output-file popeye.json
- popeye --exit-code 3 --score 75

## References
- [Popeye Documentation](https://popeyecli.io/)
- [Popeye GitHub](https://github.com/derailed/popeye)
