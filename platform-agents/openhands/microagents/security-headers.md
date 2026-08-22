---
name: "security-headers"
description: "Hardens HTTP responses by configuring and verifying security headers including CSP, HSTS, X-Frame-Options, Referrer-Policy, and X-Content-Type-Options. Validates implementations with curl and scores compliance using Mozilla Observatory."
type: knowledge
triggers: ["security-headers", "http-header-hardening"]
---

# Security Headers

Hardens HTTP responses by configuring and verifying security headers including CSP, HSTS, X-Frame-Options, Referrer-Policy, and X-Content-Type-Options. Validates implementations with curl and scores compliance using Mozilla Observatory.

## Instructions

# Security Headers

Hardens HTTP responses by configuring and verifying security headers.

## What this skill does

- Verifies which security headers a site sends using curl
- Configures headers in nginx, application middleware, and CDN edge
- Scores the site with Mozilla Observatory to track compliance progress

## When to use

- Adding headers after a penetration test finding
- Pre-launch checklist for a public-facing site or API
- Proving header coverage to compliance auditors
- Debugging CSP violations in browser console

## Real commands

```bash
# What headers does the site send?
curl -sI https://httpbin.org/headers | grep -iE 'strict-transport-security|content-security-policy|x-frame-options|referrer-policy|x-content-type-options'

# CORS on a cross-origin request
curl -sI -H 'Origin: https://malicious.example.com' https://httpbin.org/headers | grep -i 'access-control-allow-origin'

# Automated score with Mozilla Observatory
npx @mozilla/observatory-cli --host httpbin.org --rescan

# TLS version in use
curl -s -o /dev/null -w '%{ssl_protocol}\n' https://httpbin.org/
```

## nginx configuration

```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; img-src 'self' data: https:;" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header X-Content-Type-Options "nosniff" always;
```

## Testing

```bash
curl -sI https://httpbin.org/headers | grep -i x-frame-options
curl -sI https://httpbin.org/headers | grep -i content-security-policy
```

## Best practices

- Deploy HSTS only after HTTPS is stable; it is sticky and hard to undo
- Use the `always` keyword in nginx so error pages get headers too
- Re-run the Observatory scan after each header change
- Start CSP in report-only mode: `Content-Security-Policy-Report-Only`

## Capabilities

### http-header-hardening
Configure and verify HTTP security headers

**Commands:**
- `curl -sI https://httpbin.org/headers | grep -iE 'strict-transport-security|content-security-policy|x-frame-options|referrer-policy|x-content-type-options'`
- `curl -sI -H 'Origin: https://example.invalid' https://httpbin.org/headers | grep -i 'access-control-allow-origin'`
- `npx @mozilla/observatory-cli --host httpbin.org --rescan`
- `curl -s -o /dev/null -w '%{ssl_protocol}\n' https://httpbin.org/`

**Examples:**
- curl -sI https://httpbin.org/headers | grep -i x-frame-options
- curl -sI https://httpbin.org/headers | grep -i content-security-policy
- npx @mozilla/observatory-cli --host httpbin.org
