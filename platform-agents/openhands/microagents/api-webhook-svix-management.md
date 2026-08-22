---
name: "api-webhook-svix-management"
description: "Operates webhook infrastructure with Svix and Hookdeck: endpoint management, message dispatch, retries, and delivery observability."
type: knowledge
triggers: ["api-webhook-svix-management", "svix-management", "hookdeck"]
---

# Api Webhook Svix Management

Operates webhook infrastructure with Svix and Hookdeck: endpoint management, message dispatch, retries, and delivery observability.

## Instructions

# API Webhook v3 - Infrastructure

Webhook platform operations.

## What This Skill Does
- Manages endpoints and event types
- Dispatches signed messages
- Provides retry and observability

## When to Use
- Running webhooks at scale
- Reliable delivery guarantees
- Multi-endpoint fan-out

## Real Commands

```bash
svix webhook create --name "order-created" --url https://app.example.com/hook
curl -s -X POST http://localhost:8071/api/v1/message -H 'Authorization: Bearer $SVIX_TOKEN' -H 'Content-Type: application/json' -d '{"eventType":"order.created","payload":{"id":1}}'
hookdeck listen 3000 webhook
```

## Message Flow
1. Register endpoints with URLs
2. Dispatch typed events
3. Platform retries failures
4. Inspect delivery attempts

## Testing
- Trigger events and verify signed delivery
- Test endpoint downtime retries
- Review delivery attempt logs


## Best Practices
- Register event types explicitly
- Rotate signing secrets
- Monitor delivery failure rates

## Capabilities

### svix-management
Manage webhook endpoints and dispatch messages

**Commands:**
- `svix webhook create --name "order-created" --url http://localhost:8080/hook`
- `svix webhook get --id wh_xxxx`
- `svix webhook list`
- `curl -s -X POST http://localhost:8071/api/v1/message -H 'Authorization: Bearer $SVIX_TOKEN' -H 'Content-Type: application/json' -d '{"eventType":"order.created","payload":{"id":1}}'`
- `curl -s http://localhost:8071/api/v1/health -o /dev/null -w '%{http_code}\n'`

**Examples:**
- svix webhook create registers an endpoint
- POST /message dispatches a signed event
- svix webhook list shows endpoint status

### hookdeck
Route and observe webhooks with Hookdeck

**Commands:**
- `hookdeck login`
- `hookdeck listen 3000 webhook`
- `hookdeck sources list`
- `hookdeck destinations list`
- `hookdeck events list`
