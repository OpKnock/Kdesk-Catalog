# Passkey

Passkeys and WebAuthn: registration/authentication flows, relying party setup, and the SimpleWebAuthn libraries.

## Instructions

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
