Delivers alerts to Slack via webhooks, email via mailx, SMS via Twilio, and push notifications via ntfy. Supports channel selection by severity and includes rate-limiting guidance.

## Agentic Workflow: Read -> Reason -> Act (notification-channels)

You are **Notification Channels** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `notification-channels`
- Domain: Delivers alerts to Slack via webhooks, email via mailx, SMS via Twilio, and push notifications via ntfy. Supports channel selection by severity and includes rate-limiting guidance.
- **notification-delivery**: Deliver messages to Slack, email, Twilio SMS and ntfy topics using curl and CLI tools. — `curl -X POST -H 'Content-type: application/json' --data '{"text":"Deploy complet`
- Check `knowledge` and `prerequisites: echo, ntfy`

### 2. Reason — think for `notification-channels`
- For `notification-delivery`: Deliver messages to Slack, email, Twilio SMS and ntfy topics using curl and CLI tools. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `notification-channels` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Echo` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `notification-channels:e61c0c10`

# Notification Channels

Route alerts to the right channel per severity: pages, chat, email and push.

## What this skill does

- Posts messages to Slack webhooks
- Sends email via mailx
- Sends SMS via Twilio and pushes via ntfy

## When to use

- Wiring alertmanager or cron alerts to humans
- Choosing a channel for a given severity

## Real commands

```bash
# Slack webhook
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Deploy complete"}' \
  https://hooks.slack.com/services/T000/B000/XXX

# Email
printf 'Body\n' | mailx -s "Subject" -r alerts@your-app.test oncall@your-app.test

# Twilio SMS
curl -X POST https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "From=+15559876543" \
  --data-urlencode "Body=Alert: high latency" \
  -u "$TWILIO_SID:$TWILIO_TOKEN"

# ntfy push
ntfy publish mytopic "Server down!"
curl -d "pipeline failed" ntfy.sh/mytopic
```

## Channel guidance

- Pager/critical: SMS or phone call
- Normal ops: Slack or ntfy
- Reports: email

## Best practices

- Include severity, service and runbook link in every alert
- Rate-limit notifications to avoid alert storms
- Test each channel with a canned message first

## Capabilities

### notification-delivery
Deliver messages to Slack, email, Twilio SMS and ntfy topics using curl and CLI tools.

**Parameters:**
- `channel` (string): slack, email, sms or ntfy
- `message` (string): Message body text
- `recipient` (string): Webhook URL, email address or phone number

**Commands:**
- `curl -X POST -H 'Content-type: application/json' --data '{"text":"Deploy complete"}' https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
- `echo "Body text" | mailx -s "Subject" -r alerts@your-app.test oncall@your-app.test`
- `curl -X POST https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json --data-urlencode "To=+15551234567" --data-urlencode "From=+15559876543" --data-urlencode "Body=Alert: high latency" -u "$TWILIO_SID:$TWILIO_TOKEN"`
- `ntfy publish mytopic "Server down!"`
- `curl -d "pipeline failed" ntfy.sh/mytopic`

**Examples:**
- curl -X POST -H 'Content-type: application/json' --data '{"text":":warning: CPU at 95%"}' https://hooks.slack.com/services/T000/B000/XXX
- ntfy publish --title "CI" mytopic "build #42 passed"
- curl -d "disk nearly full" https://ntfy.sh/ops-alerts

## References
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [ntfy docs](https://docs.ntfy.sh/publish/)
- [Twilio Messaging API](https://www.twilio.com/docs/messaging/api)
