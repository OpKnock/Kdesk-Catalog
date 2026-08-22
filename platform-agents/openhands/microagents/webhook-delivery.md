---
name: "webhook-delivery"
description: "Operates webhook delivery end-to-end. Registers endpoints, forwards events locally with smee, sends test deliveries, inspects delivery status and logs, and replays failed deliveries."
type: knowledge
triggers: ["webhook-delivery"]
---

# Webhook Delivery

Operates webhook delivery end-to-end. Registers endpoints, forwards events locally with smee, sends test deliveries, inspects delivery status and logs, and replays failed deliveries.

## Instructions

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
