---
name: "api-sec-sql-injection"
description: "Tests APIs for injection and parameter tampering: sqlmap for SQLi, manual payload probes, fuzzing inputs, and HTTP method abuse checks. Use when working with sql injection, method abuse or when the user mentions sql injection, method abuse."
license: "MIT"
compatibility: "Requires node.js, python, owasp-zap, helmet, cors. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(npx:*) Bash(sqlmap:*)"
---

Tests APIs for injection and parameter tampering: sqlmap for SQLi, manual payload probes, fuzzing inputs, and HTTP method abuse checks.

## Agentic Workflow: Read -> Reason -> Act (api-sec-sql-injection)

You are **Api Sec Sql Injection** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-sec-sql-injection`
- Domain: Tests APIs for injection and parameter tampering: sqlmap for SQLi, manual payload probes, fuzzing inputs, and HTTP method abuse checks.
- **sql-injection**: Detect SQL injection in API parameters — `sqlmap -u "http://localhost:8080/search?q=1" --batch --level=2`
- **method-abuse**: Test HTTP method handling and fuzzing — `curl -s -X OPTIONS http://localhost:8080/users -D- -o /dev/null | grep -i allow`
- Check `knowledge` and `prerequisites: node.js, python, owasp-zap`

### 2. Reason — think for `api-sec-sql-injection`
- For `sql-injection`: Detect SQL injection in API parameters — decide which checks to run
- For `method-abuse`: Test HTTP method handling and fuzzing — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-sec-sql-injection` tools
- Tools: `Glob`, `Grep`, `Read`, `Sqlmap`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-sec-sql-injection:56049570`

# API Security v3 - Injection Testing

Injection and tampering tests.

## What This Skill Does
- Automates SQLi detection with sqlmap
- Probes parameters manually
- Tests HTTP method and mass-assignment abuse

## When to Use
- Pentest-style API reviews
- New endpoint security checks
- Bug bounty triage

## Real Commands

```bash
sqlmap -u "https://api.example.com/search?q=1" --batch --level=2
curl -s "https://api.example.com/search?q=1'" | head -5
curl -s -X OPTIONS https://api.example.com/users -D- -o /dev/null | grep -i allow
```

## Test Checklist
- SQL injection on all query params
- Mass assignment on PUT/PATCH bodies
- Disallowed methods returning 200
- CRLF injection in headers

## Testing
- Use a disposable test database
- Limit payloads to non-destructive probes
- Document every finding with evidence

## Best Practices
- Only scan authorized environments
- Combine static review with dynamic probes
- Verify fixes with the same payloads

## Capabilities

### sql-injection
Detect SQL injection in API parameters

**Parameters:**
- `url` (string): Target URL with parameters
- `level` (integer): sqlmap test level 1-5
- `data` (string): POST body for parameter testing

**Commands:**
- `sqlmap -u "http://localhost:8080/search?q=1" --batch --level=2`
- `sqlmap -u "http://localhost:8080/login" --data "email=a&pass=b" --batch`
- `curl -s "http://localhost:8080/search?q=1'" | head -5`
- `curl -s "http://localhost:8080/search?q=1%20OR%201=1" -o /dev/null -w '%{http_code}\n'`

**Examples:**
- sqlmap --batch automates detection non-interactively
- --level=2 deepens payload testing
- curl with quotes probes for raw SQL errors

### method-abuse
Test HTTP method handling and fuzzing

**Commands:**
- `curl -s -X OPTIONS http://localhost:8080/users -D- -o /dev/null | grep -i allow`
- `curl -s -X TRACE http://localhost:8080/ -o /dev/null -w '%{http_code}\n'`
- `curl -s -X PATCH http://localhost:8080/users/1 -H 'Content-Type: application/json' -d '{"role":"admin"}' -w '\n%{http_code}\n'`
- `npx fuzzapi --target http://localhost:8080/users`

**Examples:**
- -cli --help
- -api --help

## References
- [sqlmap Docs](https://sqlmap.org/usage.html)
- [OWASP Injection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
