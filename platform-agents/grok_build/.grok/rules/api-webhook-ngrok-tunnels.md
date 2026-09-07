Tests webhooks with local tooling: ngrok tunnels for public callbacks, webhook.site inspection, curl replays, and delivery simulation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ngrok http 3000`, `curl -s -X POST http://localhost:3000/webhook-test -H 'Conte`
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

**Parameters:**
- `port` (integer): Local port to tunnel
- `subdomain` (string): Fixed subdomain
- `region` (string): Tunnel region

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

## References
- [ngrok Docs](https://ngrok.com/docs)
- [webhook.site](https://webhook.site/)