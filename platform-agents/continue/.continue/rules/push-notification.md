---
name: "Push Notification"
description: "Deliver mobile notifications via FCM v1, legacy FCM, and APNs HTTP/2 using curl with OAuth tokens and certificate-based auth."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Push Notification

Deliver mobile notifications via FCM v1, legacy FCM, and APNs HTTP/2 using curl with OAuth tokens and certificate-based auth.

## Instructions

# Push Notifications

Send notifications to iOS and Android devices through FCM and APNs.

## What this skill does

- Sends FCM v1 messages with OAuth tokens
- Sends legacy FCM requests
- Pushes to APNs over HTTP/2

## When to use

- Triggering notifications from backend events
- Testing delivery with curl before building

## Real commands

```bash
# FCM v1: get OAuth token, then send
 gcloud auth application-default print-access-token
curl -X POST -H "Authorization: Bearer $FCM_TOKEN" -H "Content-Type: application/json" \
  -d @fcm.json "https://fcm.googleapis.com/v1/projects/my-firebase-project/messages:send"

# FCM legacy
curl -X POST -H "Authorization: key=$FCM_LEGACY_KEY" -H "Content-Type: application/json" \
  -d '{"to":"DEVICE_TOKEN","notification":{"title":"Hi","body":"Hello"}}' \
  https://fcm.googleapis.com/fcm/send

# APNs
curl -d '{"aps":{"alert":"Hello","sound":"default"}}' \
  -H "apns-topic: com.mycompany.myapp" --cert apns.pem \
  https://api.push.apple.com/3/device/DEVICE_TOKEN
```

## fcm.json (v1)

```json
{
  "message": {
    "token": "DEVICE_TOKEN",
    "notification": { "title": "Hi", "body": "Hello" },
    "data": { "screen": "orders" }
  }
}
```

## Best practices

- Store device tokens per user and refresh on invalid-token errors
- Use data payloads for background handling
- Send to topic groups (FCM) instead of one-by-one at scale

## Capabilities

### push-notification-delivery
Send notifications via FCM and APNs using curl and the gcloud token flow.

**Commands:**
- `gcloud auth application-default print-access-token`
- `curl -X POST -H "Authorization: Bearer $FCM_TOKEN" -H "Content-Type: application/json" -d @fcm.json "https://fcm.googleapis.com/v1/projects/my-firebase-project/messages:send"`
- `curl -X POST -H "Authorization: key=$FCM_LEGACY_KEY" -H "Content-Type: application/json" -d '{"to":"DEVICE_TOKEN","notification":{"title":"Hi","body":"Hello"}}' https://fcm.googleapis.com/fcm/send`
- `curl -d '{"aps":{"alert":"Hello","sound":"default"}}' -H "apns-topic: com.mycompany.myapp" --cert apns.pem https://api.push.apple.com/3/device/DEVICE_TOKEN`
- `curl -s -X POST -H "Authorization: Bearer $FCM_TOKEN" -H "Content-Type: application/json" -d @fcm.json "https://fcm.googleapis.com/v1/projects/my-firebase-project/messages:send" | jq .`

**Examples:**
- curl -X POST -H "Authorization: key=$FCM_LEGACY_KEY" -H "Content-Type: application/json" -d '{"to":"DEVICE_TOKEN","data":{"type":"order"}}' https://fcm.googleapis.com/fcm/send
- curl -d '{"aps":{"alert":"Order shipped"}}' -H "apns-topic: com.mycompany.myapp" --cert apns.pem https://api.push.apple.com/3/device/DEVICE_TOKEN
- gcloud auth application-default print-access-token > /tmp/fcm_token