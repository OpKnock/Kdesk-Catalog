---
name: "sftp"
description: "Interacts with remote filesystems over SFTP: interactive sessions, batch mode, uploads/downloads, and permission management. Use when working with interactive session, batch and management, devtools or when the user mentions interactive session, batch and management, devtools."
license: "MIT"
compatibility: "Requires bye, get, ls,, mkdir, put, sftp."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devtools"}
allowed-tools: "Glob Grep Read Bash(bye:*) Bash(get:*) Bash(ls,:*) Bash(mkdir:*) Bash(put:*) Bash(rm:*) Bash(sftp:*)"
---

Interacts with remote filesystems over SFTP: interactive sessions, batch mode, uploads/downloads, and permission management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `sftp user@host`, `sftp -b batch.txt user@host`
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

# SFTP Operations

Work with remote files over secure FTP.

## What This Skill Does

- Starts interactive SFTP sessions with custom ports/keys
- Uploads (put) and downloads (get) files and trees
- Navigates remote and local dirs (cd, lcd, ls, lls)
- Manages remote files: mkdir, rm, chmod, rename
- Runs scripted batch transfers non-interactively

## When to Use

- Interactive remote file management
- Scripted nightly uploads/downloads
- When rsync is unavailable on the remote

## Real Commands

```bash
# Session
sftp user@host
sftp -oPort=2222 user@host
sftp -i ~/.ssh/id_ed25519 user@host

# Interactive commands (inside sftp)
ls, pwd
lcd ./downloads, lls
get file.txt
get -r /srv/logs/ ./logs/
put report.pdf /tmp/
put -P report.pdf /tmp/          # preserve times
mkdir /backups/new
chmod 700 /backups
rm /tmp/old.log
bye

# Batch mode
sftp -b batch.txt user@host
sftp -b - user@host <<< $'put f.txt
bye'
sftp user@host <<< $'mget /data/*.csv'
```

## batch.txt Example

```
lcd ./out
put build.tar.gz /srv/app/
chmod 644 /srv/app/build.tar.gz
bye
```

## Best Practices

- Use -P flag on put to preserve modification times
- Test batch files with a dry list-only first
- Use get -r for recursive pulls
- Prefer rsync when you need delta sync or delete mirroring
- Always end batch files with bye to close cleanly

## Capabilities

### interactive-session
Navigate remote directories, upload, and download files interactively.

**Parameters:**
- `host` (string): Remote host
- `port` (integer): SSH port

**Commands:**
- `sftp user@host`
- `sftp -oPort=2222 user@host`
- `sftp -i ~/.ssh/id_ed25519 user@host`
- `ls, cd, pwd, lcd, lls`
- `get -r /srv/logs/ ./logs/`
- `put -P report.pdf /tmp/`

**Examples:**
- sftp user@host
- get -r /srv/logs/ ./logs/
- put -P report.pdf /tmp/

### batch-and-management
Run scripted transfers and manage remote files.

**Parameters:**
- `batch-file` (string): File with sftp commands
- `remote-path` (string): Remote path for operations

**Commands:**
- `sftp -b batch.txt user@host`
- `sftp -b - user@host <<< $'put f.txt\nbye'`
- `sftp user@host <<< $'mget /data/*.csv'`
- `mkdir /backups/new && chmod 700 /backups`
- `rm /tmp/old.log`
- `bye`

**Examples:**
- sftp -b batch.txt user@host
- sftp user@host <<< $'mget /data/*.csv'
- mkdir /backups/new

## References
- [sftp Manual (OpenBSD)](https://man.openbsd.org/sftp)
- [sftp Linux Manual](https://man7.org/linux/man-pages/man1/sftp.1.html)
