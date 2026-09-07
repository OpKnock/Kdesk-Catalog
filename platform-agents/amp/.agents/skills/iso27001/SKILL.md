---
name: "iso27001"
description: "Supports ISO 27001 ISMS work: asset inventory, risk assessment, control verification, and evidence collection. Use when working with isms evidence, iso27001 or when the user mentions isms evidence, iso27001."
license: "MIT"
compatibility: "Requires docker, gitleaks, nmap, openssl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "compliance"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(docker:*) Bash(gitleaks:*) Bash(nmap:*) Bash(openssl:*)"
---

Supports ISO 27001 ISMS work: asset inventory, risk assessment, control verification, and evidence collection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nmap -sV -p 22,443,8443 --open 10.0.0.0/24`
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

# ISO 27001

Information Security Management System (ISMS) support: evidence gathering for
Annex A controls, asset inventories, and risk assessments.

## When to Use

- Collecting audit evidence for certification or surveillance audits
- Building the asset inventory (A.5.9)
- Verifying technical controls: patching, encryption, access (A.8)
- Preparing the Statement of Applicability (SoA)

## Real Commands

```bash
# Asset discovery on a subnet
nmap -sV -p 22,443,8443 --open 10.0.0.0/24 -oX assets.xml

# Patch level: check SSH versions
nmap -sV -p 22 10.0.0.5

# Secret hygiene evidence
sudo gitleaks detect --source . --report-path gitleaks.json

# Access control: review users
rg -i -n "admin|root" docker-compose.yml k8s/ | head -30

# Monitoring: metrics endpoint reachable
curl -s localhost:9090/metrics | head -5

# Backups: verify job runs
crontab -l && docker compose ps --format json
```

## Common Evidence Pack

- A.5.9 asset inventory (nmap -oX output + owner table)
- A.8.8 vulnerability management (nuclei/grype reports)
- A.8.9/A.8.10 secrets management (gitleaks report, vault config)
- A.8.16 monitoring (metrics, alert rules)
- A.8.13 backup policy + restore test logs

## Best Practices

- Keep the SoA honest: mark controls as applicable or not, with justification
- Tie every control to concrete evidence artifacts
- Schedule recurring scans so evidence has dates
- Document risk treatment: accept, mitigate, transfer, avoid
- Update the ISMS after infrastructure changes

## Example Response

Returns an evidence matrix mapping Annex A controls to artifacts collected
(scans, config excerpts), with gaps and risk-level suggestions.

## Capabilities

### isms-evidence
Collect security evidence for ISO 27001 Annex A controls

**Parameters:**
- `open` (boolean): Show only open ports in nmap output
- `report-path` (string): Where to write the secret-scan report
- `severity` (string): Nuclei severity filter, e.g. critical,high

**Commands:**
- `nmap -sV -p 22,443,8443 --open 10.0.0.0/24`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:9200/_cat/health`
- `openssl cipherlist -v tls1_2`
- `gitleaks detect --source . --report-path gitleaks.json`
- `docker compose ps --format json`

**Examples:**
- nuclei -l targets.txt -severity critical,high
- rg -i "password|api_key|secret" config/ --hidden
- curl -s localhost:9090/metrics | head -20

## References
- [ISO/IEC 27001 standard](https://www.iso.org/standard/27001)
- [Annex A control reference](https://www.iso.org/standard/27002)
