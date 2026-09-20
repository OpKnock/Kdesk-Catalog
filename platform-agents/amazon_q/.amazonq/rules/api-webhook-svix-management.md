Operates webhook infrastructure with Svix and Hookdeck: endpoint management, message dispatch, retries, and delivery observability.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `svix webhook create --name "order-created" --url http://loca`, `hookdeck login`
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

**Parameters:**
- `endpoint` (string): Webhook URL
- `event-type` (string): Event type name
- `payload` (object): Event payload

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

**Examples:**
- -cli --help
- -api --help

## References
- [Svix Docs](https://www.svix.com/docs)
- [Hookdeck Docs](https://hookdeck.com/docs)