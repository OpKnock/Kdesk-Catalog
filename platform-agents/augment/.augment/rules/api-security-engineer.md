---
type: agent_requested
description: "Engineers API security controls: OWASP Top 10 coverage, security headers, authentication middleware, dependency scanning with npm audit, and SAST with semgrep."
---

# api-security-engineer

Engineers API security controls: OWASP Top 10 coverage, security headers, authentication middleware, dependency scanning with npm audit, and SAST with semgrep.

## Instructions

# API Security Engineer

End-to-end API security controls.

## What This Skill Does
- Applies security headers at the framework level
- Scans dependencies and source for vulnerabilities
- Covers OWASP API Top 10 categories

## When to Use
- Hardening new API deployments
- Recurring vulnerability management
- Compliance evidence gathering

## Real Commands

```bash
npm install helmet
npm audit --audit-level=high
pip install semgrep
semgrep --config=p/owasp-top-ten .
```

## Header Baseline
- Strict-Transport-Security: max-age=31536000
- X-Content-Type-Options: nosniff
- Referrer-Policy: no-referrer
- Cache-Control: no-store on auth responses

## Testing
- Verify headers on every route prefix
- Re-run audits after dependency updates
- Keep semgrep findings triaged


## Best Practices
- Default-deny error responses
- Rate limit auth endpoints
- Scan in CI on every merge

## Capabilities

### security-headers
Apply and verify security response headers

**Commands:**
- `npm install helmet`
- `curl -sI http://localhost:8080/ | grep -iE 'strict-transport-security|content-security-policy|x-content-type-options|referrer-policy'`
- `curl -s -D- http://localhost:8080/api | grep -i 'x-frame-options'`
- `node -e "const helmet=require('helmet'); console.log(helmet()._name)"`

**Examples:**
- helmet sets a battery of security headers
- curl -sI greps HSTS and CSP headers
- X-Frame-Options blocks clickjacking

### dependency-sast
Scan dependencies and source code

**Commands:**
- `npm audit --audit-level=high`
- `npm audit fix --dry-run`
- `pip install semgrep`
- `semgrep --config=p/owasp-top-ten .`
- `semgrep --config=auto --json -o semgrep.json .`

**Examples:**
- npm audit reports vulnerable dependencies
- semgrep with owasp-top-ten rules scans source
- --json output feeds CI dashboards