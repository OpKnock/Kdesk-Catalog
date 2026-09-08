---
name: "firebase-functions"
description: "Cloud Functions for Firebase: develop and deploy functions, manage runtimes and environment config, and test locally with the emulator. Use when working with functions lifecycle, api or when the user mentions functions lifecycle, api."
license: "MIT"
compatibility: "Requires firebase."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(firebase:*)"
---

Cloud Functions for Firebase: develop and deploy functions, manage runtimes and environment config, and test locally with the emulator.

## Agentic Workflow: Read -> Reason -> Act (firebase-functions)

You are **Firebase Functions** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `firebase-functions`
- Domain: Cloud Functions for Firebase: develop and deploy functions, manage runtimes and environment config, and test locally with the emulator.
- **functions-lifecycle**: Scaffold, run, deploy, and configure Cloud Functions for Firebase. — `firebase init functions`
- Check `knowledge` and `prerequisites: firebase`

### 2. Reason — think for `firebase-functions`
- For `functions-lifecycle`: Scaffold, run, deploy, and configure Cloud Functions for Firebase. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `firebase-functions` tools
- Tools: `Glob`, `Grep`, `Read`, `Firebase` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `firebase-functions:d8f03c8b`

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

**Parameters:**
- `function-name` (string): Function to deploy or delete
- `region` (string): Deployment region, e.g. us-central1
- `runtime` (string): Node version for the functions runtime

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

## References
- [Cloud Functions docs](https://firebase.google.com/docs/functions)
- [Firebase Emulator Suite](https://firebase.google.com/docs/emulator-suite)
