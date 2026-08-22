# Firebase Firestore

Cloud Firestore database operations: manage data, indexes, and security rules; read and write documents from the CLI.

## Instructions

# Firebase Firestore

## What this skill does

Firestore is a NoSQL document database with realtime sync. This skill covers CLI data ops, index management (composite indexes for multi-field queries), and security rules deployment.

## When to use

- Administering Firestore data from the command line
- Deploying rules and indexes with the rest of your code
- Debugging queries that fail with missing-index errors

## Real commands

```bash
# Show required indexes
firebase firestore:indexes

# Deploy rules and indexes
firebase deploy --only firestore:rules
firebase deploy --only firestore:indexes

# Dangerous cleanup (with confirmation)
firebase firestore:delete --all-collections --yes

# Query via Admin SDK
node -e "const admin=require('firebase-admin');admin.initializeApp();admin.firestore().collection('orders').where('status','==','paid').limit(5).get().then(s=>console.log(s.size))"
```

## firestore.rules example

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /orders/{orderId} {
      allow read: if request.auth != null && resource.data.owner == request.auth.uid;
      allow write: if request.auth != null && request.auth.uid == request.auth.uid;
    }
  }
}
```

## Composite index pattern

```json
{
  "indexes": [
    {
      "collectionGroup": "orders",
      "queryScope": "COLLECTION",
      "fields": [
        {"fieldPath": "status", "order": "ASCENDING"},
        {"fieldPath": "createdAt", "order": "DESCENDING"}
      ]
    }
  ]
}
```

## Testing

```bash
# Rules emulator for local validation
firebase emulators:start --only firestore
firebase deploy --only firestore:rules --dry-run
```

## Best practices

- Design queries around indexes first; multi-field inequality filters need composites.
- Test rules with the emulator before deploying.
- Use `--dry-run` for rules deploys.
- Batch writes over sequential ones; keep documents small (<1MB).
- Never run `firestore:delete --all-collections` against production without a backup.

## Capabilities

### firestore-data
Read, write, and administer Firestore data, indexes, and rules.

**Commands:**
- `firebase firestore:indexes`
- `firebase deploy --only firestore:rules`
- `firebase deploy --only firestore:indexes`
- `firebase firestore:delete --all-collections --yes`
- `node -e "const admin=require('firebase-admin');admin.initializeApp();admin.firestore().collection('orders').where('status','==','paid').limit(5).get().then(s=>console.log(s.size))"`

**Examples:**
- firebase deploy --only firestore:rules
- firebase deploy --only firestore:indexes
- node -e "const admin=require('firebase-admin');admin.initializeApp();admin.firestore().collection('orders').where('status','==','paid').limit(5).get().then(s=>console.log(s.size))"
