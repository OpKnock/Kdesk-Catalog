---
trigger: glob
description: "Builds webhook endpoints that receive events from external systems. Registers endpoints, forwards traffic locally with smee, POSTs test payloads with headers, and inspects received events with timing and status verification. Use when working with webhook ops, api, events or when the user mentions webhook ops, api, events."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Builds webhook endpoints that receive events from external systems. Registers endpoints, forwards traffic locally with smee, POSTs test payloads with headers, and inspects received events with timing and status verification.

## Agentic Workflow: Read -> Reason -> Act (webhook)

You are **Webhook** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `webhook`
- Domain: Builds webhook endpoints that receive events from external systems. Registers endpoints, forwards traffic locally with smee, POSTs test payloads with headers, and inspects received events with timing 
- **webhook-ops**: Create, receive, and debug webhook endpoints — `smee --url https://smee.io/your-channel --port 8080`
- Check `knowledge` and `prerequisites: smee, curl`

### 2. Reason — think for `webhook`
- For `webhook-ops`: Create, receive, and debug webhook endpoints — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `webhook` tools
- Tools: `Glob`, `Grep`, `Read`, `Smee`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `webhook:46dc4499`

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

**Parameters:**
- `event_type` (string): X-Event-Type header describing the event
- `port` (integer): Port for smee forwarding (default 3000)
- `url` (string): smee.io channel URL

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

## References
- [Webhooks.fyi](https://webhooks.fyi/)
- [GitHub Webhooks](https://docs.github.com/en/webhooks)
- [Stripe Webhooks](https://docs.stripe.com/webhooks)
