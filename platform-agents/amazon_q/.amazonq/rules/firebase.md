Develops Firebase projects with the Firebase CLI: hosting, functions, Firestore, emulators, and deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g firebase-tools`, `firebase deploy`
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

# Firebase

Develop and deploy Firebase apps.

## When to Use

- Static hosting with CDN (hosting)
- Serverless functions (Cloud Functions)
- NoSQL data with Firestore
- Local development with the emulator suite

## Commands

```bash
# Setup
npm install -g firebase-tools
firebase login
firebase init hosting
firebase init functions
firebase use --add

# Deploy
firebase deploy
firebase deploy --only hosting
firebase deploy --only functions:api

# Local
firebase serve --only hosting
firebase emulators:start
firebase emulators:exec "npm test"

# Firestore
firebase firestore:delete --all-collections -y
firebase deploy --only firestore:rules
firebase firestore:indexes
```

## Security Rules Example

```
rules_version = "2";
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

## Best Practices

- Develop against emulators before touching the real project
- Test security rules with the rules emulator
- Separate staging and production projects
- Pin firebase-tools versions in CI
- Deploy functions and hosting independently during rollouts
- Review generated .firebaserc so deploys target the right project

## Capabilities

### firebase-init
Initialize and configure Firebase projects.

**Parameters:**
- `project` (string): Firebase project id
- `features` (string): hosting, functions, firestore, emulators

**Commands:**
- `npm install -g firebase-tools`
- `firebase login`
- `firebase init hosting`
- `firebase init functions`
- `firebase use --add`

**Examples:**
- firebase init --hosting --project myproject
- firebase projects:list
- firebase use myproject

### firebase-deploy
Deploy hosting and functions.

**Parameters:**
- `only` (string): Targets: hosting, functions:name
- `config` (string): firebase.json config path

**Commands:**
- `firebase deploy`
- `firebase deploy --only hosting`
- `firebase deploy --only functions:api`
- `firebase serve`
- `firebase emulators:start`

**Examples:**
- firebase deploy --only functions
- firebase emulators:start --only firestore
- firebase serve --only hosting

### firestore-ops
Manage Firestore data and rules.

**Parameters:**
- `collection` (string): Collection to delete
- `rules` (string): Firestore rules file path

**Commands:**
- `firebase firestore:delete --all-collections -y`
- `firebase deploy --only firestore:rules`
- `firebase emulators:exec "npm test"`
- `firebase firestore:indexes`

**Examples:**
- firebase firestore:delete users -y
- firebase emulators:start --import ./seed

## References
- [Firebase Docs](https://firebase.google.com/docs)
- [Firebase CLI Reference](https://firebase.google.com/docs/cli)