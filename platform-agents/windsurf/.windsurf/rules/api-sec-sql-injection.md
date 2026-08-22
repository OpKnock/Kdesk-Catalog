---
trigger: glob
description: "Tests APIs for injection and parameter tampering: sqlmap for SQLi, manual payload probes, fuzzing inputs, and HTTP method abuse checks."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.sql"]
---

# Api Sec Sql Injection

Tests APIs for injection and parameter tampering: sqlmap for SQLi, manual payload probes, fuzzing inputs, and HTTP method abuse checks.

## Instructions

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
