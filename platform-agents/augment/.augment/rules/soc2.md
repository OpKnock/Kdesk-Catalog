---
type: agent_requested
description: "Readiness support for SOC 2 Type I/II: mapping Trust Services Criteria to controls and collecting evidence. Use when working with soc2 evidence or when the user mentions soc2 evidence."
---

Readiness support for SOC 2 Type I/II: mapping Trust Services Criteria to controls and collecting evidence.

## Agentic Workflow: Read -> Reason -> Act (soc2)

You are **Soc2** (compliance/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — compliance context for `soc2`
- Domain: Readiness support for SOC 2 Type I/II: mapping Trust Services Criteria to controls and collecting evidence.
- **soc2-evidence**: Gather evidence for the five Trust Services Criteria categories — `gh api repos/$GITHUB_REPO/actions/workflows --paginate | jq '.workflows[].path'`
- Check `knowledge` and `prerequisites: kubectl, terraform`

### 2. Reason — think for `soc2`
- For `soc2-evidence`: Gather evidence for the five Trust Services Criteria categories — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `soc2` tools
- Tools: `Glob`, `Grep`, `Read`, `Gh`, `Terraform` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `soc2:09d06a4d`

# SOC 2

System and Organization Controls 2 readiness: demonstrate the security, availability,
processing integrity, confidentiality, and privacy criteria.

## When to Use

- Preparing a SOC 2 Type I readiness assessment
- Collecting continuous evidence before the Type II period
- Responding to auditor requests for control artifacts

## Real Commands

```bash
# CC7.2 access control: who can deploy
gh api repos/$GITHUB_REPO/actions/workflows --paginate | jq '.workflows[].path'

# CC6.1/CC7.1: IaC review and change management
terraform plan -no-color -out=/tmp/plan.tfplan
terraform show -json /tmp/plan.tfplan | jq '.resource_changes | length'

# CC7.3 monitoring
curl -s http://localhost:8080/metrics | grep -E 'job_last_success|up'

# CC6.6 secrets
sudo gitleaks detect --source . --report-path gitleaks-soc2.json

# A1.2/A1.3 availability: scaling and failover config
rg -i "autoscal|replica|failover" terraform/ k8s/
```

## Criteria Mapping Cheat Sheet

- Security (CC1-CC9): access control, monitoring, change management
- Availability (A1): uptime, redundancy, backup testing
- Confidentiality (C1): encryption, access scope
- Processing integrity (PI1): validations, error handling
- Privacy (P1-P6): notice, choice, retention, disclosure

## Evidence Playbook

1. Enumerate controls per criterion
2. For each control, capture 1-2 artifacts (config, logs, reports)
3. Store evidence with timestamps for the Type II window
4. Run recurring checks so the evidence stream is continuous

## Best Practices

- Start 6-9 months before the Type II audit window
- Map every control to an owner and a system
- Automate evidence collection (cron + versioned reports)
- Review access lists quarterly and keep review records

## Example Response

The agent returns a criteria-to-control matrix with evidence artifacts, owner
assignments, and gaps flagged for the readiness call.

## Capabilities

### soc2-evidence
Gather evidence for the five Trust Services Criteria categories

**Parameters:**
- `paginate` (boolean): Fetch all pages of the GitHub API result
- `report-path` (string): Output file for the evidence report
- `no-color` (boolean): Plain terraform output for logs

**Commands:**
- `gh api repos/$GITHUB_REPO/actions/workflows --paginate | jq '.workflows[].path'`
- `terraform plan -no-color -out=/tmp/plan.tfplan && terraform show -json /tmp/plan.tfplan`
- `curl -s http://localhost:8080/metrics | grep -E 'job_last_success|up' | head -10`
- `kubectl get networkpolicies -A`
- `rg -i "auto.?scal|replica" terraform/ k8s/ | head -20`

**Examples:**
- gh api repos/$GITHUB_REPO/actions/runs --paginate | jq '.workflow_runs[0:5]'
- gitleaks detect --source . --report-path gitleaks-soc2.json
- kubectl get secrets -A | grep -c -v NAME

## References
- [AICPA SOC 2 overview](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2)
- [Trust Services Criteria](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2-soc-3-greater-than-trust-services-criteria)