---
name: "popeye-security"
description: "Diagnoses cluster health and configuration hygiene with Popeye, scanning live clusters for best-practice violations and dead resources."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# popeye-security

Diagnoses cluster health and configuration hygiene with Popeye, scanning live clusters for best-practice violations and dead resources.

## Instructions

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

**Commands:**
- `popeye --save`
- `popeye --out json --output-file report.json`
- `popeye --exit-code 3 --score 80`
- `popeye --pull`

**Examples:**
- popeye --save
- popeye --out json --output-file popeye.json
- popeye --exit-code 3 --score 75