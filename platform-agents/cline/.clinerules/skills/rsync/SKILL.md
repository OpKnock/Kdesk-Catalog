---
name: "rsync"
description: "Synchronizes files and directories with rsync: incremental sync, archive mode, deletion, exclusions, and remote transfers over SSH. Use when working with sync operations, backup and advanced, devtools or when the user mentions sync operations, backup and advanced, devtools."
license: "MIT"
compatibility: "Requires rsync."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devtools"}
allowed-tools: "Glob Grep Read Bash(rsync:*)"
---

Synchronizes files and directories with rsync: incremental sync, archive mode, deletion, exclusions, and remote transfers over SSH.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rsync -avz src/ user@host:/srv/app/`, `rsync -av --link-dest ../backup-2026-08-09 data/ backup-2026`
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

# rsync Synchronization

Copy and sync files efficiently — local or remote, incremental.

## What This Skill Does

- Syncs directories with archive mode (perms, times, links)
- Removes extraneous files with --delete
- Excludes patterns (node_modules, .git)
- Creates hard-link incremental backups
- Transfers over custom SSH ports/keys
- Dry-runs to preview changes

## When to Use

- Deploying code to servers
- Backing up data with dedup (link-dest)
- Mirroring directories across machines

## Real Commands

```bash
# Basic sync
rsync -avz src/ user@host:/srv/app/
rsync -av src/ dest/

# Mirror (delete extras) with dry run
rsync -n -av --delete src/ dest/
rsync -av --delete src/ dest/

# Exclusions
rsync -av --exclude 'node_modules' --exclude '.git' src/ dest/

# Remote with custom SSH
rsync -az -e 'ssh -p 2222 -i key.pem' src/ user@host:/dest/

# Incremental backups
rsync -av --link-dest ../backup-2026-08-09 data/ backup-2026-08-10/

# Limits and progress
rsync --partial --progress -avz bigfile.iso user@host:/tmp/
rsync -av --bwlimit=2000 bigdir/ user@host:/backup/
```

## Best Practices

- Always dry-run (-n) before --delete on production
- Trailing slash matters: src/ copies contents, src copies the dir
- Use --link-dest for space-efficient daily backups
- Compress (-z) only for slow links
- Pair with --checksum when timestamps lie (e.g. build artifacts)

## Capabilities

### sync-operations
Copy and synchronize directories with archive semantics.

**Parameters:**
- `src` (string): Source path
- `dest` (string): Destination path
- `exclude` (string): Pattern to exclude

**Commands:**
- `rsync -avz src/ user@host:/srv/app/`
- `rsync -av --delete src/ dest/`
- `rsync -n -av --delete src/ dest/`
- `rsync -av --exclude 'node_modules' --exclude '.git' src/ dest/`
- `rsync --partial --progress -avz bigfile.iso user@host:/tmp/`

**Examples:**
- rsync -avz src/ user@host:/srv/app/
- rsync -n -av --delete src/ dest/
- rsync -av --exclude 'node_modules' src/ dest/

### backup-and-advanced
Incremental backups with hard links and remote shell options.

**Parameters:**
- `link-dest` (string): Previous backup dir for hard-link dedup
- `bwlimit` (integer): Bandwidth limit in KB/s

**Commands:**
- `rsync -av --link-dest ../backup-2026-08-09 data/ backup-2026-08-10/`
- `rsync -az -e 'ssh -p 2222 -i key.pem' src/ user@host:/dest/`
- `rsync -av --bwlimit=2000 bigdir/ user@host:/backup/`
- `rsync -avz --delete-after src/ dest/`
- `rsync -ai source/ dest/`

**Examples:**
- rsync -av --link-dest ../backup-2026-08-09 data/ backup-2026-08-10/
- rsync -az -e 'ssh -p 2222 -i key.pem' src/ user@host:/dest/
- rsync -av --bwlimit=2000 bigdir/ user@host:/backup/

## References
- [rsync Manual](https://man7.org/linux/man-pages/man1/rsync.1.html)
- [rsync Archive](https://rsync.samba.org/documentation.html)
