---
name: "infracost"
description: "Shows cloud cost estimates for Terraform, Pulumi, and OpenTofu infrastructure before you apply, and diffs cost changes in CI. Use when working with breakdown, diff, infracost or when the user mentions breakdown, diff, infracost."
license: "MIT"
compatibility: "Requires infracost."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "finops"}
allowed-tools: "Glob Grep Read Bash(infracost:*)"
---

Shows cloud cost estimates for Terraform, Pulumi, and OpenTofu infrastructure before you apply, and diffs cost changes in CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `infracost breakdown --path .`, `infracost diff --path plan.json`
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

**Parameters:**
- `path` (string): Path to IaC directory or plan JSON
- `format` (string): table, json, html, or markdown output
- `usage-file` (string): YAML file with real usage estimates for accurate pricing

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

**Parameters:**
- `compare-to` (string): Baseline breakdown JSON to diff against
- `format` (string): Output format for comments: github-comment, slack-comment, html
- `path` (string): Plan file or directory to evaluate

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

## References
- [Infracost Docs](https://www.infracost.io/docs/)
- [Infracost CLI reference](https://www.infracost.io/docs/reference/cli/)
- [Infracost CI/CD](https://www.infracost.io/docs/integrations/ci_cd/)
