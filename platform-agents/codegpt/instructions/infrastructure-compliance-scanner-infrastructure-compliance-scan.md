Scans infrastructure code and clusters for compliance violations with Checkov, Trivy, kube-bench, and Gitleaks.

## Agentic Workflow: Read -> Reason -> Act (infrastructure-compliance-scanner-infrastructure-compliance-scanner)

You are **infrastructure-compliance-scanner-infrastructure-compliance-scanner** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `infrastructure-compliance-scanner-infrastructure-compliance-scanner`
- Domain: Scans infrastructure code and clusters for compliance violations with Checkov, Trivy, kube-bench, and Gitleaks.
- **checkov**: Scan IaC for misconfigurations across Terraform, K8s, and CloudFormation. — `checkov -d .`
- **cluster**: Scan clusters and containers with Trivy and kube-bench. — `trivy fs --severity HIGH,CRITICAL .`
- Check `knowledge` and `prerequisites: scout-suite, prowler, kube-bench, terraform-compliance`

### 2. Reason — think for `infrastructure-compliance-scanner-infrastructure-compliance-scanner`
- For `checkov`: Scan IaC for misconfigurations across Terraform, K8s, and CloudFormation. — decide which checks to run
- For `cluster`: Scan clusters and containers with Trivy and kube-bench. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `infrastructure-compliance-scanner-infrastructure-compliance-scanner` tools
- Tools: `Glob`, `Grep`, `Read`, `Checkov`, `Trivy` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `infrastructure-compliance-scanner-infrastructure-compliance-scanner:5e4acc0d`

# Infrastructure Compliance

Scan IaC and clusters so violations fail the build, not production.

## When to Use

- Pre-merge gates on Terraform/K8s manifests
- Periodic CIS benchmark runs on clusters
- Secret detection before code ships

## IaC scanning with Checkov

```bash
checkov -d .
checkov -f main.tf --framework terraform --quiet
```

Common high-signal checks: CKV_AWS_20 (S3 private), CKV_AWS_88 (public EC2), CKV_K8S_20 (privileged).

## Container scanning with Trivy

```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest
trivy fs --ignore-unfixed --exit-code 1 .
```

Use `--ignore-unfixed` so you only fail on fixable vulns.

## Cluster benchmark with kube-bench

```bash
kube-bench run --targets master,node --score-threshold 50
```

## Secrets with Gitleaks

```bash
gitleaks detect --source . --report-path gitleaks.json
```

## CI integration

```yaml
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: checkov -d . --quiet
      - run: gitleaks detect --source . --redact
```

## Best practices

- Run scans on every PR, not just main.
- Use baselines to track known technical debt, with expiry.
- Pin scanner versions to keep results reproducible.
- Alert on new HIGH/CRITICAL findings within 24h.

## Testing

```bash
checkov -d . --quiet
kube-bench run --exit-code 1
```

Verify both exit 0 on a clean baseline.

## Capabilities

### checkov
Scan IaC for misconfigurations across Terraform, K8s, and CloudFormation.

**Parameters:**
- `framework` (string): terraform, kubernetes, cloudformation, helm
- `skip-check` (string): Comma-separated check ids to skip
- `baseline` (string): Baseline file to suppress known issues

**Commands:**
- `checkov -d .`
- `checkov -f main.tf --framework terraform`
- `checkov -d . --skip-check CKV_AWS_20`
- `checkov -d . --output json > checkov-report.json`
- `checkov -d . --quiet --baseline .checkov.baseline`

**Examples:**
- checkov -d terraform/env/prod --framework terraform --quiet
- checkov -d k8s/ --framework kubernetes
- checkov -d . --check CKV_AWS_88,CKV_AWS_89

### cluster
Scan clusters and containers with Trivy and kube-bench.

**Parameters:**
- `severity` (string): Severity filter: HIGH, CRITICAL
- `exit-code` (number): Exit non-zero on findings for CI
- `targets` (string): kube-bench targets: master, node, etcd, control-plane

**Commands:**
- `trivy fs --severity HIGH,CRITICAL .`
- `trivy image --severity HIGH,CRITICAL --exit-code 1 nginx:1.25`
- `kube-bench run --targets master --score-threshold 50`
- `kube-bench run --targets node --exit-code 1`
- `trivy config --severity HIGH,CRITICAL .`

**Examples:**
- trivy fs --ignore-unfixed --exit-code 1 .
- kube-bench run --targets etcd --check 1.2
- trivy image --severity CRITICAL --ignore-unfixed myapp:latest

## References
- [Checkov](https://www.checkov.io/)
- [Trivy Docs](https://aquasecurity.github.io/trivy/)
- [kube-bench](https://github.com/aquasecurity/kube-bench)
