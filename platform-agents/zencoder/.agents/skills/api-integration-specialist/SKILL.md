---
name: "api-integration-specialist"
description: "Deep expertise in API integrations: webhook signature verification, rate-limit handling, provider contracts, and integration testing. Use when working with webhook security, provider testing or when the user mentions webhook security, provider testing."
license: "MIT"
compatibility: "Requires node.js, python, ngrok, redis, stripe-cli, twilio-cli. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(node:*) Bash(npm:*) Bash(stripe:*)"
---

Deep expertise in API integrations: webhook signature verification, rate-limit handling, provider contracts, and integration testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node -e "const c=require('crypto');const sig=c.createHmac('s`, `stripe trigger payment_intent.failed`
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

# API Integration Specialist

Masters the hard parts of integrations: security, testing, and failure handling.

## When to Use
- Webhook tampering is a risk
- Provider failures must be simulated
- Rate limits and quotas bite

## Real Commands

```bash
# Verify signatures
node -e "const c=require('crypto');const sig=c.createHmac('sha256','whsec_test').update('payload').digest('hex');console.log('sig:',sig)"

# Simulate provider events
stripe trigger payment_intent.failed
stripe trigger invoice.finalized

# Simulate failures
node -e "const p=require('p-retry');p(()=>{if(Math.random()<0.5)throw new Error('sim');return 'ok'},{retries:3}).then(console.log).catch(console.error)"

# Live forwarding
stripe listen --forward-to localhost:3000/webhooks/stripe
```

## Signature Flow
1. Extract header `t=timestamp,v1=hex`
2. Recompute HMAC over `t.payload`
3. Timing-safe compare
4. Reject stale timestamps

## Testing
Simulate duplicates, reorders, and tampered payloads in a test suite.

## Best Practices
- Dual-accept old and new secrets during rotation
- Idempotent processing for every event

## Capabilities

### webhook-security
Verify webhook signatures and secure secret rotation

**Parameters:**
- `secret` (string): Webhook signing secret
- `header` (string): Signature header name

**Commands:**
- `node -e "const c=require('crypto');const sig=c.createHmac('sha256','whsec_test').update('payload').digest('hex');console.log('sig:',sig)"`
- `node -e "const c=require('crypto');const secret='whsec_test';const sig=c.createHmac('sha256',secret).update('{\"id\":1}').digest('hex');console.log(sig)"`
- `curl -s -X POST http://localhost:3000/webhooks/stripe -H 'Content-Type: application/json' -H 'Stripe-Signature: t=123,v1=abc' -d '{"id":"evt_1"}' -w '\n%{http_code}'`
- `stripe listen --forward-to localhost:3000/webhooks/stripe`
- `node -e "console.log('rotate: whsec_old -> whsec_new with dual-accept window')"`

**Examples:**
- node -e "const c=require('crypto');const sig=c.createHmac('sha256','whsec_test').update('payload').digest('hex');console.log('sig:',sig)"
- curl -s -X POST http://localhost:3000/webhooks/stripe -H 'Content-Type: application/json' -H 'Stripe-Signature: t=123,v1=abc' -d '{"id":"evt_1"}' -w '\n%{http_code}'
- stripe listen --forward-to localhost:3000/webhooks/stripe

### provider-testing
Test integrations against provider sandboxes and simulated failures

**Parameters:**
- `event` (string): Failure event to simulate
- `failure` (string): Failure type

**Commands:**
- `stripe trigger payment_intent.failed`
- `stripe trigger invoice.finalized`
- `curl -s -X POST http://localhost:3000/api/integrations/simulate -H 'Content-Type: application/json' -d '{"failure":"timeout"}'`
- `node -e "const p=require('p-retry');p(()=>{if(Math.random()<0.5)throw new Error('sim');return 'ok'},{retries:3}).then(console.log).catch(console.error)"`
- `npm install chaos-monkey`

**Examples:**
- stripe trigger payment_intent.failed
- stripe trigger invoice.finalized
- node -e "const p=require('p-retry');p(()=>{if(Math.random()<0.5)throw new Error('sim');return 'ok'},{retries:3}).then(console.log).catch(console.error)"

## References
- [Stripe Webhook Signatures](https://docs.stripe.com/webhooks/signatures)
- [Webhooks Best Practices](https://webhooks.fyi/)
