# Notification Channels

Delivers alerts to Slack via webhooks, email via mailx, SMS via Twilio, and push notifications via ntfy. Supports channel selection by severity and includes rate-limiting guidance.

## Instructions

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
