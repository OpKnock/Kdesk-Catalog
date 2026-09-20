# api-integration-specialist

Deep expertise in API integrations: webhook signature verification, rate-limit handling, provider contracts, and integration testing.

## Instructions

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
