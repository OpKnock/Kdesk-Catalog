---
name: "firebase-functions"
description: "Cloud Functions for Firebase: develop and deploy functions, manage runtimes and environment config, and test locally with the emulator. Use when working with functions lifecycle, api or when the user mentions functions lifecycle, api."
---

Cloud Functions for Firebase: develop and deploy functions, manage runtimes and environment config, and test locally with the emulator.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `firebase init functions`
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
