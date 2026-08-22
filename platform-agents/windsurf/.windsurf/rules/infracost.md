---
trigger: glob
description: "Shows cloud cost estimates for Terraform, Pulumi, and OpenTofu infrastructure before you apply, and diffs cost changes in CI."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.sh", "**/*.tf", "**/*.{yaml,yml}"]
---

# Infracost

Shows cloud cost estimates for Terraform, Pulumi, and OpenTofu infrastructure before you apply, and diffs cost changes in CI.

## Instructions

# Infracost

Estimate infrastructure cost from Terraform/Pulumi code before provisioning.

## When to Use

- PR reviews that change resource sizes or add instances
- Estimating greenfield environments from IaC
- Budgeting multi-environment (dev/staging/prod) footprints

## Breakdown

```bash
infracost breakdown --path . --format table
infracost breakdown --path terraform/env/prod --show-skipped
infracost breakdown --path . --usage-file usage.yml
```

## Usage files

Resource prices assume default usage; provide real values for accuracy:

```yaml
aws_instance.web:
  monthly_network_ingress_gb: 120
  monthly_network_egress_gb: 30
  operating_system: linux
```

```bash
infracost breakdown --path . --usage-file usage.yml --sync-usage-file
```

`--sync-usage-file` writes missing resource keys back so you can fill real numbers.

## Diff in CI

```bash
terraform plan -out tfplan.json
infracost diff --path tfplan.json
```

For GitHub Actions, render a comment:

```bash
infracost output --path cost.json --format github-comment >> $GITHUB_OUTPUT
```

## Best practices

- Fail the build when monthly delta exceeds the team budget (e.g. $500).
- Always attach a usage file in review environments; defaults mislead.
- Compare against a baseline to see only the PR's cost impact.
- Include both IaC cost and idle/overprovisioned cost in monthly reviews.

## Testing

```bash
infracost diff --path . --compare-to .infracost/base.json
```

Keep `.infracost/base.json` refreshed weekly so diffs stay small.

## Capabilities

### breakdown
Generate detailed infrastructure cost estimates.

**Commands:**
- `infracost breakdown --path .`
- `infracost breakdown --path . --format json`
- `infracost breakdown --path ./terraform --show-skipped`
- `infracost breakdown --path . --usage-file usage.yml`
- `infracost breakdown --path . --sync-usage-file`

**Examples:**
- infracost breakdown --path . --format table
- infracost breakdown --path terraform/env/prod --show-skipped
- infracost breakdown --path . --usage-file usage.yml --out-file cost.json

### diff
Show cost change between plans in CI pull requests.

**Commands:**
- `infracost diff --path plan.json`
- `infracost diff --path . --format json`
- `infracost diff --path . --compare-to .infracost/base.json`
- `infracost output --path cost.json --format github-comment`
- `infracost output --path cost.json --format html --out-file cost.html`

**Examples:**
- infracost diff --path tfplan.json | tee /tmp/cost-diff.txt
- infracost diff --path . --format json > diff.json
- infracost output --path cost.json --format slack-comment
