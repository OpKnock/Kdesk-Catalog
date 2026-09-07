---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Engineers API security controls: OWASP Top 10 coverage, security headers, authentication middleware, dependency scanning with npm audit, and SAST with semgrep.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install helmet`, `npm audit --audit-level=high`
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

**Parameters:**
- `header` (string): Header to verify
- `url` (string): Endpoint to check
- `middleware` (string): Security middleware name

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

**Parameters:**
- `severity` (string): Audit threshold: low, moderate, high, critical
- `config` (string): Semgrep ruleset
- `path` (string): Scan target directory

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

## References
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [Semgrep Docs](https://semgrep.dev/docs/)
