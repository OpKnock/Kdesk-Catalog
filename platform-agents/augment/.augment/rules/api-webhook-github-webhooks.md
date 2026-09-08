---
type: agent_requested
description: "Integrates with platform webhooks: GitHub repository hooks, Stripe event triggers, Slack incoming webhooks, and signature verification patterns. Use when working with github webhooks, stripe slack or when the user mentions github webhooks, stripe slack."
---

Integrates with platform webhooks: GitHub repository hooks, Stripe event triggers, Slack incoming webhooks, and signature verification patterns.

## Agentic Workflow: Read -> Reason -> Act (api-webhook-github-webhooks)

You are **Api Webhook Github Webhooks** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-webhook-github-webhooks`
- Domain: Integrates with platform webhooks: GitHub repository hooks, Stripe event triggers, Slack incoming webhooks, and signature verification patterns.
- **github-webhooks**: Manage GitHub repository webhooks — `gh api repos/octocat/Hello-World/hooks --method POST -f config.url=http://localh`
- **stripe-slack**: Trigger and receive Stripe and Slack events — `stripe listen --forward-to localhost:3000/webhooks`
- Check `knowledge` and `prerequisites: node.js, python, ngrok, redis`

### 2. Reason — think for `api-webhook-github-webhooks`
- For `github-webhooks`: Manage GitHub repository webhooks — decide which checks to run
- For `stripe-slack`: Trigger and receive Stripe and Slack events — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-webhook-github-webhooks` tools
- Tools: `Glob`, `Grep`, `Read`, `Gh`, `Stripe` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-webhook-github-webhooks:2c877cb3`

# API Webhook v5 - Integrations

Platform webhook integration patterns.

## What This Skill Does
- Manages GitHub webhooks via API
- Triggers Stripe events locally
- Posts to Slack channels

## When to Use
- CI-driven webhook consumers
- Payment event handling
- Notification pipelines

## Real Commands

```bash
gh api repos/octocat/Hello-World/hooks --method POST -f config.url=https://example.com/hook -f config.content_type=json -f events[]=push
stripe listen --forward-to localhost:3000/webhooks
stripe trigger payment_intent.succeeded
```

## Integration Pattern
1. Listen locally with stripe CLI
2. Trigger a real event
3. Verify signature and payload
4. Process and acknowledge

## Testing
- Trigger each event type
- Check delivery status via APIs
- Verify signature failures are rejected


## Best Practices
- Verify provider signatures always
- Handle delivery retries gracefully
- Log event IDs end-to-end

## Capabilities

### github-webhooks
Manage GitHub repository webhooks

**Parameters:**
- `repo` (string): owner/repo
- `url` (string): Webhook URL
- `events` (array): Event types

**Commands:**
- `gh api repos/octocat/Hello-World/hooks --method POST -f config.url=http://localhost:8080/hook -f config.content_type=json -f events[]=push`
- `gh api repos/octocat/Hello-World/hooks | jq '.[].config.url'`
- `gh api repos/octocat/Hello-World/hooks/1 --method PATCH -f active=false`
- `gh api repos/octocat/Hello-World/hooks/1/deliveries | jq '.[0].status'`

**Examples:**
- gh api POST creates a push webhook
- deliveries endpoints show delivery status
- config.content_type=json sets the payload format

### stripe-slack
Trigger and receive Stripe and Slack events

**Commands:**
- `stripe listen --forward-to localhost:3000/webhooks`
- `stripe trigger payment_intent.succeeded`
- `curl -s -X POST -H "Authorization: Bearer $SLACK_TOKEN" -H 'Content-Type: application/json' -d '{"text":"Deploy complete"}' https://slack.com/api/chat.postMessage`
- `stripe trigger checkout.session.completed`

**Examples:**
- -cli --help
- -api --help

## References
- [GitHub Webhook Docs](https://docs.github.com/en/webhooks)
- [Stripe CLI Docs](https://docs.stripe.com/stripe-cli)