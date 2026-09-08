---
name: "api-integration-resilience-patterns"
description: "Troubleshoots and hardens third-party API integrations: retries, circuit breakers, idempotency, and webhook reliability. Use when working with resilience patterns, webhook debugging or when the user mentions resilience patterns, webhook debugging."
---

Troubleshoots and hardens third-party API integrations: retries, circuit breakers, idempotency, and webhook reliability.

## Agentic Workflow: Read -> Reason -> Act (api-integration-resilience-patterns)

You are **Api Integration Resilience Patterns** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-integration-resilience-patterns`
- Domain: Troubleshoots and hardens third-party API integrations: retries, circuit breakers, idempotency, and webhook reliability.
- **resilience-patterns**: Add retry backoff, circuit breakers, and fallbacks around flaky third-party calls — `npm install p-retry`
- **webhook-debugging**: Forward, replay, and verify webhooks from third-party services — `ngrok http 3000`
- Check `knowledge` and `prerequisites: node.js, python, ngrok, redis`

### 2. Reason — think for `api-integration-resilience-patterns`
- For `resilience-patterns`: Add retry backoff, circuit breakers, and fallbacks around flaky third-party calls — decide which checks to run
- For `webhook-debugging`: Forward, replay, and verify webhooks from third-party services — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-integration-resilience-patterns` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Ngrok` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-integration-resilience-patterns:34a9b331`

# API Integration (Reliability)

Hardens integrations against third-party failures: timeouts, retries, circuit breaking, idempotency.

## When to Use
- Flaky upstream APIs cause user-visible failures
- Webhooks arrive late, duplicated, or out of order
- Meeting uptime SLAs that depend on partners

## Real Commands

```bash
# Tunnel for webhook testing
ngrok http 3000

# Stripe webhook flow
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger payment_intent.succeeded

# Retry with backoff
node -e "const r=require('p-retry');r(async()=>{const res=await fetch('https://api.partner.example/v1/x');if(!res.ok)throw new Error('upstream');return res.json()},{retries:4})"

# Circuit breaker
node -e "const c=require('opossum');const b=c(()=>fetch('https://api.example.com'),{timeout:2000,errorThresholdPercentage:50,resetTimeout:30000});b.fire()"
```

## Idempotency
Send `Idempotency-Key` headers and store processed event IDs so replays are no-ops.

## Testing
Use `stripe trigger` and replay endpoints to simulate duplicates, late arrivals, and malformed payloads.

## Best Practices
- Timeout every third-party call
- Exponential backoff with jitter
- Fall back to a queue (Redis) for durable processing

## Capabilities

### resilience-patterns
Add retry backoff, circuit breakers, and fallbacks around flaky third-party calls

**Parameters:**
- `retries` (string): Retry count
- `timeoutMs` (string): Per-request timeout

**Commands:**
- `npm install p-retry`
- `node -e "const r=require('p-retry'); const f=()=>Promise.reject(new Error('flaky')); r(f,{retries:3,onFailedAttempt:e=>console.log(e.attemptNumber)}).catch(()=>{})"`
- `npm install opossum`
- `node -e "const c=require('opossum'); const b=c(Promise.resolve,{timeout:1000,errorThresholdPercentage:50}); b.fire().then(()=>b.stats&&console.log(b.stats()))"`
- `npm install p-timeout`

**Examples:**
- node -e "const r=require('p-retry');r(async()=>{const res=await fetch('https://api.payment.example/v1/charge');if(!res.ok)throw new Error('upstream');return res.json()},{retries:4})"
- node -e "const c=require('opossum');const b=c(()=>fetch('https://api.example.com'),{timeout:2000,resetTimeout:30000});b.fire()"
- npm install p-timeout && node -e "const t=require('p-timeout');t(fetch('https://slow.example'),{milliseconds:1500}).catch(e=>console.log('timeout'))"

### webhook-debugging
Forward, replay, and verify webhooks from third-party services

**Parameters:**
- `port` (string): Local webhook listener port
- `event` (string): Third-party event to trigger

**Commands:**
- `ngrok http 3000`
- `stripe listen --forward-to localhost:3000/webhooks/stripe`
- `stripe trigger payment_intent.succeeded`
- `stripe logs tail payment_intent`
- `curl -s -X POST http://localhost:3000/webhooks/replay -H 'Content-Type: application/json' -d '{"event_id":"evt_123"}'`

**Examples:**
- ngrok http 3000 --subdomain my-dev
- stripe listen --forward-to localhost:3000/webhooks/stripe --events payment_intent.succeeded
- stripe trigger invoice.paid

## References
- [Stripe CLI](https://docs.stripe.com/stripe-cli)
- [ngrok Docs](https://ngrok.com/docs)
- [Resilience Patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/backup-and-restore/resilience.html)
