Delivers and verifies one-time passwords over SMS using Twilio Verify API with TOTP fallback via oathtool. Sends codes through Twilio's managed verification service, checks submitted codes, and generates time-based codes for offline scenarios.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST "https://verify.twilio.com/v2/Services/$VERIFY_`
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

# SMS OTP

Hand-crafted skill for OTP delivery and verification over SMS.

## What this skill does

- Sends one-time codes via Twilio Messages and Verify
- Checks submitted codes against the Verify service
- Generates TOTP fallback codes with oathtool

## When to use

- Login flows that need a second factor
- Account recovery via phone
- Testing OTP delivery end to end

## Real commands

```bash
# Raw SMS with the Messages API
curl -s -u "$TWILIO_SID:$TWILIO_AUTH" -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json" --data-urlencode "To=+15551234567" --data-urlencode "From=+15559876543" --data-urlencode "Body=Your code is 123456"

# Twilio Verify: send the code
curl -s -u "$TWILIO_SID:$TWILIO_AUTH" -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SID/Verifications" --data-urlencode "To=+15551234567" --data-urlencode "Channel=sms"

# Twilio Verify: check the code
curl -s -u "$TWILIO_SID:$TWILIO_AUTH" -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SID/VerificationCheck" --data-urlencode "To=+15551234567" --data-urlencode "Code=123456"

# TOTP fallback
oathtool --totp --base32 "JBSWY3DPEHPK3PXP"

# Python SDK
pip install twilio
```

## Verify flow

1. POST /Verifications to send a code
2. User submits the code
3. POST /VerificationCheck; status approved means valid

## Testing

```bash
oathtool --totp --base32 "JBSWY3DPEHPK3PXP"   # current code
curl -s -u "$TWILIO_SID:$TWILIO_AUTH" -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SID/VerificationCheck" --data-urlencode "To=+15551234567" --data-urlencode "Code=$(oathtool --totp --base32 'JBSWY3DPEHPK3PXP')"
```

## Best practices

- Rate-limit sends per phone: max 3-5 per hour
- Use Verify instead of raw Messages: it handles expiry and checking
- Never log codes; hash them at rest

## Capabilities

### sms-otp-delivery
Delivers and verifies one-time passwords over SMS using Twilio Verify API with TOTP fallback via oathtool. Sends codes through Twilio's managed verification service, checks submitted codes, and generates time-based codes for offline scenarios.

**Parameters:**
- `verify_sid` (string): Twilio Verify Service SID
- `phone_number` (string): Destination phone number in E.164 format
- `totp_secret` (string): Base32-encoded TOTP secret for fallback

**Commands:**
- `curl -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SID/Verifications" -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" --data-urlencode "To=+15551234567" --data-urlencode "Channel=sms"`
- `curl -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SID/VerificationChecks" -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" --data-urlencode "To=+15551234567" --data-urlencode "Code=123456"`
- `oathtool --base32 --totp "JBSWY3DPEHPK3PXP"`
- `pip install pyotp`

**Examples:**
- curl -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SID/Verifications" -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" --data-urlencode "To=+15551234567" --data-urlencode "Channel=sms"
- curl -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SID/VerificationChecks" -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" --data-urlencode "To=+15551234567" --data-urlencode "Code=123456"
- oathtool --base32 --totp "JBSWY3DPEHPK3PXP"

## References
- [Twilio Verify API](https://www.twilio.com/docs/verify/api)