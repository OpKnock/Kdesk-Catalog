---
name: "api-integration-engineer"
description: "Implements third-party integrations with official SDKs and CLIs: Stripe payments, Twilio messaging, and webhook verification."
---

# api-integration-engineer

Implements third-party integrations with official SDKs and CLIs: Stripe payments, Twilio messaging, and webhook verification.

## Instructions

# API Integration Engineer

Builds real third-party integrations with official tools.

## When to Use
- Adding payment processing
- Adding SMS notifications
- Building connectors with official SDKs

## Real Commands

```bash
# Stripe
npm install stripe
node -e "const s=require('stripe')('sk_test_x');s.products.create({name:'T-Shirt'}).then(p=>console.log(p.id))"
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger payment_intent.succeeded
stripe logs tail

# Twilio
brew tap twilio/brew && brew install twilio
twilio login
twilio api:core:messages:create --from +15017122661 --to +15558675310 --text 'Your order shipped'
```

## Webhook Verification
- Verify signatures on every event
- Reply 200 immediately
- Process in a queue

## Testing
Use sandbox keys and trigger every event type before going live.

## Best Practices
- Secrets in env/secret manager
- Idempotency keys on money paths

## Capabilities

### stripe-integration
Build payment flows with Stripe SDK and CLI

**Commands:**
- `npm install stripe`
- `stripe listen --forward-to localhost:3000/webhooks/stripe`
- `stripe trigger payment_intent.succeeded`
- `node -e "const s=require('stripe')('sk_test_x');s.products.create({name:'T-Shirt'}).then(p=>console.log(p.id))"`
- `stripe logs tail`

**Examples:**
- node -e "const s=require('stripe')('sk_test_x');s.products.create({name:'T-Shirt'}).then(p=>console.log(p.id))"
- stripe trigger payment_intent.succeeded
- stripe logs tail payment_intent

### twilio-integration
Send SMS and verify delivery with Twilio

**Commands:**
- `brew tap twilio/brew && brew install twilio`
- `twilio login`
- `twilio api:core:messages:create --from +15017122661 --to +15558675310 --text 'Your order shipped'`
- `twilio api:core:messages:list --limit 5`
- `twilio api:core:accounts:list`

**Examples:**
- twilio api:core:messages:create --from +15017122661 --to +15558675310 --text 'Your order shipped'
- twilio api:core:messages:list --limit 5
- twilio api:core:accounts:list
