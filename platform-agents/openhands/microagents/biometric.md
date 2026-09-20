---
name: "biometric"
description: "Implements biometric authentication with WebAuthn/FIDO2: attestation, credential registration, assertion verification, and testing with libfido2."
type: knowledge
triggers: ["biometric", "webauthn-registration", "assertion", "attestation"]
---

# Biometric

Implements biometric authentication with WebAuthn/FIDO2: attestation, credential registration, assertion verification, and testing with libfido2.

## Instructions

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
