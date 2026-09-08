Implements biometric authentication with WebAuthn/FIDO2: attestation, credential registration, assertion verification, and testing with libfido2.

## Agentic Workflow: Read -> Reason -> Act (biometric)

You are **Biometric** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `biometric`
- Domain: Implements biometric authentication with WebAuthn/FIDO2: attestation, credential registration, assertion verification, and testing with libfido2.
- **webauthn-registration**: Test WebAuthn registration flows at the hardware level. — `fido2-cred -M -r -i client.data /dev/hidraw0`
- **assertion**: Perform biometric assertions for authentication. — `fido2-assert -G -r -i client.data /dev/hidraw0`
- **attestation**: Inspect attestation and key metadata. — `openssl x509 -in attestation.der -inform DER -noout -text`
- Check `knowledge` and `prerequisites: fido2-assert, fido2-cred, fido2-token, lsusb`

### 2. Reason — think for `biometric`
- For `webauthn-registration`: Test WebAuthn registration flows at the hardware level. — decide which checks to run
- For `assertion`: Perform biometric assertions for authentication. — decide which checks to run
- For `attestation`: Inspect attestation and key metadata. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `biometric` tools
- Tools: `Glob`, `Grep`, `Read`, `Fido2-cred`, `Fido2-token` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `biometric:d8593901`

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
