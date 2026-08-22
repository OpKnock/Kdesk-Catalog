---
name: "keepass"
description: "Manage password databases with keepassxc-cli: create databases, add and search entries, export CSV, and handle attachments from the terminal."
---

# Keepass

Manage password databases with keepassxc-cli: create databases, add and search entries, export CSV, and handle attachments from the terminal.

## Instructions

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
