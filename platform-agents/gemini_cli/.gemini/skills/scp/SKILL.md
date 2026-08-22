---
name: "scp"
description: "Copies files to and from remote hosts with scp: recursive dirs, custom ports/keys, and multiple source files."
---

# scp

Copies files to and from remote hosts with scp: recursive dirs, custom ports/keys, and multiple source files.

## Instructions

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
