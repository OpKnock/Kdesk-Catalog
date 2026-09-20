---
name: "Lastpass"
description: "Manage credentials with the LastPass CLI (lpass): login, search entries, retrieve passwords, and generate new ones from the terminal."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh"]
alwaysApply: false
---

# Lastpass

Manage credentials with the LastPass CLI (lpass): login, search entries, retrieve passwords, and generate new ones from the terminal.

## Instructions

# LastPass CLI (lpass)

Manage credentials from the terminal with lastpass-cli.

## What this skill does

- Logs into LastPass and manages the local session.
- Searches entries and retrieves passwords non-interactively.
- Generates strong passwords and adds entries.

## When to use

- Scripted credential retrieval in CI or dev tooling.
- Auditing which sites/accounts exist for a vault.
- Generating and storing random credentials.

## Real commands

```bash
# Login (prompts for master password)
lpass login alice@example.com

# Trusted device (fewer OTP prompts)
lpass login --trust alice@example.com

# Status
lpass status

# List entries
lpass ls
lpass ls -l    # include usernames and URLs

# Show password only
lpass show --password example.com

# Show multiple fields
lpass show --username --password --url example.com

# Generate a password into an entry
lpass generate --no-symbols 24 example.com/root

# Add an entry
lpass add --non-interactive --username=bob example.com

# Logout
lpass logout
```

## Testing

```bash
lpass status && lpass ls -l | head -20
```

## Best practices

- Never pipe the master password on the command line; use the prompt.
- Keep the session scoped: logout at the end of scripts.
- Use --no-symbols if target systems reject special characters.

## Capabilities

### lpass-session
Login, logout, and status of the LastPass CLI.

**Commands:**
- `lpass login alice@myapp.test`
- `lpass login --trust alice@myapp.test`
- `lpass status`
- `lpass logout`

**Examples:**
- lpass login alice@example.com
- lpass status
- lpass logout

### lpass-entries
Search, show, and manage credential entries.

**Commands:**
- `lpass ls`
- `lpass ls -l`
- `lpass show --password github.com`
- `lpass show --username --password --url github.com`
- `lpass generate --no-symbols 24 github.com/root`
- `lpass add --non-interactive --username=bob github.com`

**Examples:**
- lpass ls -l
- lpass show --password github.com
- lpass generate --no-symbols 24 github.com/root