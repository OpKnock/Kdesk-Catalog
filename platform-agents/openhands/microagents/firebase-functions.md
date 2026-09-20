---
name: "firebase-functions"
description: "Cloud Functions for Firebase: develop and deploy functions, manage runtimes and environment config, and test locally with the emulator."
type: knowledge
triggers: ["firebase-functions", "functions-lifecycle"]
---

# Firebase Functions

Cloud Functions for Firebase: develop and deploy functions, manage runtimes and environment config, and test locally with the emulator.

## Instructions

# Firebase Functions

## What this skill does

Cloud Functions for Firebase runs backend code on Firebase triggers (auth, Firestore, HTTPS, schedule). This skill covers scaffolding, local emulation, deployment, and config.

## When to use

- Building serverless backends triggered by Firebase events
- Deploying a new version of a function safely
- Testing functions locally before deploy

## Real commands

```bash
# Scaffold and emulate
firebase init functions
firebase emulators:start --only functions

# Deploy (all or specific)
firebase deploy --only functions
firebase deploy --only functions:processOrder

# Runtime config (v1-style config)
firebase functions:config:set stripe.key=sk_live_123
firebase functions:config:get

# List and delete
firebase functions:list
firebase functions:delete processOrder --region us-central1
```

## Function example

```typescript
import { onDocumentCreated } from 'firebase-functions/v2/firestore'

export const onOrderCreated = onDocumentCreated('orders/{orderId}', async (event) => {
  const order = event.data?.data()
  await stripe.charges.create({ amount: order.amount })
  await event.data.ref.update({ charged: true })
})
```

## Testing locally

```bash
firebase emulators:start --only functions,firestore
# trigger a function by writing a document in the emulated Firestore
firebase emulators:exec 'firebase deploy --only functions --dry-run'
```

## Best practices

- Prefer v2 functions (`onDocumentCreated`) with explicit regions.
- Keep functions idempotent; retries mean duplicate invocations.
- Use runtime env vars (v2) over config:set (v1).
- Test with the emulator locally; keep emulator-only endpoints out of prod.
- Set `maxInstances` to avoid runaway billing from hot functions.

## Capabilities

### functions-lifecycle
Scaffold, run, deploy, and configure Cloud Functions for Firebase.

**Commands:**
- `firebase init functions`
- `firebase emulators:start --only functions`
- `firebase deploy --only functions`
- `firebase functions:config:set stripe.key=sk_live_123`
- `firebase functions:list`
- `firebase functions:delete myFunction --region us-central1`

**Examples:**
- firebase init functions && firebase emulators:start --only functions
- firebase functions:config:set stripe.key=sk_live_123 && firebase deploy --only functions
- firebase functions:list
