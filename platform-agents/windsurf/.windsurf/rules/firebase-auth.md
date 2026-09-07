---
trigger: glob
description: "Firebase Authentication operations: manage users and ID tokens, test sign-in flows with the CLI, and verify token validation. Use when working with auth admin, api or when the user mentions auth admin, api."
globs: ["**/*.go", "**/*.java", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
---

Firebase Authentication operations: manage users and ID tokens, test sign-in flows with the CLI, and verify token validation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `firebase auth:list`
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

# Firebase Auth

## What this skill does

Firebase Auth handles email/password, social, and phone sign-ins, and issues ID tokens. The CLI and Admin SDK manage users, imports, custom tokens, and token verification.

## When to use

- Managing user accounts from the command line
- Migrating users between projects via import/export
- Verifying ID tokens server-side

## Real commands

```bash
# List and manage users
firebase auth:list
firebase auth:create user@example.com
firebase auth:delete user@example.com

# Import users (hash config required for passwords)
firebase auth:import users.json

# Mint an ID token for a Google OAuth token
firebase auth:token google-oauth-token

# Verify an ID token with the Admin SDK
node -e "const admin=require('firebase-admin');admin.initializeApp();admin.auth().verifyIdToken('ID_TOKEN').then(d=>console.log(d.uid,d.email)).catch(console.error)"
```

## users.json import example

```json
{
  "users": [
    {
      "localId": "user-1",
      "email": "a@example.com",
      "emailVerified": true,
      "passwordHash": "base64-encoded-hash",
      "salt": "base64-salt"
    }
  ]
}
```

## Custom claims

```javascript
await admin.auth().setCustomUserClaims(uid, { role: 'admin' })
```

## Testing

```bash
# Round trip: create -> sign in via REST -> verify
curl -s -X POST 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=$API_KEY' -H 'Content-Type: application/json' -d '{"email":"user@example.com","password":"pw","returnSecureToken":true}' | jq '.idToken | length > 0'
```

## Best practices

- Always verify ID tokens server-side with the Admin SDK; never trust client claims.
- Check `exp` and `auth_time` claims in token verification.
- Use custom claims for roles, not for frequent-changing data.
- Set a session revocation policy for sensitive apps (verifyIdToken with checkRevoked).

## Capabilities

### auth-admin
Administer Firebase Auth users, issue custom tokens, and verify ID tokens.

**Parameters:**
- `email` (string): User email to create or delete
- `id-token` (string): ID token to verify
- `import-file` (string): JSON file with users to import

**Commands:**
- `firebase auth:list`
- `firebase auth:import users.json`
- `firebase auth:create user@localhost`
- `firebase auth:token google-oauth-token`
- `node -e "const admin=require('firebase-admin');admin.initializeApp();admin.auth().verifyIdToken('ID_TOKEN').then(d=>console.log(d.uid,d.email)).catch(console.error)"`
- `firebase auth:delete user@localhost`

**Examples:**
- firebase auth:list
- firebase auth:import users.json
- node -e "const admin=require('firebase-admin');admin.initializeApp();admin.auth().verifyIdToken('ID_TOKEN').then(d=>console.log(d.uid,d.email)).catch(console.error)"

## References
- [Firebase Auth REST API](https://firebase.google.com/docs/reference/rest/auth)
- [Admin SDK verifyIdToken](https://firebase.google.com/docs/auth/admin/verify-id-tokens)
