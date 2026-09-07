---
name: "api-compliance-engineer"
description: "Implements GDPR/SOC 2 controls in API code and config: data minimization, retention, encryption, and audit logging. Use when working with data protection, audit logging or when the user mentions data protection, audit logging."
license: "MIT"
compatibility: "Requires scout-suite, prowler, checkov, tfsec, node.js, python. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(node:*) Bash(openssl:*) Bash(python:*)"
---

Implements GDPR/SOC 2 controls in API code and config: data minimization, retention, encryption, and audit logging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openssl rand -base64 32`, `node -e "console.log(JSON.stringify({ts:Date.now(),user:'u1'`
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

# API Compliance Engineer

Implements compliance controls directly in API code and config.

## When to Use
- GDPR data handling in APIs
- SOC 2 control implementation
- Data minimization and retention

## Real Commands

```bash
# Key material
openssl rand -base64 32

# Hashing for searchable fields
node -e "const c=require('crypto');const h=c.createHash('sha256');console.log(h.update('email@example.com').digest('hex').slice(0,16))"

# AES-GCM encryption
node -e "const c=require('crypto');const iv=c.randomBytes(16);const ciph=c.createCipheriv('aes-256-gcm',c.randomBytes(32),iv);console.log('enc ok')"

# Audit event
node -e "console.log(JSON.stringify({ts:Date.now(),user:'u1',action:'read',resource:'orders/42',outcome:'allow'}))"
```

## Control Checklist
- Encrypt PII at rest and in transit
- Mask PII in logs
- Log access to sensitive endpoints
- Retention policy enforced in code

## Testing
Verify no PII appears in raw logs after requests.

## Best Practices
- Minimize PII in responses by default
- Never log full tokens or PII

## Capabilities

### data-protection
Apply encryption, masking, and retention controls to API data

**Parameters:**
- `algorithm` (string): Encryption algorithm
- `field` (string): Field to protect

**Commands:**
- `openssl rand -base64 32`
- `node -e "const c=require('crypto');const k=c.randomBytes(32);console.log('key bytes:',k.length)"`
- `node -e "const c=require('crypto');const h=c.createHash('sha256');console.log(h.update('email@localhost').digest('hex').slice(0,16))"`
- `python -c "import hashlib;print(hashlib.sha256(b'email@localhost').hexdigest()[:16])"`
- `node -e "const c=require('crypto');const iv=c.randomBytes(16);const ciph=c.createCipheriv('aes-256-gcm',c.randomBytes(32),iv);console.log('enc ok')"`

**Examples:**
- node -e "const c=require('crypto');const k=c.randomBytes(32);console.log('key bytes:',k.length)"
- python -c "import hashlib;print(hashlib.sha256(b'email@localhost').hexdigest()[:16])"
- openssl rand -base64 32

### audit-logging
Log access and data events for compliance evidence

**Parameters:**
- `user` (string): Acting user
- `action` (string): Audited action

**Commands:**
- `node -e "console.log(JSON.stringify({ts:Date.now(),user:'u1',action:'read',resource:'orders/42',outcome:'allow'}))"`
- `curl -s -X POST http://localhost:3000/api/audit -H 'Content-Type: application/json' -d '{"user":"u1","action":"export"}' -w '\n%{http_code}'`
- `python -c "import json,datetime;print(json.dumps({'ts':datetime.datetime.now().isoformat(),'action':'login'}))"`
- `node -e "console.log('retention: 90d hot, 365d cold')"`
- `curl -s http://localhost:3000/api/audit/search?user=u1 | python -m json.tool`

**Examples:**
- node -e "console.log(JSON.stringify({ts:Date.now(),user:'u1',action:'read',resource:'orders/42',outcome:'allow'}))"
- curl -s http://localhost:3000/api/audit/search?user=u1 | python -m json.tool
- python -c "import json,datetime;print(json.dumps({'ts':datetime.datetime.now().isoformat(),'action':'login'}))"

## References
- [GDPR Guide](https://gdpr-info.eu/)
- [OWASP Data Protection](https://owasp.org/www-project-data-protection/)
