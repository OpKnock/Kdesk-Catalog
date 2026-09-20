---
applyTo: "**/*.py **/*.r **/*.rs **/*.sh"
---

Expert SAML 2.0 reference covering signing and verifying assertions with xmlsec1, base64-decoding SAMLResponses, exchanging metadata, and wiring SP-initiated login.

## Agentic Workflow: Read -> Reason -> Act (saml)

You are **Saml** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `saml`
- Domain: Expert SAML 2.0 reference covering signing and verifying assertions with xmlsec1, base64-decoding SAMLResponses, exchanging metadata, and wiring SP-initiated login.
- **saml-assertion-tooling**: Sign, verify, and decode SAML assertions with xmlsec1 and openssl — `xmlsec1 --verify --pubkey-cert-pem sp-cert.pem saml-response.xml`
- Check `knowledge` and `prerequisites: openssl, python, xmlsec1`

### 2. Reason — think for `saml`
- For `saml-assertion-tooling`: Sign, verify, and decode SAML assertions with xmlsec1 and openssl — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `saml` tools
- Tools: `Glob`, `Grep`, `Read`, `Xmlsec1`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `saml:a3b50033`

# SAML 2.0

Expert skill for debugging and building SAML 2.0 SSO.

## What this skill does

- Verifies XML-DSig signatures on SAML assertions with xmlsec1
- Decodes base64 SAMLResponses to inspect their XML
- Posts SAMLResponses to the Assertion Consumer Service endpoint

## When to use

- SP cannot validate an IdP-issued assertion
- Analyzing why a login fails: signature, audience, or expiry
- Testing an ACS endpoint without a browser flow

## Real commands

```bash
# Verify a signature against the IdP certificate
xmlsec1 --verify --pubkey-cert-pem idp-cert.pem saml-response.xml

# Sign an unsigned assertion (IdP side)
xmlsec1 --sign --privkey-pem idp-key.pem --pubkey-pem idp-cert.pem --output signed.xml unsigned-assertion.xml

# Decode the base64 SAMLResponse from the browser POST
python -c 'import base64; print(base64.b64decode(open("saml-response.b64").read()).decode())'

# Simulate the ACS POST
curl -d "SAMLResponse=$(cat saml-response.b64)" https://app.your-app.test/acs

# Compare certificates
openssl x509 -in idp-cert.pem -noout -fingerprint -sha256
```

## Checking an assertion

- Confirm the Issuer matches the IdP entity ID
- Confirm Conditions: NotBefore/NotOnOrAfter cover the current time
- Confirm AudienceRestriction lists your SP entity ID

## Testing

```bash
python -c 'import base64; print(base64.b64decode(open("saml-response.b64").read()).decode())' > response.xml
xmlsec1 --verify --pubkey-cert-pem idp-cert.pem response.xml
```

## Best practices

- Validate signature, audience, and NotOnOrAfter, in that order
- Never trust an unsigned assertion, even from a test IdP
- Rotate IdP certs before expiry; keep metadata current

## Capabilities

### saml-assertion-tooling
Sign, verify, and decode SAML assertions with xmlsec1 and openssl

**Parameters:**
- `cert_file` (string): PEM certificate used for verification
- `key_file` (string): Private key used for signing
- `acs_url` (string): Assertion Consumer Service endpoint

**Commands:**
- `xmlsec1 --verify --pubkey-cert-pem sp-cert.pem saml-response.xml`
- `xmlsec1 --sign --privkey-pem idp-key.pem --pubkey-pem idp-cert.pem --output signed.xml unsigned-assertion.xml`
- `python -c 'import base64; print(base64.b64decode(open("saml-response.b64").read()).decode())'`
- `curl -d "SAMLResponse=$(cat saml-response.b64)" https://app.your-app.test/acs`
- `openssl x509 -in idp-cert.pem -noout -fingerprint -sha256`

**Examples:**
- python -c 'import base64; print(base64.b64decode(open("saml-response.b64").read()).decode())'
- xmlsec1 --verify --pubkey-cert-pem sp-cert.pem signed.xml
- curl -d "SAMLResponse=$(cat saml-response.b64)" https://app.your-app.test/acs

## References
- [xmlsec1 documentation](https://www.aleksey.com/xmlsec/api.html)
- [SAML V2.0 standard](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf)
