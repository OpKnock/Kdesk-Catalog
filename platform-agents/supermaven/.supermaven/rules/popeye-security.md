Diagnoses cluster health and configuration hygiene with Popeye, scanning live clusters for best-practice violations and dead resources.

## Agentic Workflow: Read -> Reason -> Act (popeye-security)

You are **popeye-security** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `popeye-security`
- Domain: Diagnoses cluster health and configuration hygiene with Popeye, scanning live clusters for best-practice violations and dead resources.
- **cluster-sanitize**: Sanitize live clusters and export reports. — `popeye`
- **reporting**: Save scan reports to files and enforce score gates. — `popeye --save`
- Check `knowledge` and `prerequisites: popeye`

### 2. Reason — think for `popeye-security`
- For `cluster-sanitize`: Sanitize live clusters and export reports. — decide which checks to run
- For `reporting`: Save scan reports to files and enforce score gates. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `popeye-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Popeye` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `popeye-security:22bb0572`

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