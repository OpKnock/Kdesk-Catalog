---
trigger: glob
description: "Firestore offline persistence: enable local caching, debug cache reads, and design apps that work when connectivity drops. Use when working with offline persistence, api or when the user mentions offline persistence, api."
globs: ["**/*.java", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
---

Firestore offline persistence: enable local caching, debug cache reads, and design apps that work when connectivity drops.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node -e "const db=require('firebase/firestore');firebase.fir`
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

# Firestore Offline

## What this skill does

Firestore caches data locally so reads and queued writes continue offline. Mobile SDKs enable persistence by default; web needs explicit settings. This skill covers enabling and verifying the cache.

## When to use

- Mobile apps that must work on subways/airplanes
- Web apps wanting instant re-renders from cache
- Queuing writes that happened offline

## Real commands

```bash
# Web: persistent cache with IndexedDB tab manager
node -e "const {initializeFirestore,persistentLocalCache,indexedDbLocalCache}=require('firebase/firestore');const db=initializeFirestore(app,{localCache:persistentLocalCache({tabManager:indexedDbLocalCache()})});console.log(db)"

# Older web SDK pattern
firebase.firestore().enablePersistence().catch(e => console.log('multi-tab needs config'))

# Local emulation to test offline behavior
firebase emulators:start --only firestore

# Audit cache config in the codebase
 grep -rn 'enablePersistence\|persistentLocalCache' src/ | head -10
```

## Read source options

```javascript
// Server-first vs cache-first reads
import { getDoc, source } from 'firebase/firestore'
const snap = await getDoc(docRef, { source: source.server })
const cached = await getDoc(docRef, { source: source.cache })
```

## Testing offline behavior

```bash
# Simulate offline: kill the emulator or disable the network
firebase emulators:start --only firestore
# load the page, disconnect, verify reads still render from cache
```

## Best practices

- Web: pick `persistentLocalCache` explicitly; avoid mixing persistence modes per tab.
- Use `multiTabLocalCache` for multi-tab consistency on web.
- Remember cache-only data may be stale: use `snapshotListeners` to reconcile.
- Test with `getDoc(docRef, { source: source.cache })` to force cache reads.
- Handle `failed-precondition` errors (persistence unavailable) gracefully.

## Capabilities

### offline-persistence
Enable and debug offline persistence, and verify cache behavior in client SDKs.

**Parameters:**
- `cache-mode` (string): persistent or memory local cache mode
- `tab-manager` (string): indexedDbLocalCache or multiTabLocalCache
- `settings-file` (string): File where Firestore settings are configured

**Commands:**
- `node -e "const db=require('firebase/firestore');firebase.firestore().settings({persistence: true});firebase.firestore().enablePersistence().then(()=>console.log('offline ok'))"`
- `node -e "const {initializeFirestore,persistentLocalCache,indexedDbLocalCache}=require('firebase/firestore');const db=initializeFirestore(app,{localCache:persistentLocalCache({tabManager:indexedDbLocalCache()})});console.log(db)"`
- `firebase emulators:start --only firestore`
- `grep -rn 'enablePersistence\|persistentLocalCache' src/ | head -10`
- `curl -s 'http://localhost:8080/api/cache-stats' | jq '.localDocuments'`

**Examples:**
- node -e "const {initializeFirestore,persistentLocalCache,indexedDbLocalCache}=require('firebase/firestore');const db=initializeFirestore(app,{localCache:persistentLocalCache({tabManager:indexedDbLocalCache()})});console.log(db)"
- firebase emulators:start --only firestore
- grep -rn 'enablePersistence\|persistentLocalCache' src/ | head -10

## References
- [Firestore offline data](https://firebase.google.com/docs/firestore/manage-data/enable-offline)
- [Firestore cache semantics](https://firebase.google.com/docs/firestore/manage-data/enable-offline#monitor_network_status)
