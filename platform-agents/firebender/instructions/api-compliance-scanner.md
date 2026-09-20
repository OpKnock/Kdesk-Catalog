# Api Compliance Scanner

Implements compliance scanning: install scanners, run baseline checks, and fix misconfigurations against GDPR and SOC 2.

## Instructions

# API Compliance (Implementation)

Gets compliance scanning running and fixes baseline findings.

## When to Use
- No scanning exists yet
- Preparing infrastructure for compliance
- Quick wins on misconfigurations

## Real Commands

```bash
# Install
pip install checkov prowler scoutsuite
brew install tfsec

# Baseline scans
checkov -d . --quiet
tfsec .
prowler aws --group group17 --severity high
scout aws --report-dir reports/scout --services ec2,s3

# Targeted check
checkov -d . --check CKV_AWS_20 --quiet
```

## Fix Loop
1. Run baseline
2. Fix critical findings
3. Re-scan
4. Baseline accepted risks

## CI Hook
Add `checkov -d . --quiet` as a pipeline step so new misconfigurations fail fast.

## Testing
Verify fixes by re-running the exact failing check ID.

## Best Practices
- Fix encryption and logging checks first
- Keep scanner versions pinned

## Capabilities

### scanner-setup
Install and configure compliance scanners locally and in CI

**Commands:**
- `pip install checkov`
- `pip install prowler`
- `pip install scoutsuite`
- `brew install tfsec`
- `checkov --version && tfsec --version`

**Examples:**
- pip install checkov prowler scoutsuite && checkov --version
- brew install tfsec && tfsec --version
- pip install checkov && checkov -d . --quiet

### baseline-scanning
Run baseline scans and fix the highest-severity findings

**Commands:**
- `checkov -d . --quiet`
- `tfsec .`
- `prowler aws --group group17`
- `scout aws --report-dir reports/scout --services ec2,s3`
- `checkov -d . --check CKV_AWS_20 --quiet`

**Examples:**
- checkov -d . --quiet && tfsec .
- prowler aws --group group17 --severity high
- scout aws --report-dir reports/scout --services ec2,s3
