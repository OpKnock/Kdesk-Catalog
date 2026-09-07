---
name: "api-webhook-specialist"
description: "Secures webhooks with HMAC signatures: signing payloads with openssl and node crypto, signature verification middleware, and replay protection. Use when working with hmac signing, verification or when the user mentions hmac signing, verification."
---

Secures webhooks with HMAC signatures: signing payloads with openssl and node crypto, signature verification middleware, and replay protection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openssl dgst -sha256 -hmac "secret-key" -hex payload.json`, `node -e "const c=require('crypto'); const ok=(sig,p)=>{const`
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

# API Webhook Specialist

Webhook signature security.

## What This Skill Does
- Signs payloads with HMAC-SHA256
- Verifies signatures in middleware
- Protects against replay and forgery

## When to Use
- Receiving third-party webhooks
- Emitting signed webhooks
- Auditing delivery authenticity

## Real Commands

```bash
openssl dgst -sha256 -hmac "secret-key" -hex payload.json
node -e "const c=require('crypto'); console.log(c.createHmac('sha256','secret-key').update('payload').digest('hex'))"
```

## Verification Middleware

```js
app.post('/webhooks', (req, res) => {
  const sig = req.get('X-Signature').replace('sha256=', '');
  const expected = crypto.createHmac('sha256', SECRET)
    .update(JSON.stringify(req.body)).digest('hex');
  if (!crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
    return res.sendStatus(401);
  }
  res.sendStatus(200);
});
```

## Testing
- Send bad signatures and expect 401
- Verify timestamped replay rejection
- Test header/body integrity


## Best Practices
- Rotate webhook secrets regularly
- Use timingSafeEqual for comparisons
- Include timestamps to block replays

## Capabilities

### hmac-signing
Sign and verify webhook payloads

**Parameters:**
- `secret` (string): Shared HMAC secret
- `algorithm` (string): sha256, sha512
- `payload` (string): Payload to sign

**Commands:**
- `openssl dgst -sha256 -hmac "secret-key" -hex payload.json`
- `node -e "const c=require('crypto'); const sig=c.createHmac('sha256','secret-key').update(JSON.stringify({event:'x'})).digest('hex'); console.log(sig)"`
- `node -e "const c=require('crypto'); const sig=(s)=>c.createHmac('sha256','secret-key').update(s).digest('hex'); const payload=JSON.stringify({a:1}); console.log('X-Signature:', sig(payload))"`
- `curl -s -X POST http://localhost:3000/webhooks -H 'Content-Type: application/json' -H "X-Signature: sha256=$(openssl dgst -sha256 -hmac 'secret-key' -hex payload.json | awk '{print $2}')" -d @payload.json -w '\n%{http_code}\n'`

**Examples:**
- openssl dgst -hmac signs with a shared secret
- node crypto verifies signatures in middleware
- curl sends the signature header for testing

### verification
Verify signatures in middleware

**Commands:**
- `node -e "const c=require('crypto'); const ok=(sig,p)=>{const expect=c.createHmac('sha256','secret-key').update(p).digest('hex'); return c.timingSafeEqual(Buffer.from(sig),Buffer.from(expect))}; console.log(ok('abc','x'), ok(c.createHmac('sha256','secret-key').update('x').digest('hex'),'x'))"`
- `curl -s -X POST http://localhost:3000/webhooks -H 'Content-Type: application/json' -H 'X-Signature: sha256=bad' -d '{"a":1}' -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help

## References
- [Stripe Webhook Signatures](https://docs.stripe.com/webhooks/signatures)
- [Node crypto Docs](https://nodejs.org/api/crypto.html)
