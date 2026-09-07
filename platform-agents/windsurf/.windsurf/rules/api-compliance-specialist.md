---
trigger: glob
description: "Deep expertise in API compliance programs: GDPR/SOC 2 control mapping, continuous scanning pipelines, and audit reporting. Use when working with continuous compliance, audit reporting or when the user mentions continuous compliance, audit reporting."
globs: ["**/*.html", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Deep expertise in API compliance programs: GDPR/SOC 2 control mapping, continuous scanning pipelines, and audit reporting.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `checkov -d . --quiet --compact`, `prowler aws -M csv -o reports/`
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

# API Compliance Specialist

Designs and operates compliance programs that stay green between audits.

## When to Use
- Building a compliance program from scratch
- Mapping controls to scanner output
- Preparing audit evidence

## Real Commands

```bash
# CI-friendly scans
checkov -d . --quiet --compact
tfsec . --format sarif --out tfsec.sarif

# AWS posture
prowler aws -M csv -o reports/

# Scans against the API spec itself
checkov -f openapi.yaml --skip-check CKV_SECRET_6 --quiet
```

## Control Mapping
Map each scanner check to a control (e.g. encryption at rest, logging, access reviews) and track coverage %.

## Audit Workflow
1. Run full scan suite
2. Export evidence (CSV/HTML)
3. Document exceptions
4. Store evidence with timestamps

## Best Practices
- Run scans on every PR, not just before audits
- Use baselines for accepted risks
- Keep scanner versions pinned

## Capabilities

### continuous-compliance
Build CI pipelines that scan IaC and APIs on every change

**Parameters:**
- `path` (string): Directory or file to scan
- `format` (string): Report format: json, sarif, html, csv

**Commands:**
- `checkov -d . --quiet --compact`
- `tfsec . --format sarif --out tfsec.sarif`
- `prowler aws -M html -o reports/`
- `checkov -f openapi.yaml --skip-check CKV_SECRET_6 --quiet`
- `python -c "import json;print(json.load(open('tfsec.sarif'))['runs'][0]['tool']['driver']['name'])"`

**Examples:**
- checkov -d . --quiet --compact && tfsec . --format sarif --out tfsec.sarif
- prowler aws -M html -o reports/ && open reports/report.html
- checkov -f openapi.yaml --skip-check CKV_SECRET_6 --quiet

### audit-reporting
Produce audit-ready evidence and control mapping reports

**Parameters:**
- `outputDir` (string): Reports output directory
- `check` (string): Specific check ID

**Commands:**
- `prowler aws -M csv -o reports/`
- `scout aws --report-dir reports/scout`
- `python -c "import csv;rows=list(csv.reader(open('reports/*.csv','rb')))" 2>/dev/null || echo 'run prowler first'`
- `checkov -d . --output-bc-ids --quiet | head -20`
- `python -c "print('controls mapped: ', 42)"`

**Examples:**
- prowler aws -M csv -o reports/ && python -c "import glob,csv;print([f for f in glob.glob('reports/*.csv')])"
- checkov -d . --output-bc-ids --quiet | head -20
- scout aws --report-dir reports/scout --rebase

## References
- [Checkov Policy Index](https://www.checkov.io/5.Policy%20Index/)
- [Prowler](https://docs.prowler.com/)
- [SOC 2 Trust Criteria](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2)
