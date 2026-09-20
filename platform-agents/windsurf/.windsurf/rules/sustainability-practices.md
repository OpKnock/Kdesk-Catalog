---
trigger: glob
description: "Measures and reduces software carbon footprint with Cloud Carbon Footprint, InfraCost, and workload efficiency analysis. Use when working with carbon measurement, cost efficiency, workload efficiency or when the user mentions carbon measurement, cost efficiency, workload efficiency."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.sh"]
---

Measures and reduces software carbon footprint with Cloud Carbon Footprint, InfraCost, and workload efficiency analysis.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ccf estimate --configfile ccf.config.json --period 2024-01-0`, `infracost breakdown --path .`
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

# Sustainability Practices

Measure and reduce the environmental impact of software.

## What This Skill Does

- Estimates cloud carbon emissions by service and period
- Identifies idle and oversized workloads
- Aligns efficiency work with cost data
- Promotes right-sizing and autoscaling practices

## When to Use

- Reporting software carbon footprint
- Reducing cloud waste and emissions
- Prioritizing efficiency investments

## Real Commands

```bash
# Carbon estimation
ccf estimate --configfile ccf.config.json --period 2024-01-01 2024-01-31
ccf recommendations --configfile ccf.config.json

# Cost-efficiency
infracost breakdown --path .
infracost diff --path . --compare-to=infracost-base.json

# Utilization
kubectl top nodes
kubectl top pods -A
kubectl get hpa -A
kubectl get nodes -o custom-columns=NAME:.metadata.name,CPU:.status.allocatable.cpu
```

## Reduction Checklist

- Right-size pods and instances to measured utilization
- Autoscale everything that can be scaled to zero
- Prefer ARM and energy-efficient instance families
- Cache aggressively to reduce compute demand
- Offload batch work to off-peak hours

## Best Practices

- Measure first: baseline carbon before optimizing
- Pair carbon savings with cost savings for buy-in
- Monitor utilization continuously, not just at launch
- Document efficiency budgets alongside SLIs
- Revisit instance families when prices and efficiency change

## Capabilities

### carbon-measurement
Estimate cloud carbon emissions and energy usage.

**Parameters:**
- `configfile` (string): Cloud Carbon Footprint config file
- `period` (string): Date range for estimation

**Commands:**
- `ccf estimate --configfile ccf.config.json --period 2024-01-01 2024-01-31`
- `ccf report --configfile ccf.config.json`
- `ccf footprint --configfile ccf.config.json`
- `ccf recommendations --configfile ccf.config.json`

**Examples:**
- ccf estimate --configfile ccf.config.json --period 2024-01-01 2024-01-31
- ccf report --configfile ccf.config.json
- ccf recommendations --configfile ccf.config.json

### cost-efficiency
Align efficiency with cost using InfraCost and cloud queries.

**Parameters:**
- `path` (string): Terraform path to analyze
- `format` (string): Output format: html, json, table

**Commands:**
- `infracost breakdown --path .`
- `infracost diff --path . --compare-to=infracost-base.json`
- `infracost output --format html --path infracost-base.json`
- `infracost breakdown --path . --usage-file infracost-usage.yml`

**Examples:**
- infracost breakdown --path .
- infracost diff --path . --compare-to=infracost-base.json
- infracost output --format html --path infracost-base.json

### workload-efficiency
Analyze cluster utilization and right-sizing opportunities.

**Parameters:**
- `namespace` (string): Namespace scope for resource metrics
- `format` (string): Output format for kubectl top metrics: wide, json.

**Commands:**
- `kubectl top nodes`
- `kubectl top pods -A`
- `kubectl get hpa -A`
- `kubectl get nodes -o custom-columns=NAME:.metadata.name,CPU:.status.allocatable.cpu,MEM:.status.allocatable.memory`

**Examples:**
- kubectl top nodes
- kubectl top pods -A
- kubectl get hpa -A

## References
- [Cloud Carbon Footprint](https://github.com/cloud-carbon-footprint/cloud-carbon-footprint)
- [InfraCost Documentation](https://www.infracost.io/docs/)
- [Green Software Foundation](https://greensoftware.foundation/)
