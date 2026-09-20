---
type: agent_requested
description: "Implements GDPR/SOC 2 controls in API code and config: data minimization, retention, encryption, and audit logging."
---

# api-compliance-engineer

Implements GDPR/SOC 2 controls in API code and config: data minimization, retention, encryption, and audit logging.

## Instructions

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