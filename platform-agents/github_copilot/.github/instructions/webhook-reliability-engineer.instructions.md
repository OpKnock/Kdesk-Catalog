---
applyTo: "**/*.json **/*.r"
---

Design, deliver, and debug webhook integrations with retries, signatures, and visibility using svix, ngrok, and curl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ngrok http 3000`, `svix login`
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

# Webhook Reliability Engineering

Design webhook integrations that deliver events reliably, verify their authenticity, and fail loudly instead of silently.

## When to Use

- Integrating with GitHub, Stripe, Slack, or any provider pushing events
- Building a webhook dispatch service for your own platform
- Debugging why a third-party integration stops receiving events

## Delivery Contract

1. Receiver must reply 2xx within the provider timeout, ideally under 10 seconds.
2. On non-2xx, the provider retries with exponential backoff and jitter; track attempt counts.
3. Every delivery should carry: event id, event type, timestamp, and payload version.
4. Duplicate delivery is normal; receivers must be idempotent on event id.

## Signature Verification

1. Compute the HMAC over the raw body (not the parsed JSON) with the shared secret.
2. Compare using a constant-time comparison; never a plain string equality.
3. Validate the timestamp window (usually +/- 5 minutes) to stop replay attacks.
4. Rotate secrets without breaking in-flight deliveries by accepting two active secrets.

## Local Debugging Loop

1. Run your receiver locally on port 3000.
2. Expose it: ngrok http 3000.
3. Point the provider's webhook URL at the tunnel and send a test event.
4. Inspect the request body, headers, and signature in the ngrok inspector; replay payloads with curl.

## Observability

- Log: event id, attempt number, latency, status code, and failure reason.
- Alert on: delivery failure rate above threshold, retry queue depth, signature verification failures.
- Maintain a dead-letter queue for events that exhaust all retries.

## Common Pitfalls

- Verifying signatures against JSON.stringify output instead of the raw body.
- Receiver doing heavy work (email, DB writes) inline and timing out.
- No idempotency, so a single retry duplicates side effects.
- Hardcoding the provider secret in the repo.

## Checklist

- Raw-body HMAC verification with constant-time compare
- Idempotent handlers keyed on event id
- 2xx acknowledgment within timeout
- Retry with backoff + dead-letter queue
- Failure alerting and delivery dashboards

## Capabilities

### Expose local endpoints with ngrok
Tunnel a local webhook receiver to a public HTTPS URL and inspect incoming traffic.

**Parameters:**
- `local port` (integer): Port your webhook receiver listens on.
- `basic-auth` (string): user:pass credential protecting the public tunnel URL.

**Commands:**
- `ngrok http 3000`
- `ngrok http --basic-auth=user:pass --host-header=rewrite 3000`
- `ngrok status`
- `ngrok tunnel list`

**Examples:**
- ngrok http 3000
- ngrok http --basic-auth=user:pass --host-header=rewrite 3000

### Manage endpoints with svix
Create applications and endpoints, send test messages, and list deliveries from the svix CLI.

**Parameters:**
- `event-types` (string): Comma-separated event types the endpoint subscribes to.
- `payload` (string): JSON payload sent with the test message.

**Commands:**
- `svix login`
- `svix application create --name my-app`
- `svix endpoint create --url http://localhost:8080/webhooks --event-types issue.created`
- `svix message send --event-type issue.created --payload '{"id":42}' --app my-app`
- `svix endpoint list --app my-app`

**Examples:**
- svix endpoint create --url http://localhost:8080/webhooks --event-types issue.created
- svix message send --event-type issue.created --payload '{"id":42}' --app my-app

### Verify deliveries and retries with curl
Simulate provider webhooks, check signature headers, and replay failed deliveries against your receiver.

**Parameters:**
- `signature header` (string): Header name carrying the HMAC signature (svix-signature, x-hub-signature-256, etc.).
- `retries` (integer): Number of retry attempts for curl-based delivery checks.

**Commands:**
- `curl -s -i -X POST https://tunnel.ngrok.io/webhooks -H 'Content-Type: application/json' -H 'svix-id: msg_1' -H 'svix-signature: v1,<sig>' -H 'svix-timestamp: 1720000000' -d '{"event":"build.failed"}'`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}s' --retry 3 --retry-delay 2 -X POST http://localhost:8080/webhooks -d '{}'`
- `curl -s -H 'Authorization: Bearer demo-token' 'https://api.svix.com/api/v1/app/my-app/msg/msg_1/attempt'`

**Examples:**
- curl -s -i -X POST https://tunnel.ngrok.io/webhooks -H 'Content-Type: application/json' -H 'svix-id: msg_1' -H 'svix-signature: v1,<sig>' -H 'svix-timestamp: 1720000000' -d '{"event":"build.failed"}'
- curl -s -o /dev/null -w '%{http_code} %{time_total}s' --retry 3 --retry-delay 2 -X POST http://localhost:8080/webhooks -d '{}'

## References
- [](https://ngrok.com/docs)
- [](https://docs.svix.com)
- [](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
- [](https://webhooks.fyi/)
