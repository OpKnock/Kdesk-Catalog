---
name: "passwordless"
description: "Passwordless authentication: magic links, email OTPs, TOTP codes, and verification endpoints. Use when working with passwordless flows, api or when the user mentions passwordless flows, api."
type: knowledge
triggers: ["passwordless", "passwordless-flows"]
---

Passwordless authentication: magic links, email OTPs, TOTP codes, and verification endpoints.

## Agentic Workflow: Read -> Reason -> Act (passwordless)

You are **Passwordless** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `passwordless`
- Domain: Passwordless authentication: magic links, email OTPs, TOTP codes, and verification endpoints.
- **passwordless-flows**: Implement magic-link and OTP flows: request codes, verify codes, and TOTP generation. — `curl -X POST http://localhost:3000/auth/magic-link -d '{"email":"alice@example.o`
- Check `knowledge` and `prerequisites: oathtool`

### 2. Reason — think for `passwordless`
- For `passwordless-flows`: Implement magic-link and OTP flows: request codes, verify codes, and TOTP generation. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `passwordless` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Oathtool` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `passwordless:f8e5924b`

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

**Parameters:**
- `channel` (string): email, sms or authenticator app
- `secret` (string): TOTP base32 secret
- `token` (string): Verification code

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

## References
- [RFC 6238 TOTP](https://datatracker.ietf.org/doc/html/rfc6238)
- [Passwordless Authentication (Auth0)](https://auth0.com/docs/authenticate/passwordless)
