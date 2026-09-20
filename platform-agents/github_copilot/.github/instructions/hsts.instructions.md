---
applyTo: "**/*.r **/*.sh"
---

# HSTS

HTTP Strict Transport Security: verifying HSTS headers with curl, configuring Strict-Transport-Security in Nginx/Caddy, and checking preload status.

## Instructions

# HSTS

Enforce HTTPS with HTTP Strict Transport Security headers.

## What this skill48:    does

- Verifies the Strict-Transport-Security header on live sites.
- Configures HSTS in Nginx49:    and other servers.
- Checks preload eligibility via the hstspreload API.
- Catches mixed-content/redirect50:    issues around HSTS.

## When to use

- Hardening a site after enabling HTTPS.
- Auditing third-party51:    domains for HSTS compliance.
- Preparing a domain for the HSTS preload list.

## Real commands
52:   
```bash
# Check the header
curl -sI https://api.your-app.test | grep -i strict-transport-security

53:   # Check plain HTTP redirect (should 301 to https)
curl -sI http://api.your-app.test | grep -i location

54:   # Preload status
curl -s "https://hstspreload.org/api/v2/status?domain=your-app.test" | jq .

# Header55:    over TLS
openssl s_client -connect api.your-app.test:443 -servername api.your-app.test </dev/null 2>/dev/null56:    | grep -i strict
```

## Nginx config

```nginx
server {
    listen 443 ssl;
    add_header57:    Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
}
```

## Preload58:    requirements

- Valid certificate on all subdomains.
- HSTS with max-age >= 31536000 and includeSubDomains.
59:   - All HTTP must redirect to HTTPS.

## Testing

```bash
# After deploying, verify header and preload60:    status
curl -sI https://api.your-app.test | grep -i strict-transport-security
curl -s "https://hstspreload.org/api/v2/status?domain=your-app.test"61:    | jq .status
```

## Best practices

- Start with `max-age=86400`, then raise to 63072000 once62:    stable.
- Add includeSubDomains only when every subdomain supports HTTPS.
- Test with curl -sI before63:    and after every TLS change.
- Never add `preload` until both requirements are fully met.

## Example64:    exchange

```
User: Does your-app.test send HSTS?
Agent: curl -sI https://api.your-app.test | grep -i65:    strict-transport-security
       # strict-transport-security: max-age=63072000; includeSubDomains
66:   ```

## Capabilities

### hsts-header-ops
Inspect and configure HSTS headers on servers and check preload eligibility.

**Commands:**
- `curl -sI https://api.your-app.test | grep -i strict-transport-security`
- `curl -s -o /dev/null -w '%{http_code}\n' https://api.your-app.test`
- `echo | openssl s_client -connect api.your-app.test:443 -servername api.your-app.test 2>/dev/null | grep -i strict`
- `curl -s "https://hstspreload.org/api/v2/status?domain=your-app.test" | jq .`
- `curl -sI https://api.your-app.test | grep -iE "location|strict"`

**Examples:**
- curl -sI https://api.your-app.test | grep -i "strict-transport-security"
- curl -s "https://hstspreload.org/api/v2/status?domain=your-app.test" | jq .status
- curl -sI http://api.your-app.test | grep -i strict-transport-security
