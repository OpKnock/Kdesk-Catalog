---
name: "passwordless"
description: "Passwordless authentication: magic links, email OTPs, TOTP codes, and verification endpoints. Use when working with passwordless flows, api or when the user mentions passwordless flows, api."
license: "MIT"
compatibility: "Requires oathtool. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(oathtool:*)"
---

Passwordless authentication: magic links, email OTPs, TOTP codes, and verification endpoints.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST http://localhost:3000/auth/magic-link -d '{"ema`
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
