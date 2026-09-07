---
trigger: glob
description: "Manages passwords and secrets with the Bitwarden CLI: login, item CRUD, generation, exports, and sync. Use when working with auth session, item management, generation export, api or when the user mentions auth session, item management, generation export, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh"]
---

Manages passwords and secrets with the Bitwarden CLI: login, item CRUD, generation, exports, and sync.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bw login`, `bw get password https://api.your-app.test`
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

# Bitwarden

## What this skill does

Manages passwords and secrets with the Bitwarden CLI (bw): login/unlock, item CRUD, password generation, exports, and TOTP retrieval.

## When to use

- Fetching a stored credential for a script or deploy
- Generating strong passwords
- Migrating or exporting a vault

## Real commands

```bash
# Login and unlock
bw login user@api.your-app.test
bw unlock --raw
bw status

# Search and read
bw list items --search github
bw get password https://stripe.com
bw get item prod-db

# Create an item
BW_SESSION=$(bw unlock --raw)
echo '{"type":1,"name":"prod-db","login":{"username":"admin","password":"secret"}}' | bw create item --session $BW_SESSION

# Generate
bw generate -l 24 -n -s

# Export
bw export --format json --output vault.json --session $BW_SESSION
```

## Testing

- Run bw sync after external changes
- Verify exports import cleanly (json preferred)

## Best practices

- Keep BW_SESSION out of logs; use --session carefully
- Rotate shared passwords via item edits
- Use TOTP items with bw get totp for 2FA flows
- Export only to trusted, encrypted storage

## Capabilities

### auth-session
Log in, unlock, and manage CLI sessions.

**Parameters:**
- `email` (string): Account email
- `raw` (boolean): Print raw session token

**Commands:**
- `bw login`
- `bw unlock`
- `bw status`
- `bw logout`
- `bw sync`

**Examples:**
- bw login user@api.your-app.test
- bw unlock --raw | pbcopy
- bw status | jq '.status'

### item-management
Create, read, update, and delete vault items.

**Parameters:**
- `search` (string): Search query
- `item_id` (string): Item ID or search term

**Commands:**
- `bw get password https://api.your-app.test`
- `bw list items --search github`
- `bw get item my-api-key`
- `bw create item --session $BW_SESSION`
- `bw delete item item-12345`

**Examples:**
- bw list items --search aws | jq '.[].login.username'
- bw get password https://stripe.com
- echo '{"type":1,"name":"prod-db","login":{"username":"admin","password":"secret"}}' | bw create item

### generation-export
Generate passwords and export vaults.

**Parameters:**
- `length` (number): Password length (-l)
- `export_format` (string): json or csv

**Commands:**
- `bw generate -l 20 -n -s`
- `bw generate -u -l 24`
- `bw export --format json --output bw.json --session $BW_SESSION`
- `bw export --format csv --output bw.csv`
- `bw get totp item-12345`

**Examples:**
- bw generate -l 24 -n -s --base64
- bw export --format json --output vault.json
- bw get totp google

## References
- [Bitwarden CLI Docs](https://bitwarden.com/help/cli/)
- [Bitwarden API](https://bitwarden.com/help/api/)
