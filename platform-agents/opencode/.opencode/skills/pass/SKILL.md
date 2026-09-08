---
name: "pass"
description: "Manages secrets using the password store utility: initializes GPG-encrypted stores, generates and inserts passwords and API tokens, and syncs via git enabling CLI-centric secret management. Use when working with pass passwordstore, api or when the user mentions pass passwordstore, api."
---

Manages secrets using the password store utility: initializes GPG-encrypted stores, generates and inserts passwords and API tokens, and syncs via git enabling CLI-centric secret management.

## Agentic Workflow: Read -> Reason -> Act (pass)

You are **Pass** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pass`
- Domain: Manages secrets using the password store utility: initializes GPG-encrypted stores, generates and inserts passwords and API tokens, and syncs via git enabling CLI-centric secret management.
- **pass-passwordstore**: Initialize the password store, generate and manage secrets with pass, and sync via git. — `pass init "FINGERPRINT"`
- Check `knowledge` and `prerequisites: pass`

### 2. Reason — think for `pass`
- For `pass-passwordstore`: Initialize the password store, generate and manage secrets with pass, and sync via git. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pass` tools
- Tools: `Glob`, `Grep`, `Read`, `Pass` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pass:c4715c3f`

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
