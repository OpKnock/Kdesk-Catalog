---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Implements passwordless authentication using WebAuthn/FIDO2. Generates registration options, verifies attestation responses, asserts logins with @simplewebauthn, and inspects authenticator certificates with openssl.

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

# WebAuthn

## What this skill does

Implement passwordless, phishing-resistant authentication using WebAuthn/FIDO2. Covers generating registration options, verifying attestation responses, and asserting logins with @simplewebauthn.

## When to use

- Adding passkeys or security keys to an API
- Replacing passwords for web clients
- Verifying authenticator attestations server-side

## Real commands

```bash
# Install libraries
npm install @simplewebauthn/server @simplewebauthn/browser

# Fetch registration options
curl -s -X POST http://localhost:8080/auth/register/options -d "{\"username\":\"alice\"}" | jq ".publicKey.challenge"

# Verify the registration response server-side
node scripts/verify-registration.mjs attestation.json

# Login options
curl -s -X POST http://localhost:8080/auth/login/options -d "{\"username\":\"alice\"}" | jq ".publicKey.allowCredentials"

# Inspect the attestation cert (if one is provided)
openssl x509 -in attestation.der -inform DER -text -noout

# Verify assertion
node scripts/verify-assertion.mjs assertion.json challenge.json
```

## Server flow

1. Generate a challenge (>= 16 random bytes)
2. Return PublicKeyCredentialCreationOptions to the client
3. Receive attestation and call `verifyRegistrationResponse`
4. Store the credential ID and public key per user

## Best practices

- Persist the counter and reject decreasing counters
- Set `userVerification: preferred` for good UX with security
- Never store raw attestation objects longer than needed
- Use constant-time comparisons when checking signatures

## Testing

```bash
node scripts/generate-challenge.mjs > challenge.json
curl -s -X POST http://localhost:8080/auth/register/options -d "{\"username\":\"alice\"}" | jq ".publicKey"
```

## Capabilities

### webauthn-flow
Implement and test WebAuthn registration and login

**Parameters:**
- `rpID` (string): Relying Party ID, e.g. auth.example.com
- `origin` (string): Allowed origin for the WebAuthn ceremony
- `userVerification` (string): required, preferred, or discouraged

**Commands:**
- `npm install @simplewebauthn/server @simplewebauthn/browser`
- `openssl x509 -in attestation.der -inform DER -text -noout`
- `node scripts/generate-challenge.mjs`
- `curl -s -X POST http://localhost:8080/auth/register/options -d "{\"username\":\"alice\"}" | jq ".publicKey.challenge"`
- `node scripts/verify-registration.mjs attestation.json`

**Examples:**
- curl -s -X POST http://localhost:8080/auth/login/options -d "{\"username\":\"alice\"}" | jq ".publicKey.allowCredentials[0].id"
- node scripts/verify-assertion.mjs assertion.json challenge.json
- openssl x509 -in attestation.der -inform DER -noout -subject -issuer

## References
- [WebAuthn Guide](https://webauthn.guide/)
- [@simplewebauthn Docs](https://simplewebauthn.dev/docs/)
- [W3C WebAuthn spec](https://www.w3.org/TR/webauthn-2/)
