---
applyTo: "**/*.go **/*.r **/*.rs **/*.sh"
---

Manage credentials with the LastPass CLI (lpass): login, search entries, retrieve passwords, and generate new ones from the terminal.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `lpass login alice@myapp.test`, `lpass ls`
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
