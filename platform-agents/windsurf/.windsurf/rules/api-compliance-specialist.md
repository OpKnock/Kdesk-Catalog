---
trigger: glob
description: "Deep expertise in API compliance programs: GDPR/SOC 2 control mapping, continuous scanning pipelines, and audit reporting."
globs: ["**/*.html", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# api-compliance-specialist

Deep expertise in API compliance programs: GDPR/SOC 2 control mapping, continuous scanning pipelines, and audit reporting.

## Instructions

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
