---
name: "git-crypt"
description: "Transparently encrypts sensitive files in Git repositories with git-crypt, keyed by GPG users or symmetric keys. Use when working with repo setup, encryption lifecycle, security or when the user mentions repo setup, encryption lifecycle, security."
---

Transparently encrypts sensitive files in Git repositories with git-crypt, keyed by GPG users or symmetric keys.

## Agentic Workflow: Read -> Reason -> Act (git-crypt)

You are **git-crypt** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `git-crypt`
- Domain: Transparently encrypts sensitive files in Git repositories with git-crypt, keyed by GPG users or symmetric keys.
- **repo-setup**: Initialize encryption, define .gitattributes, and add collaborators. — `git-crypt init`
- **encryption-lifecycle**: Encrypt tracked files, lock/unlock working copies, and verify encryption state. — `git-crypt lock`
- Check `knowledge` and `prerequisites: git, git-crypt`

### 2. Reason — think for `git-crypt`
- For `repo-setup`: Initialize encryption, define .gitattributes, and add collaborators. — decide which checks to run
- For `encryption-lifecycle`: Encrypt tracked files, lock/unlock working copies, and verify encryption state. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `git-crypt` tools
- Tools: `Glob`, `Grep`, `Read`, `Git-crypt`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `git-crypt:595df5ac`

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
