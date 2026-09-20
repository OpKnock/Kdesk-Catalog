---
applyTo: "**/*.json **/*.r **/*.sh"
---

# Api Webhook Ngrok Tunnels

Tests webhooks with local tooling: ngrok tunnels for public callbacks, webhook.site inspection, curl replays, and delivery simulation.

## Instructions

# API Webhook v2 - Testing

Webhook testing tooling.

## What This Skill Does
- Tunnels local receivers with ngrok
- Inspects incoming payloads
- Replays deliveries for verification

## When to Use
- Testing provider webhooks locally
- Debugging delivery payloads
- Demonstrating receivers

## Real Commands

```bash
ngrok http 3000
curl -s http://localhost:4040/api/tunnels | jq '.tunnels[0].public_url'
curl -s -X POST http://localhost:3000/webhook-test -H 'Content-Type: application/json' -d '{"event":"test"}'
```

## Workflow
1. Start ngrok on the receiver port
2. Configure the provider with the public URL
3. Trigger the provider event
4. Inspect payloads at the tunnel console

## Testing
- Replay events with curl --retry
- Verify headers and raw bodies arrive intact
- Test concurrent deliveries


## Best Practices
- Use fixed subdomains in dev
- Keep receiver logs enabled
- Reset delivery state between tests

## Capabilities

### ngrok-tunnels
Expose local webhook receivers publicly

**Commands:**
- `ngrok http 3000`
- `ngrok http --host-header=rewrite 3000`
- `curl -s http://localhost:4040/api/tunnels | jq '.tunnels[0].public_url'`
- `ngrok config check`

**Examples:**
- ngrok http 3000 creates a public tunnel
- localhost:4040 exposes tunnel status
- ngrok config check validates the config

### delivery-simulation
Simulate webhook deliveries

**Commands:**
- `curl -s -X POST http://localhost:3000/webhook-test -H 'Content-Type: application/json' -d '{"event":"test"}' -w '\n%{http_code}\n'`
- `curl -s -X POST http://localhost:3000/webhook-test -H 'Content-Type: application/json' -d '{"event":"test"}' --retry 2 --retry-delay 1 -w '\n%{http_code}\n'`
- `curl -s https://webhook.site/token | jq '.uuid'`

**Examples:**
- -cli --help
- -api --help
