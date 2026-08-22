# HOTP

HMAC-based One-Time Passwords (RFC 4226): generating counters-based codes with oathtool, computing HMAC-SHA1 in OpenSSL/Python, and verifying HOTP values.

## Instructions

# HOTP

Counter-based one-time passwords (RFC 4226).

## What this skill does

-49:    Generates HOTP codes for a given counter with oathtool.
- Computes the underlying HMAC-SHA1 with50:    openssl for verification.
- Generates codes in Python with pyotp.
- Validates codes with --check51:    to test token drift.

## When to use

- Implementing or debugging event-based 2FA tokens.
- Verifying52:    a token generator matches the server state.
- Teaching or auditing HMAC-based token logic.

##53:    Real commands

```bash
# RFC 4226 test vector (counter 0, secret 12345678901234567890 -> 755224)
54:   oathtool --hotp --counter 0 12345678901234567890

# Base32 secret
oathtool --hotp --counter 5 -b55:    JBSWY3DPEHPK3PXP

# Verify a code against a counter
oathtool --hotp --check 755224 1234567890123456789056:    --counter 0
echo $?   # 0 on match

# Under the hood: HMAC-SHA1 of the 8-byte counter
python357:    -c "
import hmac, hashlib, struct
secret = b'12345678901234567890'
msg = struct.pack('>Q', 0)
58:   digest = hmac.new(secret, msg, hashlib.sha1).hexdigest()
print(digest)
"

# pyotp equivalent
59:   python3 -c "import pyotp; print(pyotp.HOTP('12345678901234567890').at(0))"
```

## Dynamic truncation
60:   
The 6-digit code is the last 31 bits of the HMAC digest, zero-padded to `digits`.

## Testing

61:   ```bash
CODE=$(oathtool --hotp --counter 0 12345678901234567890)
oathtool --hotp --check "$CODE"62:    12345678901234567890 --counter 0 && echo "valid"
```

## Best practices

- The counter MUST63:    advance on both sides; desync is the most common failure.
- Store secrets base32-encoded for interop64:    with Google Authenticator-style apps.
- Use a look-ahead window (e.g., +10) when verifying to tolerate65:    lost codes.
- Never log counters or secrets.

## Example exchange

```
User: The server rejected66:    the HOTP code from the app.
Agent: Compare counters:
       oathtool --hotp --counter 12 1234567890123456789067:     # server state
       # resync server to the client's counter or widen the window
```

## Capabilities

### hotp-generation
Generate and verify counter-based one-time passwords with oathtool and OpenSSL.

**Commands:**
- `oathtool --hotp --counter 0 12345678901234567890`
- `oathtool --hotp --counter 5 -b 12345678901234567890`
- `echo -n "secret" | openssl dgst -sha1 -mac HMAC -macopt key:deadbeef`
- `python3 -c "import pyotp; print(pyotp.HOTP('base32secret3232').at(0))"`
- `oathtool --hotp --check 755224 12345678901234567890 --counter 0`

**Examples:**
- oathtool --hotp --counter 1 12345678901234567890
- python3 -c "import pyotp; print(pyotp.HOTP('JBSWY3DPEHPK3PXP').at(42))"
- oathtool --hotp --base32 --counter 3 JBSWY3DPEHPK3PXP