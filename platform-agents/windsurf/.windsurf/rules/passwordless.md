---
trigger: glob
description: "Passwordless authentication: magic links, email OTPs, TOTP codes, and verification endpoints."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Passwordless

Passwordless authentication: magic links, email OTPs, TOTP codes, and verification endpoints.

## Instructions

# Passwordless

Passwordless auth exchanges knowledge (passwords) for possession: email links, SMS codes, or TOTP apps.

## What this skill does

- Implements magic-link and OTP request/verify endpoints
- Generates and validates TOTP codes
- Handles token expiry and rate limiting

## When to use

- Reducing password theft and phishing
- Low-friction onboarding

## Real commands

```bash
# Request a magic link
curl -X POST http://localhost:3000/auth/magic-link -d '{"email":"user@example.com"}' -H "Content-Type: application/json"

# Verify the token
curl -X POST http://localhost:3000/auth/verify-token -d '{"email":"user@example.com","token":"123456"}' -H "Content-Type: application/json"

# Generate a TOTP code locally
 oathtool --totp -b JBSWY3DPEHPK3PXP
```

## Flow rules

- Tokens expire in 5-15 minutes and are single-use
- Rate-limit request endpoints per email/phone
- Always bind tokens to the verified identity

## Best practices

- Return generic responses to avoid enumeration
- Log login events for audit
- Fall back to TOTP when email/SMS channels are unreliable

## Capabilities

### passwordless-flows
Implement magic-link and OTP flows: request codes, verify codes, and TOTP generation.

**Commands:**
- `curl -X POST http://localhost:3000/auth/magic-link -d '{"email":"alice@example.org"}' -H "Content-Type: application/json"`
- `curl -X POST http://localhost:3000/auth/verify-token -d '{"email":"alice@example.org","token":"847291"}' -H "Content-Type: application/json"`
- `oathtool --totp -b JBSWY3DPEHPK3PXP`
- `oathtool --totp --time-step-size 60 -b JBSWY3DPEHPK3PXP`
- `curl -X POST http://localhost:3000/auth/request-otp -d '{"phone":"+14155550123"}' -H "Content-Type: application/json"`

**Examples:**
- oathtool --totp -b JBSWY3DPEHPK3PXP
- curl -X POST http://localhost:3000/auth/verify-token -d '{"email":"user@example.com","token":"123456"}'
- curl -X POST http://localhost:3000/auth/magic-link -d '{"email":"user@example.com"}'
