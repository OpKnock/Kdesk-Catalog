Verify security controls required handling PHI systems. and BAAs.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openssl s_client -connect app.example.com:443 -tls1_2 -brief`
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

# HIPAA

Health Insurance Portability and Accountability Act compliance for systems that
create, receive, or transmit protected health information (PHI).

## When to Use

- Pre-launch security review of a health app
- Verifying encryption, audit logging, and access controls
- Preparing for a Security Risk Assessment (SRA)

## Real Commands

```bash
# Verify encryption in transit
openssl s_client -connect app.example.com:443 -tls1_2 -brief
curl -sI https://app.example.com | grep -i strict-transport-security

# Check encryption at rest posture (via config review)
rg -i "encrypt|kms|aes" config/ docker-compose.yml

# Scan for secrets that could expose PHI databases
trufflehog filesystem .
gitleaks detect --source .

# Verify audit log endpoint requires auth
curl -s -o /dev/null -w '%{http_code}' https://app.example.com/api/audit-logs

# Minimum necessary access: review roles
rg -i -n "role|scope|permission" src/auth/ | head -30
```

## Key Safeguards Checklist

- Access: unique user IDs, role-based access, automatic logoff
- Audit: record who accessed PHI, when, and why
- Integrity: mechanisms to verify PHI isn't altered
- Transmission: encryption in transit (TLS 1.2+)
- Breach: notification procedures and BAA on file with vendors

## Best Practices

- Never log PHI fields; log IDs only
- Encrypt databases and backups (AES-256) and rotate keys
- Sign Business Associate Agreements with every vendor touching PHI
- Run the SRA annually and after major changes
- Restrict PHI access to minimum necessary role scope

## Example Response

The agent produces a controls matrix (encryption, audit, access) with evidence
from the commands run, flags gaps, and lists the exact remediation steps.

## Capabilities

### hipaa-controls
Verify security controls required for PHI systems

**Parameters:**
- `tls1_2` (boolean): Require TLS 1.2 or higher for the connection test
- `no-update` (boolean): Run trufflehog without checking for updates
- `verbose` (boolean): Show full secret-scan details

**Commands:**
- `openssl s_client -connect app.example.com:443 -tls1_2 -brief`
- `curl -sI http://localhost:8080 | grep -i strict-transport-security`
- `trufflehog filesystem . --no-update`
- `gitleaks detect --source . --verbose`
- `curl -s http://localhost:8080/api/audit-logs -o /dev/null -w '%{http_code}\n'`

**Examples:**
- rg -i "phi|medical|health|diagnosis" src/ | wc -l
- curl -s -o /dev/null -w '%{http_code}' -u $SA_TOKEN http://localhost:8080/api/audit-logs
- nmap -Pn -p443 --script ssl-enum-ciphers app.example.com

## References
- [HHS HIPAA official site](https://www.hhs.gov/hipaa/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)