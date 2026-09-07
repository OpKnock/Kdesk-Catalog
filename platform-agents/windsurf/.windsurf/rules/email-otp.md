---
trigger: glob
description: "One-time password delivery by email: generate OTPs, send via SMTP/transactional APIs, and verify codes with rate limiting and expiry. Use when working with otp verification, api or when the user mentions otp verification, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh"]
---

One-time password delivery by email: generate OTPs, send via SMTP/transactional APIs, and verify codes with rate limiting and expiry.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s --url 'smtp://smtp.gmail.com:587' --ssl-reqd --mail-`
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

# Email OTP

## What this skill does

Email OTPs deliver time-limited one-time codes by email for login or verification. Production systems store only a hash of the code, expire it, and throttle verification attempts.

## When to use

- Passwordless login or second-factor email verification
- Confirming new devices or sensitive actions

## Real commands

```bash
# Send via SMTP with curl (starttls)
curl -s --url 'smtp://smtp.gmail.com:587' --ssl-reqd --mail-from otp@yourdomain.com \
  --mail-rcpt user@gmail.com --upload-file email.txt --user 'otp@yourdomain.com:app-password'

# Generate a TOTP (RFC 6238) for comparison
node -e "const o=require('otplib');console.log(o.authenticator.generate('BASE32SECRET'))"

# Store the code with TTL in Redis
redis-cli SET otp:user@gmail.com 482913 EX 300
redis-cli GET otp:user@gmail.com

# Send via SendGrid API
curl -s -X POST https://api.sendgrid.com/v3/mail/send -H 'Authorization: Bearer $SENDGRID_KEY' -H 'Content-Type: application/json' -d @email.json
```

## email.json example

```json
{
  "personalizations": [{"to": [{"email": "user@gmail.com"}]}],
  "from": {"email": "otp@yourdomain.com", "name": "Example Auth"},
  "subject": "Your login code",
  "content": [{"type": "text/plain", "value": "Your code is 482913. It expires in 5 minutes."}]
}
```

## Verification flow

```bash
# Check existence + TTL, then compare hash; increment attempts
redis-cli GET otp:user@gmail.com
redis-cli TTL otp:user@gmail.com
redis-cli INCR fail:user@gmail.com
```

## Best practices

- Store a bcrypt/argon2 hash of the code, never the raw code.
- 6 digits, 5-10 minute TTL, max 3-5 attempts then invalidate.
- Log the attempt count per email; lock after 10 failed tries per hour.
- Never reuse codes; always rotate on resend.
- Monitor SMTP delivery rate; bounced OTPs burn user trust.

## Capabilities

### otp-verification
Send OTP emails and verify codes against stored hashes with expiry and attempt limits.

**Parameters:**
- `recipient` (string): Email address receiving the OTP
- `ttl` (integer): OTP validity in seconds (e.g. 300)
- `code-length` (integer): Number of digits in the OTP

**Commands:**
- `curl -s --url 'smtp://smtp.gmail.com:587' --ssl-reqd --mail-from otp@yourdomain.com --mail-rcpt user@gmail.com --upload-file email.txt --user 'otp@yourdomain.com:app-password'`
- `node -e "const o=require('otplib');console.log(o.authenticator.generate('BASE32SECRET'))"`
- `curl -s -X POST https://api.sendgrid.com/v3/mail/send -H 'Authorization: Bearer $SENDGRID_KEY' -H 'Content-Type: application/json' -d @email.json`
- `redis-cli SET otp:user@gmail.com 482913 EX 300`
- `redis-cli GET otp:user@gmail.com`

**Examples:**
- redis-cli SET otp:user@gmail.com 482913 EX 300 && curl -s --url 'smtp://smtp.gmail.com:587' --ssl-reqd --mail-from otp@yourdomain.com --mail-rcpt user@gmail.com --upload-file email.txt --user 'otp@yourdomain.com:app-password'
- redis-cli GET otp:user@gmail.com
- curl -s -X POST https://api.sendgrid.com/v3/mail/send -H 'Authorization: Bearer $SENDGRID_KEY' -H 'Content-Type: application/json' -d @email.json

## References
- [NIST OTP Guidelines 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
