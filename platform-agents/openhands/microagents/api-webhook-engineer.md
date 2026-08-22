---
name: "api-webhook-engineer"
description: "Implements webhook delivery in Node.js: receiver endpoints, retry with backoff, delivery logging, and idempotent handling of events."
type: knowledge
triggers: ["api-webhook-engineer", "webhook-receiver", "retry-policy"]
---

# api-webhook-engineer

Implements webhook delivery in Node.js: receiver endpoints, retry with backoff, delivery logging, and idempotent handling of events.

## Instructions

# API Webhook Engineer

Webhook delivery implementation.

## What This Skill Does
- Receives and processes webhook events
- Implements retries with exponential backoff
- Logs deliveries for debugging

## When to Use
- Building webhook receivers
- Adding reliable event delivery
- Handling third-party webhooks

## Real Commands

```bash
npm install express
node server.js
curl -s -X POST http://localhost:3000/webhooks -H 'Content-Type: application/json' -d '{"event":"order.created","data":{"id":1}}' -w '\n%{http_code}\n'
```

## Receiver Pattern

```js
app.post('/webhooks', async (req, res) => {
  const key = req.body.id || hash(req.body);
  if (await processed(key)) return res.sendStatus(200);
  await processEvent(req.body);
  res.sendStatus(200);
});
```

## Testing
- Replay events and verify idempotency
- Simulate handler failure and check retries
- Verify logs capture delivery attempts


## Best Practices
- Respond 200 fast, process asynchronously
- Use idempotency keys for every event
- Log delivery metadata with event IDs

## Capabilities

### webhook-receiver
Build a webhook receiver endpoint

**Commands:**
- `npm install express`
- `node server.js`
- `curl -s -X POST http://localhost:3000/webhooks -H 'Content-Type: application/json' -d '{"event":"order.created","data":{"id":1}}' -w '\n%{http_code}\n'`
- `curl -s -X POST http://localhost:3000/webhooks -H 'Content-Type: application/json' -d '{"event":"order.created","data":{"id":1}}' -w '\n%{http_code}\n'`
- `curl -s http://localhost:3000/webhooks/log | jq 'length'`

**Examples:**
- POST /webhooks receives events
- Replaying the same event is idempotent
- Delivery logs record every attempt

### retry-policy
Retry failed deliveries with backoff

**Commands:**
- `npm install p-retry`
- `node -e "const pRetry=require('p-retry'); const send=()=>Promise.reject(new Error('down')); pRetry(send,{retries:3,factor:2}).catch(e=>console.log('gave up:',e.message))"`
- `node -e "const r=require('retry'); const o=r.operation({retries:4,factor:2,minTimeout:1000}); o.attempt(n=>console.log('attempt',n))"`
