---
name: "Webhook Signature"
description: "Computes and validates HMAC-SHA256 signatures on webhook payloads using openssl, Node.js crypto, and Python hmac. Sends signed webhooks with X-Hub-Signature-256 headers and verifies incoming signatures with constant-time comparison. Use when working with signature verification, api, webhook, security or when the user mentions signature verification, api, webhook, security."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Computes and validates HMAC-SHA256 signatures on webhook payloads using openssl, Node.js crypto, and Python hmac. Sends signed webhooks with X-Hub-Signature-256 headers and verifies incoming signatures with constant-time comparison.

## Agentic Workflow: Read -> Reason -> Act (webhook-signature)

You are **Webhook Signature** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `webhook-signature`
- Domain: Computes and validates HMAC-SHA256 signatures on webhook payloads using openssl, Node.js crypto, and Python hmac. Sends signed webhooks with X-Hub-Signature-256 headers and verifies incoming signature
- **signature-verification**: Compute and validate webhook HMAC signatures — `openssl dgst -sha256 -hmac "whsec_abc123" -binary payload.json | base64`
- Check `knowledge` and `prerequisites: node, openssl, python`

### 2. Reason — think for `webhook-signature`
- For `signature-verification`: Compute and validate webhook HMAC signatures — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `webhook-signature` tools
- Tools: `Glob`, `Grep`, `Read`, `Openssl`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `webhook-signature:57847027`

# Webhook Signature

## What this skill does

Add and verify HMAC-SHA256 signatures on webhook payloads so receivers can authenticate the sender and detect tampering. Covers computing signatures with openssl/node/python and validating `X-Hub-Signature-256`.

## When to use

- Signing outgoing webhooks for customers
- Verifying incoming GitHub/Stripe webhooks
- Auditing signature handling in a receiver

## Real commands

```bash
# Compute signature with openssl (base64, GitHub style)
openssl dgst -sha256 -hmac "whsec_abc123" -binary payload.json | base64

# Compute hex signature with node
node -e "const c=require('crypto');const fs=require('fs');const s=c.createHmac('sha256','whsec_abc123').update(fs.readFileSync('payload.json')).digest('hex');console.log('sha256='+s)"

# Compute hex with python
python -c "import hmac,hashlib;print(hmac.new(b'whsec_abc123',open('payload.json','rb').read(),hashlib.sha256).hexdigest())"

# Send a signed webhook
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=$(openssl dgst -sha256 -hmac 'whsec_abc123' -binary payload.json | base64)" \
  -d @payload.json http://localhost:8080/webhooks/orders

# Tampered signature must be rejected (expect 401)
curl -s -X POST -H "X-Hub-Signature-256: sha256=deadbeef" -d @payload.json http://localhost:8080/webhooks/orders -o /dev/null -w "%{http_code}\n"
```

## Verification rules

- Hash the raw request body bytes, not the re-parsed JSON
- Compare in constant time (crypto.timingSafeEqual / hmac.compare_digest)
- Support `sha256=signature` format; drop `sha1=` gracefully
- Log failures but never include the payload or secret

## Best practices

- Rotate secrets and support multiple active secrets
- Include a timestamp when signatures can be replayed
- Reject requests with missing or malformed signature headers

## Testing

```bash
# Valid signature -> 200/2xx
# Invalid signature -> 401
# Missing signature -> 401
```

## Capabilities

### signature-verification
Compute and validate webhook HMAC signatures

**Parameters:**
- `secret` (string): HMAC shared secret (whsec_...)
- `algorithm` (string): sha256 or sha1 for legacy payloads
- `payload` (string): Path to the raw payload file

**Commands:**
- `openssl dgst -sha256 -hmac "whsec_abc123" -binary payload.json | base64`
- `node -e "const c=require(\"crypto\");const fs=require(\"fs\");const s=c.createHmac(\"sha256\",\"whsec_abc123\").update(fs.readFileSync(\"payload.json\")).digest(\"hex\");console.log(\"sha256=\"+s)"`
- `curl -s -X POST -H "X-Hub-Signature-256: sha256=deadbeef" -d @payload.json http://localhost:8080/webhooks/orders -o /dev/null -w "%{http_code}"`
- `curl -s -X POST -H "X-Hub-Signature-256: sha256=$(openssl dgst -sha256 -hmac \"whsec_abc123\" -binary payload.json | base64)" -d @payload.json http://localhost:8080/webhooks/orders`
- `python -c "import hmac,hashlib;print(hmac.new(b\"whsec_abc123\",open(\"payload.json\",\"rb\").read(),hashlib.sha256).hexdigest())"`

**Examples:**
- echo -n "{\"event\":\"test\"}" | openssl dgst -sha256 -hmac "whsec_abc123" -binary | base64
- curl -s -X POST -H "Content-Type: application/json" -H "X-Hub-Signature-256: sha256=$(echo -n "{\"event\":\"test\"}" | openssl dgst -sha256 -hmac "whsec_abc123" -binary | base64)" -d "{\"event\":\"test\"}" http://localhost:8080/webhooks/orders
- node verify.js payload.json sha256=<computed>

## References
- [GitHub Validating Deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)
- [Stripe Webhook Signatures](https://docs.stripe.com/webhooks/signatures)
- [RFC 7519 - JWS](https://datatracker.ietf.org/doc/html/rfc7519)