---
name: "Gopass"
description: "Initialize stores, insert/read secrets, manage recipients, and generate passwords. secrets and recipients, and use templates for structured entries.'"
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Gopass

Initialize stores, insert/read secrets, manage recipients, and generate passwords. secrets and recipients, and use templates for structured entries.'

## Instructions

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