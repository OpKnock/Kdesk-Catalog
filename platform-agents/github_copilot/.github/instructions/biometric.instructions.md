---
applyTo: "**/*.r **/*.sh"
---

Implements biometric authentication with WebAuthn/FIDO2: attestation, credential registration, assertion verification, and testing with libfido2.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `fido2-cred -M -r -i client.data /dev/hidraw0`, `fido2-assert -G -r -i client.data /dev/hidraw0`
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

# Biometric

## What this skill does

Implements biometric authentication using WebAuthn/FIDO2: registering authenticators with attestation, performing assertions, inspecting attestation certificates, and testing with libfido2 hardware tools.

## When to use

- Adding passkey/fingerprint login to an app
- Testing FIDO2 flows with real hardware
- Verifying attestation certificates from authenticators

## Real commands

```bash
# List tokens
fido2-token -L

# Make a credential (registration)
fido2-cred -M -r -i client.data -o cred /dev/hidraw0

# Verify the credential
fido2-cred -V -r -i client.data -o cred -c cred /dev/hidraw0

# Assert (login)
fido2-assert -G -r -i client.data -o assert /dev/hidraw0

# Inspect attestation cert
openssl x509 -in attestation.der -inform DER -noout -subject -issuer
```

## Testing

- Verify attestation chains with openssl x509 against vendor roots
- Exercise reject paths: wrong user presence, revoked credential

## Best practices

- Verify signature counters and origin in the RP
- Store only public keys and credential IDs, never biometric templates
- Offer fallback (password/TOTP) alongside biometrics
- Use a passkey provider SDK (e.g. WebAuthn lib) rather than raw hardware in production

## Capabilities

### webauthn-registration
Test WebAuthn registration flows at the hardware level.

**Parameters:**
- `device` (string): HID device path, e.g. /dev/hidraw0
- `client_data` (string): Client data JSON file

**Commands:**
- `fido2-cred -M -r -i client.data /dev/hidraw0`
- `fido2-cred -M -r -i client.data -o cred /dev/hidraw0`
- `fido2-token -L`
- `fido2-token -I /dev/hidraw0`
- `fido2-cred -V -r -i client.data -o cred -c cred /dev/hidraw0`

**Examples:**
- fido2-token -L | grep -i yubikey
- fido2-cred -M -r -i client.data -o cred /dev/hidraw0
- fido2-cred -V -r -i client.data -o cred -c cred /dev/hidraw0

### assertion
Perform biometric assertions for authentication.

**Parameters:**
- `device` (string): HID device path
- `assertion_file` (string): Output assertion file

**Commands:**
- `fido2-assert -G -r -i client.data /dev/hidraw0`
- `fido2-assert -G -r -i client.data -o assert /dev/hidraw0`
- `fido2-assert -V -r -i client.data -o assert -c cred /dev/hidraw0`
- `fido2-token -R /dev/hidraw0`

**Examples:**
- fido2-assert -G -r -i client.data -o assert /dev/hidraw0
- fido2-assert -V -r -i client.data -o assert -c cred /dev/hidraw0
- fido2-token -R /dev/hidraw0

### attestation
Inspect attestation and key metadata.

**Parameters:**
- `cert_file` (string): Attestation certificate file
- `format` (string): DER or PEM

**Commands:**
- `openssl x509 -in attestation.der -inform DER -noout -text`
- `openssl x509 -in attestation.der -inform DER -noout -subject -issuer`
- `fido2-token -I /dev/hidraw0`
- `fido2-cred -Q -r /dev/hidraw0`
- `lsusb | grep -i -E 'fido|yubikey|feitian'`

**Examples:**
- openssl x509 -in attestation.der -inform DER -noout -subject -issuer
- fido2-token -I /dev/hidraw0
- lsusb | grep -i fido

## References
- [WebAuthn Spec](https://www.w3.org/TR/webauthn-2/)
- [libfido2](https://github.com/Yubico/libfido2)
- [OWASP Biometrics](https://owasp.org/www-community/controls/Biometric_Authentication)
