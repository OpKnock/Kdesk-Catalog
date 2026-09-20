---
name: "api-sec-tls-certificates"
description: "Audits API transport security: TLS certificate validation with openssl, SSL/TLS configuration scanning with testssl.sh and sslyze, and header checks. Use when working with tls certificates, config scans or when the user mentions tls certificates, config scans."
---

Audits API transport security: TLS certificate validation with openssl, SSL/TLS configuration scanning with testssl.sh and sslyze, and header checks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `echo | openssl s_client -connect api.example.com:443 -server`, `testssl.sh api.example.com`
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

# API Security v4 - TLS

Transport security auditing.

## What This Skill Does
- Verifies certificate validity and chain
- Scans cipher and protocol support
- Checks security response headers

## When to Use
- Certificate renewal verification
- PCI compliance evidence
- Post-incident transport review

## Real Commands

```bash
echo | openssl s_client -connect api.example.com:443 -servername api.example.com 2>/dev/null | openssl x509 -noout -subject -dates -issuer
testssl.sh api.example.com
npx sslyze api.example.com --certinfo
```

## Checks
- Certificate expiry and SANs
- TLS 1.2/1.3 enabled, 1.0/1.1 disabled
- Weak ciphers negotiated
- HSTS header present

## Testing
- Test from external networks to see public config
- Compare staging and production configs
- Re-test after any config change

## Best Practices
- Enforce TLS 1.2+ and modern ciphers
- Send HSTS with a long max-age
- Automate expiry monitoring

## Capabilities

### tls-certificates
Inspect TLS certificates and handshakes

**Parameters:**
- `host` (string): Target hostname
- `port` (integer): TLS port, default 443
- `protocol` (string): TLS version to test

**Commands:**
- `echo | openssl s_client -connect api.example.com:443 -servername api.example.com 2>/dev/null | openssl x509 -noout -subject -dates -issuer`
- `echo | openssl s_client -connect api.example.com:443 -tls1_2 -servername api.example.com 2>/dev/null | grep -E 'Protocol|Cipher'`
- `curl -sI http://localhost:8080 | grep -iE 'strict-transport|content-security'`
- `npx sslyze api.example.com --certinfo`

**Examples:**
- openssl s_client extracts certificate details
- -tls1_2 forces the protocol for version checks
- sslyze --certinfo reports cert chain issues

### config-scans
Scan TLS configuration with testssl.sh

**Commands:**
- `testssl.sh api.example.com`
- `testssl.sh --hints api.example.com`
- `testssl.sh --ssl-native api.example.com`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/health`

**Examples:**
- -cli --help
- -api --help

## References
- [OpenSSL s_client](https://docs.openssl.org/master/man1/openssl-s_client/)
- [testssl.sh](https://testssl.sh/)
