---
trigger: glob
description: "Manage credentials with the LastPass CLI (lpass): login, search entries, retrieve passwords, and generate new ones from the terminal. Use when working with lpass session, lpass entries, api or when the user mentions lpass session, lpass entries, api."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh"]
---

Manage credentials with the LastPass CLI (lpass): login, search entries, retrieve passwords, and generate new ones from the terminal.

## Agentic Workflow: Read -> Reason -> Act (lastpass)

You are **Lastpass** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `lastpass`
- Domain: Manage credentials with the LastPass CLI (lpass): login, search entries, retrieve passwords, and generate new ones from the terminal.
- **lpass-session**: Login, logout, and status of the LastPass CLI. — `lpass login alice@myapp.test`
- **lpass-entries**: Search, show, and manage credential entries. — `lpass ls`
- Check `knowledge` and `prerequisites: lpass`

### 2. Reason — think for `lastpass`
- For `lpass-session`: Login, logout, and status of the LastPass CLI. — decide which checks to run
- For `lpass-entries`: Search, show, and manage credential entries. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `lastpass` tools
- Tools: `Glob`, `Grep`, `Read`, `Lpass` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `lastpass:57378403`

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

**Parameters:**
- `email` (string): LastPass account email.
- `trust` (boolean): Trust the device for this session.

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

**Parameters:**
- `search` (string): Entry search term or full path.
- `username` (string): Username for new entries.
- `length` (integer): Generated password length.

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

## References
- [LastPass CLI](https://github.com/lastpass/lastpass-cli)
- [lpass man page](https://lastpass.github.io/lastpass-cli/lpass.1.html)
