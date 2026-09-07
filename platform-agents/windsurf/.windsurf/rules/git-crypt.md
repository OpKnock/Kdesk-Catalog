---
trigger: glob
description: "Transparently encrypts sensitive files in Git repositories with git-crypt, keyed by GPG users or symmetric keys. Use when working with repo setup, encryption lifecycle, security or when the user mentions repo setup, encryption lifecycle, security."
globs: ["**/*.r", "**/*.rs", "**/*.sh"]
---

Transparently encrypts sensitive files in Git repositories with git-crypt, keyed by GPG users or symmetric keys.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `git-crypt init`, `git-crypt lock`
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

# git-crypt

Transparent file encryption inside Git repositories.

## What This Skill Does

- Initializes a repository for git-crypt encryption
- Encrypts files matched by .gitattributes on commit
- Decrypts working copies on unlock for authorized collaborators
- Manages collaborator GPG keys and symmetric fallback keys

## When to Use

- Committing .env files, keys, or configs with secrets to a shared repo
- Enabling a team to clone and decrypt without extra tooling
- Replacing ad-hoc encryption of config files

## Real Commands

```bash
# Initialize and grant access
cd repo
git-crypt init
git-crypt add-gpg-user user@example.com

# Mark files for encryption
cat >> .gitattributes <<EOF
.env filter=git-crypt diff=git-crypt
*.key filter=git-crypt diff=git-crypt
EOF

# Verify what will be encrypted
git-crypt status

# Collaborate: unlock and lock
git-crypt unlock        # with your GPG key
git-crypt unlock /tmp/team.key   # with symmetric key
git-crypt lock

# Export a shared symmetric key for CI
# (NOT for teams with per-user GPG keys)
git-crypt export-key /tmp/team.key
```

## Best Practices

- Never commit the exported symmetric key to the repository
- Prefer per-user GPG keys; export a shared key only for CI bots
- Test by cloning fresh: encrypted files should read as ciphertext in a locked clone
- Rotate keys by exporting a new key and re-adding GPG users
- Keep .gitattributes explicit and review it on pull requests

## Capabilities

### repo-setup
Initialize encryption, define .gitattributes, and add collaborators.

**Parameters:**
- `user` (string): GPG email or key ID of the collaborator
- `keyFile` (string): Path to export the symmetric key

**Commands:**
- `git-crypt init`
- `git-crypt add-gpg-user user@localhost`
- `git-crypt add-gpg-user --trusted admin@localhost`
- `git-crypt status`
- `git-crypt export-key /tmp/team.key`

**Examples:**
- git-crypt init
- git-crypt add-gpg-user alice@localhost
- git-crypt status

### encryption-lifecycle
Encrypt tracked files, lock/unlock working copies, and verify encryption state.

**Parameters:**
- `keyFile` (string): Symmetric key file for unlocking without GPG
- `revision` (string): Git revision to inspect encryption state

**Commands:**
- `git-crypt lock`
- `git-crypt unlock`
- `git-crypt unlock /tmp/team.key`
- `git-crypt status -f .env`
- `git cat-file blob HEAD:.env | head -c 16`

**Examples:**
- git-crypt unlock
- git-crypt lock
- git-crypt status

## References
- [git-crypt GitHub](https://github.com/AGWA/git-crypt)
- [git-crypt README Guide](https://github.com/AGWA/git-crypt/blob/master/README.md)
