---
trigger: glob
description: "Integrates with platform webhooks: GitHub repository hooks, Stripe event triggers, Slack incoming webhooks, and signature verification patterns. Use when working with github webhooks, stripe slack or when the user mentions github webhooks, stripe slack."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Integrates with platform webhooks: GitHub repository hooks, Stripe event triggers, Slack incoming webhooks, and signature verification patterns.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh api repos/octocat/Hello-World/hooks --method POST -f conf`, `stripe listen --forward-to localhost:3000/webhooks`
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
