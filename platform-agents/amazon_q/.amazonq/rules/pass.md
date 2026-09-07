Manages secrets using the password store utility: initializes GPG-encrypted stores, generates and inserts passwords and API tokens, and syncs via git enabling CLI-centric secret management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pass init "FINGERPRINT"`
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

# pass

pass stores secrets as GPG-encrypted files in a git-tracked directory.

## What this skill does

- Initializes stores with a GPG key
- Generates and inserts passwords/API tokens
- Syncs the store with git

## When to use

- CLI-centric secret management on servers
- Committing encrypted secrets to git

## Real commands

```bash
# Initialize
pass init "ABCD1234..."

# Generate (no symbols, 20 chars)
pass generate -n Email/example 20
pass generate --no-symbols -l 24 server/root

# Insert and view
pass insert dev/apitoken
pass show dev/apitoken
pass show -c dev/apitoken   # copy to clipboard

# Edit multi-line
pass edit dev/credentials

# List and git
pass ls
pass git status
pass git push
```

## Multiline entries

```
password123
---
url: https://example.com
username: alice
```

## Best practices

- Use `-c` to copy instead of printing secrets to logs
- Keep the store in a private git repo with GPG-only access
- Rotate keys by re-encrypting with `pass init` and old recipients

## Capabilities

### pass-passwordstore
Initialize the password store, generate and manage secrets with pass, and sync via git.

**Parameters:**
- `path` (string): Store path, e.g. dev/apitoken
- `length` (integer): Generated password length
- `no_symbols` (boolean): Exclude symbols from generation

**Commands:**
- `pass init "FINGERPRINT"`
- `pass generate -n Email/example 20`
- `pass insert dev/apitoken`
- `pass show dev/apitoken`
- `pass edit dev/apitoken`

**Examples:**
- pass generate --no-symbols -l 24 server/root
- pass ls
- pass git push

## References
- [pass Official Site](https://www.passwordstore.org/)
- [pass man page](https://git.zx2c4.com/password-store/about/)