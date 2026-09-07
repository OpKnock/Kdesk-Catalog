---
name: "api-integration-engineer"
description: "Implements third-party integrations with official SDKs and CLIs: Stripe payments, Twilio messaging, and webhook verification. Use when working with stripe integration, twilio integration or when the user mentions stripe integration, twilio integration."
license: "MIT"
compatibility: "Requires node.js, python, ngrok, redis, stripe-cli, twilio-cli."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(brew:*) Bash(node:*) Bash(npm:*) Bash(stripe:*) Bash(twilio:*)"
---

Implements third-party integrations with official SDKs and CLIs: Stripe payments, Twilio messaging, and webhook verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install stripe`, `brew tap twilio/brew && brew install twilio`
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

**Parameters:**
- `key` (string): Stripe API key
- `event` (string): Event to trigger

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

**Parameters:**
- `from` (string): Sender number
- `to` (string): Recipient number
- `text` (string): Message body

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

## References
- [Stripe Node SDK](https://docs.stripe.com/api?lang=node)
- [Twilio CLI](https://www.twilio.com/docs/twilio-cli)
