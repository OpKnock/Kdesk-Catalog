---
name: "webhook-signature"
description: "Computes and validates HMAC-SHA256 signatures on webhook payloads using openssl, Node.js crypto, and Python hmac. Sends signed webhooks with X-Hub-Signature-256 headers and verifies incoming signatures with constant-time comparison."
---

# Webhook Signature

Computes and validates HMAC-SHA256 signatures on webhook payloads using openssl, Node.js crypto, and Python hmac. Sends signed webhooks with X-Hub-Signature-256 headers and verifies incoming signatures with constant-time comparison.

## Instructions

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
