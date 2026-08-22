---
trigger: glob
description: "Prevent cross-site scripting through your API responses: set Content-Security-Policy headers, sanitize and encode output, validate inputs, and scan with automated payloads."
globs: ["**/*.html", "**/*.java", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
---

# XSS Protection

Prevent cross-site scripting through your API responses: set Content-Security-Policy headers, sanitize and encode output, validate inputs, and scan with automated payloads.

## Instructions

# XSS Protection

## What this skill does
Prevent cross-site scripting through your API responses: set Content-Security-Policy headers, sanitize and encode output, validate inputs, and scan with automated payloads.

## When to use
- APIs that render user content (HTML, markdown, chat)
- Auditing reflected/stored XSS vectors
- Enabling CSP for frontends

## Real commands
```bash
# Check CSP header
curl -sI https://httpbin.org/ | grep -i 'content-security-policy'

# Stored XSS: submit a script payload
curl -s -X POST http://localhost:8080/api/echo \
  -H 'Content-Type: application/json' \
  -d '{"name":"<script>alert(1)</script>"}' | jq -r '.safeName'

# Ensure markup is neutralized
curl -s -X POST http://localhost:8080/api/echo \
  -H 'Content-Type: application/json' \
  -d '{"name":"<img src=x onerror=alert(1)>"}' | grep -c '<img'   # expect 0

# Sanitize server-side with DOMPurify
node -e "const D=require('isomorphic-dompurify');console.log(D.sanitize('<img src=x onerror=alert(1)>'))"

# Contextual output encoding in templates
node -e "const e=require('html-escape');console.log(e('<b>x</b>'))"
```

## Sample CSP header
```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'
```

## Defenses by layer
- Input: validate types/lengths; never trust markup
- Sanitization: allowlist tags/attributes (DOMPurify, bleach)
- Output: encode per context (HTML attr, JS, URL)
- Headers: CSP, X-Content-Type-Options: nosniff

## Best practices
- Default-deny CSP; loosen only with justification
- Encode at the boundary, not in the data
- Escape JSON strings correctly when embedding in HTML
- Scan all user-input endpoints with payload batteries

## Testing
```bash
curl -s -X POST http://localhost:8080/api/echo -d '{"name":"<script>alert(1)</script>"}' | grep -c script
curl -sI http://localhost:8080/ | grep -iE 'content-security-policy|x-frame-options'
```

## Capabilities

### xss-hardening
Audit and harden APIs against cross-site scripting

**Commands:**
- `curl -sI https://httpbin.org/ | grep -i 'content-security-policy'`
- `curl -s -X POST http://localhost:8080/api/echo -H 'Content-Type: application/json' -d '{"name":"javascript:alert(1)"}' | jq -r '.safeName'`
- `node -e "const s=require('html-escape'?);console.log(s)" `
- `npm install dompurify isomorphic-dompurify`
- `curl -s -X POST http://localhost:8080/api/echo -H 'Content-Type: application/json' -d '{"name":"javascript:alert(1)"}' | jq -r '.safeName'`

**Examples:**
- curl -sI http://localhost:8080/ | grep -iE 'x-frame-options|x-xss-protection'
- node -e "const DOMPurify=require('isomorphic-dompurify');console.log(DOMPurify.sanitize('<img src=x onerror=alert(1)>'))"
- curl -s -X POST http://localhost:8080/api/echo -d '{"name":"javascript:alert(1)"}' | jq '.safeName'
