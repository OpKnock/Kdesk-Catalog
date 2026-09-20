---
applyTo: "**/*.r **/*.sh"
---

Guides GDPR compliance work: data mapping, consent audit, breach response, and record keeping.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rg -i -n "(email|phone|ssn|passport|birth[_-]?date|ip_addres`
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

# GDPR

EU General Data Protection Regulation compliance skill: finds personal data, verifies
consent and deletion flows, and supports records of processing.

## When to Use

- Mapping where personal data lives before a DPIA
- Auditing consent capture and right-to-erasure flows
- Preparing Art. 30 records of processing activities
- Verifying data minimization and retention settings

## Real Commands

```bash
# Find where personal data fields are handled in code
rg -i -n "email|phone|birth_date|ssn|iban" src/ --glob '!*.test.*' --glob '!*.spec.*'

# Find cookie and tracking usage
rg -l -i "document.cookie|localStorage|analytics" public/ src/

# Check TLS in transit
openssl s_client -connect app.example.com:443 -servername app.example.com -brief

# Scan logs for leaked PII in CI artifacts
rg -l -i "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}" logs/ || echo 'no emails in logs'

# Retention: find delete paths
rg -i -n "deleteMany|destroy|delete\(" src/routes/users/
```

## Deliverables the skill produces

- PII inventory: field, endpoint, storage location, retention
- Consent audit: where collected, where stored, proof of opt-in
- Deletion audit: does erasure remove all copies (incl. backups)
- Processing records draft aligned with Art. 30

## Best Practices

- Document the lawful basis for each processing purpose
- Keep retention periods explicit and enforced by jobs
- Ensure breach detection: alerting on unusual data exports
- Encrypt at rest and in transit; scope access by role
- Provide export (Art. 20) and erasure (Art. 17) endpoints for user data

## Example Response

The agent returns a PII map with file:line references, a gap list (missing consent
records, deletion flows), and concrete remediation steps per article.

## Capabilities

### gdpr-audit
Find personal data in code, audit consent, and verify security controls

**Parameters:**
- `glob` (string): File pattern filter for the personal-data scan
- `audit` (boolean): Produce a report instead of interactive output
- `source` (string): Directory to scan for secrets and personal data

**Commands:**
- `rg -i -n "(email|phone|ssn|passport|birth[_-]?date|ip_address)" src/ --glob '!*.test.*'`
- `git grep -l -i "personal data" config/`
- `node scripts/check-cookies.js --audit`
- `gitleaks detect --source . --no-banner`
- `rg -l -i "gdpr|art. 30|roppa" docs/ records/`

**Examples:**
- rg -n 'user\.email' src/ | wc -l
- npx cookie-checker --scan .
- openssl s_client -connect example.com:443 -servername example.com -brief

## References
- [GDPR text (EUR-Lex)](https://gdpr-info.eu/)
- [EDPB guidelines](https://www.edpb.europa.eu/)
