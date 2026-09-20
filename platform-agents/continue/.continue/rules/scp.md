---
name: "scp"
description: "Copies files to and from remote hosts with scp: recursive dirs, custom ports/keys, and multiple source files. Use when working with file transfer, devtools or when the user mentions file transfer, devtools."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Copies files to and from remote hosts with scp: recursive dirs, custom ports/keys, and multiple source files.

## Agentic Workflow: Read -> Reason -> Act (scp)

You are **scp** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `scp`
- Domain: Copies files to and from remote hosts with scp: recursive dirs, custom ports/keys, and multiple source files.
- **file-transfer**: Copy files and directories between local and remote hosts. — `scp file.txt user@host:/home/user/`
- Check `knowledge` and `prerequisites: scp`

### 2. Reason — think for `scp`
- For `file-transfer`: Copy files and directories between local and remote hosts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `scp` tools
- Tools: `Glob`, `Grep`, `Read`, `Scp` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `scp:9e5ceca0`

# scp File Transfer

Copy files securely to and from remote machines.

## What This Skill Does

- Copies single files and whole directories (-r)
- Supports custom ports, keys, and multiple sources
- Preserves permissions with -p
- Compresses on slow links with -C
- Fetches remote files to local paths

## When to Use

- Quick file transfers without full rsync
- Pulling logs/configs from servers
- Pushing artifacts to hosts

## Real Commands

```bash
# Basic
scp file.txt user@host:/home/user/
scp user@host:/var/log/app.log ./app.log

# Directories
scp -r project/ user@host:/srv/
scp -r user@host:/etc/nginx/ ./nginx-backup/

# Options
scp -P 2222 file.txt user@host:/tmp/
scp -i ~/.ssh/id_ed25519 file.txt user@host:/tmp/
scp -p file.txt user@host:/home/user/    # preserve mtime/perms
scp -C bigfile.tar user@host:/tmp/       # compress

# Multiple sources
scp file1.txt file2.txt dir/ user@host:/tmp/
```

## Best Practices

- Use -P for the remote SSH port (lowercase -p means preserve)
- Prefer rsync for directories with many files (resume support)
- Verify remote paths are absolute to avoid surprises
- Use -C for large text files over slow links
- Batch with scp -r and a single host for scriptable deploys

## Capabilities

### file-transfer
Copy files and directories between local and remote hosts.

**Parameters:**
- `src` (string): Source path (local or user@host:path)
- `dest` (string): Destination path
- `port` (integer): SSH port (-P)
- `key` (string): Identity file (-i)

**Commands:**
- `scp file.txt user@host:/home/user/`
- `scp -r project/ user@host:/srv/`
- `scp user@host:/var/log/app.log ./app.log`
- `scp file1.txt file2.txt user@host:/tmp/`
- `scp -P 2222 file.txt user@host:/tmp/`
- `scp -i ~/.ssh/id_ed25519 file.txt user@host:/tmp/`

**Examples:**
- scp file.txt user@host:/home/user/
- scp -r project/ user@host:/srv/
- scp -i ~/.ssh/id_ed25519 file.txt user@host:/tmp/

## References
- [scp Manual (OpenBSD)](https://man.openbsd.org/scp)
- [scp Linux Manual](https://man7.org/linux/man-pages/man1/scp.1.html)