Generate and verify RFC 6238 time-based one-time passwords using oathtool and Python's pyotp. Produces 6 or 8-digit codes from base32 secrets, verifies with configurable time windows for clock skew, and outputs otpauth URIs for QR code enrollment — all without a physical authenticator device.

## Agentic Workflow: Read -> Reason -> Act (totp)

You are **Totp** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `totp`
- Domain: Generate and verify RFC 6238 time-based one-time passwords using oathtool and Python's pyotp. Produces 6 or 8-digit codes from base32 secrets, verifies with configurable time windows for clock skew, a
- **totp-codes**: Generate and verify RFC 6238 TOTP codes — `oathtool --totp --base32 "JBSWY3DPEHPK3PXP"`
- Check `knowledge` and `prerequisites: oathtool, python`

### 2. Reason — think for `totp`
- For `totp-codes`: Generate and verify RFC 6238 TOTP codes — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `totp` tools
- Tools: `Glob`, `Grep`, `Read`, `Oathtool`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `totp:706a3030`

# TOTP

Hand-crafted skill for time-based one-time passwords (RFC 6238).

## What this skill does

- Generates 6/8-digit codes from a base32 secret
- Verifies codes with a time window for clock skew
- Produces secrets and codes from Python with pyotp

## When to use

- Testing 2FA flows without a phone
- Verifying TOTP secrets during onboarding
- Building authenticator-app compatible logins

## Real commands

```bash
# Current 6-digit code
oathtool --totp --base32 "JBSWY3DPEHPK3PXP"

# 8 digits
oathtool --totp -d 8 --base32 "JBSWY3DPEHPK3PXP"

# Verify including +/- 3 steps for skew
oathtool --totp --window 3 --base32 "JBSWY3DPEHPK3PXP"

# Python
python -c 'import pyotp; print(pyotp.TOTP("JBSWY3DPEHPK3PXP").now())'
python -c 'import pyotp; print(pyotp.TOTP("JBSWY3DPEHPK3PXP").verify("123456"))'
```

## Secret handling

- Secrets are base32-encoded (A-Z 2-7)
- The QR code URI: otpauth://totp/App:user?secret=JBSWY3DPEHPK3PXP&issuer=App
- Never log secrets; derive them from key material at rest

## Testing

```bash
CODE=$(oathtool --totp --base32 "JBSWY3DPEHPK3PXP")
python -c "import pyotp; print(pyotp.TOTP('JBSWY3DPEHPK3PXP').verify('$CODE'))"
```

## Best practices

- Use a window of 1-3 steps only; larger windows weaken security
- Hash secrets and codes at rest, never store plaintext
- Accept one code once: track used codes per 30s step

## Capabilities

### totp-codes
Generate and verify RFC 6238 TOTP codes

**Parameters:**
- `secret_base32` (string): Base32-encoded shared secret
- `digits` (integer): Code length, 6 or 8
- `window` (integer): Steps before/after current allowed for verification

**Commands:**
- `oathtool --totp --base32 "JBSWY3DPEHPK3PXP"`
- `oathtool --totp -d 8 --base32 "JBSWY3DPEHPK3PXP"`
- `oathtool --totp --window 3 --base32 "JBSWY3DPEHPK3PXP"`
- `python -c 'import pyotp; print(pyotp.TOTP("JBSWY3DPEHPK3PXP").now())'`
- `python -c 'import pyotp; print(pyotp.TOTP("JBSWY3DPEHPK3PXP").verify("123456"))'`

**Examples:**
- oathtool --totp --base32 "JBSWY3DPEHPK3PXP"
- python -c 'import pyotp; print(pyotp.TOTP("JBSWY3DPEHPK3PXP").now())'
- python -c 'import pyotp; print(pyotp.TOTP("JBSWY3DPEHPK3PXP", interval=30).verify(input()))'

## References
- [RFC 6238 TOTP](https://www.rfc-editor.org/rfc/rfc6238)
- [oathtool manual](https://www.nongnu.org/oath-toolkit/oathtool.1.html)