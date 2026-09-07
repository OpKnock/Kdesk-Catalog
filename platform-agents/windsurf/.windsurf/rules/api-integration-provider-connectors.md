---
trigger: glob
description: "Implements third-party API integrations: payment and SMS connectors with webhooks, API keys, and sandbox testing. Use when working with provider connectors, webhook implementation or when the user mentions provider connectors, webhook implementation."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Implements third-party API integrations: payment and SMS connectors with webhooks, API keys, and sandbox testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `stripe login`, `ngrok http 3000`
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

# API Integration (Implementation)

Builds working integrations with third-party providers using official CLIs and sandboxes.

## When to Use
- Adding Stripe, Twilio, or similar providers
- Setting up local webhook development
- Migrating from test to live mode

## Real Commands

```bash
# Stripe setup
stripe login
stripe create product --name 'T-Shirt'
stripe create price --product prod_123 --unit-amount 1999 --currency usd

# Local webhook dev
ngrok http 3000
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger checkout.session.completed

# Twilio
brew tap twilio/brew && brew install twilio
twilio login
twilio api:core:messages:create --from +15017122661 --to +15558675310 --text 'Hello'
```

## Key Management
- Store keys in a secret manager, never in code
- Use test keys in development

## Testing
Trigger every webhook event in sandbox mode and verify processing end to end.

## Best Practices
- Verify webhook signatures
- Respond 2xx fast, process asynchronously
- Keep idempotency keys on money moves

## Capabilities

### provider-connectors
Connect payment and messaging providers using their official CLIs and SDKs

**Parameters:**
- `amount` (string): Amount in minor units
- `currency` (string): Currency code

**Commands:**
- `stripe login`
- `stripe create product --name 'T-Shirt'`
- `stripe create price --product prod_123 --unit-amount 1999 --currency usd`
- `stripe payment_intents create --amount 1999 --currency usd`
- `twilio api:core:messages:create --from +15017122661 --to +15558675310 --text 'Hello from Twilio'`

**Examples:**
- stripe create price --product prod_123 --unit-amount 1999 --currency usd
- stripe payment_intents create --amount 1999 --currency usd --automatic-payment-methods[enabled]=true
- twilio api:core:messages:create --from +15017122661 --to +15558675310 --text 'Order shipped'

### webhook-implementation
Receive, verify, and process webhooks from providers

**Parameters:**
- `port` (string): Local port
- `event` (string): Webhook event type

**Commands:**
- `ngrok http 3000`
- `stripe listen --forward-to localhost:3000/webhooks/stripe`
- `stripe trigger checkout.session.completed`
- `curl -s http://localhost:4040/api/tunnels | python -m json.tool`
- `curl -s -X POST http://localhost:3000/webhooks/health -o /dev/null -w '%{http_code}'`

**Examples:**
- ngrok http 3000 --subdomain api-dev
- stripe listen --forward-to localhost:3000/webhooks/stripe --events checkout.session.completed
- curl -s http://localhost:4040/api/tunnels | python -m json.tool

## References
- [Stripe CLI Reference](https://docs.stripe.com/cli)
- [Twilio CLI](https://www.twilio.com/docs/twilio-cli)
- [ngrok Docs](https://ngrok.com/docs)
