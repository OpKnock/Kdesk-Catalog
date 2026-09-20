---
trigger: glob
description: "Builds webhook endpoints that receive events from external systems. Registers endpoints, forwards traffic locally with smee, POSTs test payloads with headers, and inspects received events with timing and status verification."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Webhook

Builds webhook endpoints that receive events from external systems. Registers endpoints, forwards traffic locally with smee, POSTs test payloads with headers, and inspects received events with timing and status verification.

## Instructions

# Webhook

## What this skill does

Build webhook endpoints that receive events from external systems: register endpoints, forward traffic locally with smee, POST test payloads, and inspect what was received with headers intact.

## When to use

- Accepting events from GitHub, Stripe, or custom providers
- Building a webhook consumer
- Debugging payloads and headers

## Real commands

```bash
# Forward remote webhooks to localhost
smee --url https://smee.io/your-channel --port 8080

# Receive a webhook POST
curl -s -X POST http://localhost:8080/hooks \
  -H "Content-Type: application/json" \
  -H "X-Event-Type: order.created" \
  -d "{\"id\":42}" -w "\n%{http_code}\n"

# Inspect the most recently received event
curl -s http://localhost:8080/hooks/received | jq ".[-1] | {event, id, received_at}"

# Ping handler
curl -s -X POST http://localhost:8080/hooks/ping | jq ".message"

# Respond fast: 2xx within a few seconds
curl -s http://localhost:8080/hooks -o /dev/null -w "%{time_total}s %{http_code}\n"
```

## Receiver contract

- Respond 2xx quickly (providers retry otherwise)
- Verify signature before doing work
- Process asynchronously (queue), not inline
- Deduplicate by delivery ID

## Best practices

- Return 200 for valid events, 4xx for invalid
- Include X-Event-Type and X-Delivery-ID in logs
- Acknowledge before long processing via a queue
- Keep a received-events buffer for debugging

## Testing

```bash
smee --url https://smee.io/test --port 8080 &
curl -s -X POST http://localhost:8080/hooks -H "X-Event-Type: test.event" -d "{\"probe\":true}"
curl -s http://localhost:8080/hooks/received | jq ".[-1]"
```

## Capabilities

### webhook-ops
Create, receive, and debug webhook endpoints

**Commands:**
- `smee --url https://smee.io/your-channel --port 8080`
- `curl -s -X POST http://localhost:8080/hooks -H "Content-Type: application/json" -H "X-Event-Type: order.created" -d "{\"id\":42}" -w "\n%{http_code}\n"`
- `curl -s http://localhost:8080/hooks/received | jq ".[-1] | {event, id, received_at}"`
- `curl -s -X POST http://localhost:8080/hooks/ping | jq ".message"`
- `curl -s http://localhost:8080/hooks -o /dev/null -w "%{time_total}s %{http_code}\n"`

**Examples:**
- smee --url https://smee.io/demo-channel --port 8080
- curl -s -X POST http://localhost:8080/hooks -H "Content-Type: application/json" -d "{\"event\":\"payment.succeeded"}" | jq ".received"
- curl -sI http://localhost:8080/hooks -X OPTIONS | grep -i "x-webhook"
