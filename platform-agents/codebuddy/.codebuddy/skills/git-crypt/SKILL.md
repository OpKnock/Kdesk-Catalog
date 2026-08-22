---
name: "git-crypt"
description: "Transparently encrypts sensitive files in Git repositories with git-crypt, keyed by GPG users or symmetric keys."
---

# git-crypt

Transparently encrypts sensitive files in Git repositories with git-crypt, keyed by GPG users or symmetric keys.

## Instructions

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
