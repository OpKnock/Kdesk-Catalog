Firestore realtime updates: subscribe to document and collection snapshots, handle listener lifecycle, and debug sync lag.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node -e "const {onSnapshot,doc}=require('firebase/firestore'`
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

# Firestore Realtime

## What this skill does

Firestore pushes document changes to subscribed clients via snapshot listeners. `onSnapshot` fires on server updates, local writes, and cache events; listeners auto-reconnect and dedupe.

## When to use

- Chat, presence, or collaborative screens
- Dashboards that must reflect DB state instantly
- Any screen that should update without polling

## Real commands

```bash
# Document listener
node -e "const {onSnapshot,doc}=require('firebase/firestore');onSnapshot(doc(db,'orders','o1'),s=>console.log(s.data()));setTimeout(()=>{},10000)"

# Query listener with filter
node -e "const {onSnapshot,collection,query,where}=require('firebase/firestore');onSnapshot(query(collection(db,'orders'),where('status','==','paid')),s=>console.log('size',s.size))"

# Unsubscribe properly
node -e "const unsub=onSnapshot(doc(db,'orders','o1'),()=>{});setTimeout(unsub,5000);console.log('unsubscribed')"

# Find all listeners in code
 grep -rn 'onSnapshot' src/ | head -10
```

## Metadata handling

```javascript
onSnapshot(docRef, { includeMetadataChanges: true }, (snap) => {
  if (snap.metadata.hasPendingWrites) console.log('local write, not yet on server')
  if (!snap.metadata.isFromCache) console.log('fresh from server')
})
```

## Testing

```bash
firebase emulators:start --only firestore
# write a doc via the emulator UI and watch the listener fire
node -e "const {setDoc,doc}=require('firebase/firestore');setDoc(doc(db,'orders','o1'),{status:'paid'})"
```

## Best practices

- Always store the unsubscribe function and call it on screen teardown.
- Prefer filtered queries over listening to whole collections.
- Use `includeMetadataChanges` to distinguish cache vs server events.
- Cap concurrent listeners; each one is a connection/session on the backend.
- Handle listener errors: log, retry, and surface offline state.

## Capabilities

### realtime-listeners
Attach, manage, and debug Firestore snapshot listeners.

**Parameters:**
- `document-path` (string): Document to listen to
- `query-filter` (string): Where clause for collection listeners
- `listener-name` (string): Label used in logs to identify the listener

**Commands:**
- `node -e "const {onSnapshot,doc}=require('firebase/firestore');onSnapshot(doc(db,'orders','o1'),s=>console.log(s.data()));setTimeout(()=>{},10000)"`
- `node -e "const {onSnapshot,collection,query,where}=require('firebase/firestore');onSnapshot(query(collection(db,'orders'),where('status','==','paid')),s=>console.log('size',s.size))"`
- `grep -rn 'onSnapshot' src/ | head -10`
- `firebase emulators:start --only firestore`
- `node -e "const unsub=onSnapshot(doc(db,'orders','o1'),()=>{});setTimeout(unsub,5000);console.log('unsubscribed')"`

**Examples:**
- node -e "const {onSnapshot,doc}=require('firebase/firestore');onSnapshot(doc(db,'orders','o1'),s=>console.log(s.data()));setTimeout(()=>{},10000)"
- node -e "const {onSnapshot,collection,query,where}=require('firebase/firestore');onSnapshot(query(collection(db,'orders'),where('status','==','paid')),s=>console.log('size',s.size))"
- grep -rn 'onSnapshot' src/ | head -10

## References
- [Listen to realtime updates](https://firebase.google.com/docs/firestore/query-data/listen)
- [Get realtime updates (web SDK)](https://firebase.google.com/docs/firestore/query-data/listen#web_2)