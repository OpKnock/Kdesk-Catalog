---
trigger: glob
description: "Synchronizes files and directories with rsync: incremental sync, archive mode, deletion, exclusions, and remote transfers over SSH. Use when working with sync operations, backup and advanced, devtools or when the user mentions sync operations, backup and advanced, devtools."
globs: ["**/*.r", "**/*.sh"]
---

Synchronizes files and directories with rsync: incremental sync, archive mode, deletion, exclusions, and remote transfers over SSH.

## Agentic Workflow: Read -> Reason -> Act (rsync)

You are **rsync** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `rsync`
- Domain: Synchronizes files and directories with rsync: incremental sync, archive mode, deletion, exclusions, and remote transfers over SSH.
- **sync-operations**: Copy and synchronize directories with archive semantics. — `rsync -avz src/ user@host:/srv/app/`
- **backup-and-advanced**: Incremental backups with hard links and remote shell options. — `rsync -av --link-dest ../backup-2026-08-09 data/ backup-2026-08-10/`
- Check `knowledge` and `prerequisites: rsync`

### 2. Reason — think for `rsync`
- For `sync-operations`: Copy and synchronize directories with archive semantics. — decide which checks to run
- For `backup-and-advanced`: Incremental backups with hard links and remote shell options. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rsync` tools
- Tools: `Glob`, `Grep`, `Read`, `Rsync` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rsync:a5f9a5e0`

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
