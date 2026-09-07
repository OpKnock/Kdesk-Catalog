---
applyTo: "**/*.r **/*.sh"
---

Manage password databases with keepassxc-cli: create databases, add and search entries, export CSV, and handle attachments from the terminal.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `keepassxc-cli create db.kdbx`, `keepassxc-cli add -p db.kdbx Web/staging.myapp.test --userna`
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

# KeePassXC (keepassxc-cli)

Manage KeePassXC password databases from the command line.

## What this skill does

- Creates and unlocks .kdbx databases.
- Adds, edits, generates, and deletes entries.
- Exports CSV backups and handles attachments.

## When to use

- Scripting credential rotation across services.
- Migrating secrets into a shared database.
- Automation that needs to fetch a credential at runtime.

## Real commands

```bash
# Create a database (prompts for master password)
keepassxc-cli create db.kdbx

# List groups and entries
keepassxc-cli ls -p db.kdbx

# Show an entry (masked)
keepassxc-cli show -p db.kdbx Web/staging.myapp.test

# Show the password
keepassxc-cli show -p db.kdbx -s Web/staging.myapp.test

# Add an entry
keepassxc-cli add -p db.kdbx Web/staging.myapp.test \
  --username alice --password s3cret

# Generate a strong password into an entry
keepassxc-cli generate -p db.kdbx Web/staging.myapp.test \
  --length 24 --lowercase --uppercase --numbers --special

# Edit username
keepassxc-cli edit -p db.kdbx Web/staging.myapp.test --username alice2

# Export CSV backup
keepassxc-cli export -p db.kdbx -f csv backup.csv

# Attach a file
keepassxc-cli attachment-export -p db.kdbx Web/staging.myapp.test key.pem keyfile.pem

# Delete an entry
keepassxc-cli rm -p db.kdbx Web/staging.myapp.test
```

## Testing

```bash
# Verify the backup parses
head -5 backup.csv
```

## Best practices

- Never pass the master password on the command line; use the prompt.
- Keep exports encrypted; CSV backups contain plaintext secrets.
- Store TOTP seeds as extra fields; pair with oathtool for OTP.

## Capabilities

### db-lifecycle
Create, unlock, and inspect KeePassXC databases.

**Parameters:**
- `db` (string): Database file path.
- `entry` (string): Entry path, e.g. Web/staging.myapp.test.
- `show_secret` (boolean): -s prints the password.

**Commands:**
- `keepassxc-cli create db.kdbx`
- `keepassxc-cli ls -p db.kdbx`
- `keepassxc-cli show -p db.kdbx Web/staging.myapp.test`
- `keepassxc-cli show -p db.kdbx -s Web/staging.myapp.test`
- `keepassxc-cli export -p db.kdbx -f csv backup.csv`

**Examples:**
- keepassxc-cli create db.kdbx
- keepassxc-cli ls -p db.kdbx
- keepassxc-cli show -p db.kdbx -s Web/staging.myapp.test

### entry-ops
Add, edit, generate, and remove entries with attachments.

**Parameters:**
- `entry` (string): Entry path.
- `username` (string): Username for the entry.
- `password` (string): Password for the entry.
- `length` (integer): Generated password length.

**Commands:**
- `keepassxc-cli add -p db.kdbx Web/staging.myapp.test --username alice --password s3cret`
- `keepassxc-cli generate -p db.kdbx Web/staging.myapp.test --length 24 --lowercase --uppercase --numbers --special`
- `keepassxc-cli edit -p db.kdbx Web/staging.myapp.test --username alice2`
- `keepassxc-cli rm -p db.kdbx Web/staging.myapp.test`
- `keepassxc-cli attachment-export -p db.kdbx Web/staging.myapp.test key.pem keyfile.pem`

**Examples:**
- keepassxc-cli add -p db.kdbx Web/staging.myapp.test --username alice --password s3cret
- keepassxc-cli generate -p db.kdbx Web/staging.myapp.test --length 24
- keepassxc-cli attachment-export -p db.kdbx Web/staging.myapp.test key.pem keyfile.pem

## References
- [KeePassXC CLI](https://keepassxc.org/docs/KeePassXC_UserGuide.html#_cli_usage)
- [keepassxc-cli man page](https://github.com/keepassxreboot/keepassxc/blob/develop/docs/man/keepassxc-cli.1)
