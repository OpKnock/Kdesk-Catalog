---
name: "webhook-delivery"
description: "Operates webhook delivery end-to-end. Registers endpoints, forwards events locally with smee, sends test deliveries, inspects delivery status and logs, and replays failed deliveries. Use when working with webhook delivery, api or when the user mentions webhook delivery, api."
type: knowledge
triggers: ["webhook-delivery"]
---

Operates webhook delivery end-to-end. Registers endpoints, forwards events locally with smee, sends test deliveries, inspects delivery status and logs, and replays failed deliveries.

## Agentic Workflow: Read -> Reason -> Act (webhook-delivery)

You are **Webhook Delivery** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `webhook-delivery`
- Domain: Operates webhook delivery end-to-end. Registers endpoints, forwards events locally with smee, sends test deliveries, inspects delivery status and logs, and replays failed deliveries.
- **webhook-delivery**: Forward, deliver, and monitor webhook events — `smee --url https://smee.io/your-channel --port 8080`
- Check `knowledge` and `prerequisites: smee, curl`

### 2. Reason — think for `webhook-delivery`
- For `webhook-delivery`: Forward, deliver, and monitor webhook events — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `webhook-delivery` tools
- Tools: `Glob`, `Grep`, `Read`, `Smee`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `webhook-delivery:a8b3458c`

# Webhook Delivery

## What this skill does

Set up and operate webhook delivery for your API: register endpoints, forward events locally with smee, send test deliveries, inspect delivery status, and replay failures.

## When to use

- Building a webhook feature for customers
- Debugging undelivered events
- Replaying deliveries after an outage

## Real commands

```bash
# Forward remote webhooks to localhost
smee --url https://smee.io/your-channel --port 8080

# Simulate an event POST
curl -X POST -H "Content-Type: application/json" \
  -d "{\"event\":\"order.created\",\"id\":42}" \
  http://localhost:8080/webhooks/orders

# Delivery status
curl -s http://localhost:8080/webhooks/deliveries | jq ".[0].status"

# Count failed deliveries
curl -s "http://localhost:8080/webhooks/deliveries?status=failed" | jq "length"

# Retry a delivery
curl -s -X POST http://localhost:8080/webhooks/deliveries/DELIVERY_ID/retry | jq ".attempts"

# List registered endpoints
curl -s http://localhost:8080/webhooks/endpoints | jq ".[].url"
```

## Delivery record fields

- delivery_id, event_id, endpoint_id
- status, attempts, last_error
- request_headers, request_body, response_body
- created_at, next_retry_at

## Best practices

- Sign payloads (see webhook-signature-skill)
- Include `X-Event-ID` and `X-Delivery-ID` headers
- Retry with exponential backoff, cap at ~5 attempts
- Dead-letter events that exceed retry limits
- Keep delivery logs for at least 30 days

## Testing

```bash
smee --url https://smee.io/test-channel --port 8080 &
curl -s -X POST http://localhost:8080/webhooks/orders -d "{\"event\":\"test\"}"
curl -s http://localhost:8080/webhooks/deliveries | jq ".[0]"
```

## Capabilities

### webhook-delivery
Forward, deliver, and monitor webhook events

**Parameters:**
- `url` (string): smee.io channel URL for local forwarding
- `port` (integer): Local port smee forwards to (default 3000)
- `status` (string): Filter deliveries by status: pending, delivered, failed

**Commands:**
- `smee --url https://smee.io/your-channel --port 8080`
- `curl -X POST -H "Content-Type: application/json" -d "{\"event\":\"order.created\",\"id\":42}" http://localhost:8080/webhooks/orders`
- `curl -s http://localhost:8080/webhooks/deliveries | jq ".[0].status"`
- `curl -s -X POST http://localhost:8080/webhooks/deliveries/DELIVERY_ID/retry | jq ".attempts"`
- `curl -s "http://localhost:8080/webhooks/deliveries?status=failed" | jq "length"`

**Examples:**
- smee --url https://smee.io/your-channel --port 8080
- curl -s -X POST http://localhost:8080/webhooks/orders -H "X-Event-ID: evt_1" -d "{\"event\":\"payment.succeeded"}" | jq
- curl -s http://localhost:8080/webhooks/endpoints | jq ".[].url"

## References
- [Webhooks.fyi](https://webhooks.fyi/)
- [GitHub Webhooks Docs](https://docs.github.com/en/webhooks)
- [Stripe Webhook Best Practices](https://docs.stripe.com/webhooks/best-practices)
