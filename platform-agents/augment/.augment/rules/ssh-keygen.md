---
type: agent_requested
description: "Generates and manages SSH key pairs: ed25519/RSA creation, fingerprinting, passphrase changes, host key verification, and known_hosts. Use when working with key generation, host and fingerprints, devtools or when the user mentions key generation, host and fingerprints, devtools."
---

Generates and manages SSH key pairs: ed25519/RSA creation, fingerprinting, passphrase changes, host key verification, and known_hosts.

## Agentic Workflow: Read -> Reason -> Act (ssh-keygen)

You are **ssh-keygen** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `ssh-keygen`
- Domain: Generates and manages SSH key pairs: ed25519/RSA creation, fingerprinting, passphrase changes, host key verification, and known_hosts.
- **key-generation**: Generate strong key pairs and export public keys. — `ssh-keygen -t ed25519 -C "jane@localhost"`
- **host-and-fingerprints**: Verify host keys and manage known_hosts. — `ssh-keygen -l -f ~/.ssh/id_ed25519.pub`
- Check `knowledge` and `prerequisites: ssh-keygen, ssh-keyscan`

### 2. Reason — think for `ssh-keygen`
- For `key-generation`: Generate strong key pairs and export public keys. — decide which checks to run
- For `host-and-fingerprints`: Verify host keys and manage known_hosts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ssh-keygen` tools
- Tools: `Glob`, `Grep`, `Read`, `Ssh-keygen`, `Ssh-keyscan` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ssh-keygen:b5ad16bf`

# SSH Key Management

Create and manage SSH keys: generation, fingerprints, passphrases, known_hosts.

## What This Skill Does

- Generates ed25519/RSA key pairs
- Exports and fingerprints keys
- Changes passphrases and re-keys
- Manages known_hosts entries
- Verifies host keys before connecting

## When to Use

- Setting up SSH auth for a new machine
- Auditing key fingerprints
- Fixing host key mismatch errors

## Real Commands

```bash
# Generation
ssh-keygen -t ed25519 -C "jane@example.com"
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
ssh-keygen -t ed25519 -N '' -f /tmp/ci-key

# Public key and fingerprints
ssh-keygen -y -f ~/.ssh/id_ed25519
ssh-keygen -l -f ~/.ssh/id_ed25519.pub
ssh-keygen -l -E sha256 -f /etc/ssh/ssh_host_ed25519_key.pub

# Passphrase
ssh-keygen -p -f ~/.ssh/id_ed25519

# known_hosts
ssh-keygen -F github.com
ssh-keygen -R github.com
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts
```

## Best Practices

- Prefer ed25519; use RSA 4096 only for legacy servers
- Always set a comment (-C) identifying the key owner
- Verify fingerprints against official channels before trusting hosts
- Use ssh-keygen -R to purge stale host entries
- Never share private keys; public keys travel safely

## Capabilities

### key-generation
Generate strong key pairs and export public keys.

**Parameters:**
- `type` (string): Key type: ed25519, rsa, ecdsa
- `bits` (integer): Key bits for rsa (-b)
- `file` (string): Key file path (-f)
- `comment` (string): Key comment (-C)

**Commands:**
- `ssh-keygen -t ed25519 -C "jane@localhost"`
- `ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa`
- `ssh-keygen -y -f ~/.ssh/id_ed25519`
- `ssh-keygen -t ed25519 -N '' -f /tmp/testkey`
- `ssh-keygen -p -f ~/.ssh/id_ed25519`

**Examples:**
- ssh-keygen -t ed25519 -C "jane@localhost"
- ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
- ssh-keygen -p -f ~/.ssh/id_ed25519

### host-and-fingerprints
Verify host keys and manage known_hosts.

**Parameters:**
- `host` (string): Host name for known_hosts ops
- `file` (string): Public key file for fingerprinting

**Commands:**
- `ssh-keygen -l -f ~/.ssh/id_ed25519.pub`
- `ssh-keygen -l -E sha256 -f /etc/ssh/ssh_host_ed25519_key.pub`
- `ssh-keygen -F github.com`
- `ssh-keygen -R github.com`
- `ssh-keygen -H -F github.com`
- `ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts`

**Examples:**
- ssh-keygen -l -f ~/.ssh/id_ed25519.pub
- ssh-keygen -R github.com
- ssh-keyscan -t ed25519 github.com

## References
- [ssh-keygen Manual](https://man.openbsd.org/ssh-keygen)
- [GitHub SSH Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)