# infrastructure-compliance-scanner-infrastructure-compliance-scanner

Scans infrastructure code and clusters for compliance violations with Checkov, Trivy, kube-bench, and Gitleaks.

## Instructions

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