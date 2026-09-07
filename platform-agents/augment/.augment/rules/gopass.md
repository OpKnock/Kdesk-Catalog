---
type: agent_requested
description: "Initialize stores, insert/read secrets, manage recipients, and generate passwords. secrets and recipients, and use templates for structured entries.'. Use when working with gopass store, api or when the user mentions gopass store, api."
---

Initialize stores, insert/read secrets, manage recipients, and generate passwords. secrets and recipients, and use templates for structured entries.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gopass init --store=team`
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

# gopass

## What this skill does

gopass is a password manager for teams, storing secrets in git-encrypted stores with GPG. It supports multiple stores, recipients, templates, and structured entries with JSON/yaml values.

## When to use

- Sharing service credentials across a team
- Keeping secrets in git (encrypted) with a full history
- Managing machine accounts, API keys, and DB passwords

## Real commands

```bash
# Initialize (root or named store)
gopass init
gopass init --store=team

# Insert and read secrets
gopass insert team/db/postgres
gopass show team/db/postgres

# Generate a strong password
gopass generate team/aws/access-key 24

# Recipients and sync
gopass recipients add alice@example.com --store=team
gopass sync --store=team

# List a tree
 gopass list team/db
```

## Structured secret example

```bash
gopass insert team/db/postgres
# paste:
url: postgres://db:5432
username: app
password: s3cret
```

```bash
# Read one field
gopass show team/db/postgres password
```

## Templates

```bash
gopass templates edit
gopass templates show db
```

## Testing

```bash
# Round trip and diff on git history
 gopass show team/db/postgres password | wc -c
 cd $(gopass config --format=json | jq -r '.path')
 git log --oneline -3
```

## Best practices

- Add every teammate who must read the store as a recipient.
- Store one credential per entry with structured fields.
- Use `gopass sync` in CI to keep shared stores converged.
- Rotate secrets by generating new values, never editing in place blindly.
- Back up the store git remote; encryption keys are the real risk.

## Capabilities

### gopass-store
Initialize stores, insert/read secrets, manage recipients, and generate passwords.

**Parameters:**
- `store` (string): Store name (root or named store)
- `path` (string): Secret path like team/db/postgres
- `length` (integer): Generated password length

**Commands:**
- `gopass init --store=team`
- `gopass insert team/db/postgres`
- `gopass generate team/aws/access-key 24`
- `gopass show team/db/postgres`
- `gopass recipients add alice@localhost --store=team`
- `gopass list team/db`
- `gopass sync --store=team`

**Examples:**
- gopass generate team/aws/access-key 24
- gopass show team/db/postgres
- gopass recipients add alice@localhost --store=team && gopass sync --store=team

## References
- [gopass documentation](https://www.gopass.pw/docs/)
- [gopass usage guide](https://www.gopass.pw/docs/features/)