Expert reference covering authenticated curl flows, TLS certificate verification, OWASP ZAP baseline scans, and rate-limit/authorization probing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -H "Authorization: Bearer $TOKEN" https://api.your-a`
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

# REST API Security

Expert skill for securing and auditing REST APIs.

## What this skill does

- Verifies auth enforcement: unauthenticated requests must be rejected
- Checks TLS configuration and certificate expiry
- Runs automated baseline scans with OWASP ZAP

## When to use

- Before exposing a new endpoint to production traffic
- After an incident involving leaked credentials
- Periodic compliance checks of API posture

## Real commands

```bash
# Does the endpoint require auth? (expect 401/403)
curl -s -o /dev/null -w '%{http_code}\n' https://api.your-app.test/v1/users

# Authenticated call
curl -s -H "Authorization: Bearer $TOKEN" https://api.your-app.test/v1/users

# TLS: protocol, cipher, certificate dates
curl -skI https://api.your-app.test/ -o /dev/null -w '%{ssl_protocol} %{ssl_verify_result}\n'
openssl s_client -connect api.your-app.test:443 -servername api.your-app.test 2>/dev/null | openssl x509 -noout -dates

# Automated passive scan
zap-baseline.py -t https://staging.your-app.test -r zap-report.html

# Verify authorization: low-privilege token must not delete resources
curl -s -o /dev/null -w '%{http_code}\n' -X DELETE https://api.your-app.test/v1/orders/1 -H "Authorization: Bearer $LOW_PRIV_TOKEN"
```

## Rate limit check

```bash
for i in $(seq 1 60); do curl -s -o /dev/null -w '%{http_code} ' http://localhost:8080/api; done
# Expect 429s after the configured burst
```

## Testing

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://staging.your-app.test/healthz
```

## Best practices

- Never ship endpoints that succeed without auth; test it explicitly
- Require TLS 1.2+ and rotate certs before expiry
- Run the ZAP baseline in CI on every staging deploy

## Capabilities

### rest-api-hardening
Probe and harden REST APIs: auth, TLS, scanning, rate limits

**Parameters:**
- `token` (string): Bearer token for authenticated requests
- `target` (string): Base URL to scan or probe
- `report` (string): Output file for the ZAP scan report

**Commands:**
- `curl -s -H "Authorization: Bearer $TOKEN" https://api.your-app.test/v1/users`
- `curl -skI https://api.your-app.test/ -o /dev/null -w '%{http_code} %{ssl_verify_result}\n'`
- `openssl s_client -connect api.your-app.test:443 -servername api.your-app.test 2>/dev/null | openssl x509 -noout -dates`
- `zap-baseline.py -t https://staging.your-app.test -r zap-report.html`
- `curl -s -o /dev/null -w '%{http_code}\n' -X DELETE https://api.your-app.test/v1/orders/1 -H "Authorization: Bearer $TOKEN"`

**Examples:**
- curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' -X POST https://api.your-app.test/v1/login -d '{"user":"admin","pass":"wrong"}'
- curl -s -o /dev/null -w '%{http_code}\n' https://api.your-app.test/v1/users
- zap-baseline.py -t https://staging.your-app.test -r zap-report.html

## References
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [ZAP Baseline Scan](https://www.zaproxy.org/docs/docker/baseline-scan/)