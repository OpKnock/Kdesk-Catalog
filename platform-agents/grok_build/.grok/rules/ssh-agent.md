Manages SSH keys in the agent: add/remove keys, list fingerprints, lifetimes, and agent forwarding for multi-hop connections.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `eval "$(ssh-agent -s)"`, `ssh-add -t 1h ~/.ssh/id_ed25519`
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

# SSH Agent Management

Hold SSH keys in memory so you authenticate without passphrases on every use.

## What This Skill Does

- Starts the agent and loads private keys
- Lists loaded keys and fingerprints
- Removes keys (individual or all)
- Sets lifetimes and confirmation prompts
- Enables agent forwarding for jump hosts

## When to Use

- Passphrase-protected keys without re-entry
- Multiple keys needing selection per host
- Jump-host chains (bastion -> target)

## Real Commands

```bash
# Start and add
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add ~/.ssh/id_rsa

# Inspect
ssh-add -l                    # fingerprints
ssh-add -L                    # public keys
ssh-add -E sha256 -l          # sha256 fingerprints

# Remove
ssh-add -d ~/.ssh/id_ed25519
ssh-add -D                    # all keys
ssh-agent -k                  # kill agent

# Security options
ssh-add -t 1h ~/.ssh/id_ed25519
ssh-add -c ~/.ssh/id_ed25519  # confirm each use
ssh-add -x                    # lock agent
ssh-add -X                    # unlock

# Forwarding
ssh -A user@jumphost
```

## Best Practices

- Use ed25519 keys with short lifetimes in the agent
- Set -t lifetimes on shared machines
- Use -A only on trusted jump hosts (forwarding leaks key use)
- Add `AddKeysToAgent yes` in ~/.ssh/config for convenience
- Lock the agent (-x) when stepping away from shared sessions

## Capabilities

### agent-lifecycle
Start the agent and manage loaded keys.

**Parameters:**
- `keyfile` (string): Private key path
- `agent-sock` (string): Agent socket path (SSH_AUTH_SOCK)

**Commands:**
- `eval "$(ssh-agent -s)"`
- `ssh-add ~/.ssh/id_ed25519`
- `ssh-add -l`
- `ssh-add -L`
- `ssh-add -D`
- `ssh-agent -k`

**Examples:**
- eval "$(ssh-agent -s)"
- ssh-add ~/.ssh/id_ed25519
- ssh-add -l

### key-security
Set lifetimes, require confirmation, and inspect agent state.

**Parameters:**
- `lifetime` (integer): Key lifetime in seconds (-t)
- `confirm` (boolean): Require confirmation before use (-c)

**Commands:**
- `ssh-add -t 1h ~/.ssh/id_ed25519`
- `ssh-add -c ~/.ssh/id_ed25519`
- `ssh-add -t 3600`
- `ssh-add -x && ssh-add -X`
- `ssh -A user@jumphost`
- `ssh-add -E sha256 -l`

**Examples:**
- ssh-add -t 1h ~/.ssh/id_ed25519
- ssh-add -c ~/.ssh/id_ed25519
- ssh-add -E sha256 -l

## References
- [ssh-agent Manual](https://man.openbsd.org/ssh-agent)
- [ssh-add Manual](https://man.openbsd.org/ssh-add)