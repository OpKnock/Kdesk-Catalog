---
type: agent_requested
description: "Passkeys and WebAuthn: registration/authentication flows, relying party setup, and the SimpleWebAuthn libraries. Use when working with passkey integration, api or when the user mentions passkey integration, api."
---

Passkeys and WebAuthn: registration/authentication flows, relying party setup, and the SimpleWebAuthn libraries.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @simplewebauthn/server @simplewebauthn/browser`
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

# Passkeys

Passkeys replace passwords with device-bound WebAuthn credentials, protected by biometrics or PINs.

## What this skill does

- Implements registration (attestation) and login (assertion) endpoints
- Uses SimpleWebAuthn for ceremony verification
- Configures relying party settings

## When to use

- Passwordless login in web apps
- Removing passwords from accounts

## Real commands

```bash
# Dependencies
npm install @simplewebauthn/server @simplewebauthn/browser

# RP endpoints (dev server)
curl -s -X POST http://localhost:3000/register/start -d '{"email":"alice@example.com"}' -H 'Content-Type: application/json' | jq .
curl -s -X POST http://localhost:3000/login/start | jq '.options.publicKey'
```

## Server flow (Node)

```js
const { generateRegistrationOptions, verifyRegistrationResponse } = require('@simplewebauthn/server');

const options = await generateRegistrationOptions({
  rpName: 'MyApp',
  rpID: 'example.com',
  userName: user.email,
  timeout: 60000,
});
// send options to browser, then verify attestation response
const verification = await verifyRegistrationResponse({ response, expectedChallenge, expectedOrigin: 'https://example.com', expectedRPID: 'example.com' });
```

## Best practices

- Store challenge + user session server-side
- Verify expectedOrigin and expectedRPID strictly
- Always test in a real browser; localhost uses special origins

## Capabilities

### passkey-integration
Integrate WebAuthn passkeys into web apps: registration, authentication, and verification with SimpleWebAuthn.

**Parameters:**
- `rp_id` (string): Relying party ID (effective domain)
- `rp_name` (string): Relying party display name
- `origin` (string): Allowed origin(s) for attestation

**Commands:**
- `npm install @simplewebauthn/server @simplewebauthn/browser`
- `npm install @simplewebauthn/server --save`
- `curl -s -X POST http://localhost:3000/register/start | jq .`
- `curl -s -X POST http://localhost:3000/login/start | jq .options`
- `curl -sI https://webauthn.io | grep -i 'permissions-policy'`

**Examples:**
- curl -s -X POST http://localhost:3000/register/start -d '{"email":"alice@example.com"}' -H 'Content-Type: application/json' | jq .
- curl -s -X POST http://localhost:3000/login/start | jq '.options.publicKey'
- npm install @simplewebauthn/server

## References
- [Passkeys on Google](https://developers.google.com/identity/passkeys)
- [SimpleWebAuthn Docs](https://simplewebauthn.dev/docs/)