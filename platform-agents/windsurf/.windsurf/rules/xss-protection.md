---
trigger: glob
description: "Prevent cross-site scripting through your API responses: set Content-Security-Policy headers, sanitize and encode output, validate inputs, and scan with automated payloads. Use when working with xss hardening, api or when the user mentions xss hardening, api."
globs: ["**/*.html", "**/*.java", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
---

Prevent cross-site scripting through your API responses: set Content-Security-Policy headers, sanitize and encode output, validate inputs, and scan with automated payloads.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -sI https://httpbin.org/ | grep -i 'content-security-po`
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

**Parameters:**
- `policy` (string): Content-Security-Policy header value
- `payload` (string): Test payload containing markup
- `library` (string): Sanitizer: dompurify, owasp-html-sanitizer, bleach

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

## References
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [MDN Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
