---
applyTo: "**/*.json **/*.r **/*.sh"
---

Troubleshoots and hardens third-party API integrations: retries, circuit breakers, idempotency, and webhook reliability.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install p-retry`, `ngrok http 3000`
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
