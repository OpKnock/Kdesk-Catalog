---
trigger: glob
description: "Downloads web resources with wget: recursive site mirroring, resuming, URL lists, rate limiting, and authentication. Use when working with download operations, mirroring and auth, devtools or when the user mentions download operations, mirroring and auth, devtools."
globs: ["**/*.r", "**/*.sh"]
---

Downloads web resources with wget: recursive site mirroring, resuming, URL lists, rate limiting, and authentication.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `wget http://localhost:8080/file.zip`, `wget -r -l 2 -np http://localhost:8080/docs/`
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

# wget Downloads

Fetch files and mirror websites from the command line.

## What This Skill Does

- Downloads files with custom names and directories
- Resumes interrupted transfers
- Recursively mirrors sites and doc trees
- Filters by extension and limits rate
- Authenticates and handles redirects

## When to Use

- Scriptable downloads in CI/cron
- Site mirrors for offline documentation
- Batch URL list downloads

## Real Commands

```bash
# Basic downloads
wget https://example.com/file.zip
wget -O app.tar.gz https://example.com/app.tar.gz
wget -P /downloads https://example.com/file.zip
wget -c https://example.com/big.iso
wget -q --show-progress https://example.com/file.zip

# Batch and limits
wget -i urls.txt
wget --limit-rate=2M https://example.com/big.iso

# Mirrors
wget -r -l 2 -np https://example.com/docs/
wget --mirror -p --convert-links -P ./site https://example.com
wget -r -A pdf,epub https://example.com/books/

# Auth
wget --user=jane --password=s3cr3t https://example.com/private/file.zip
wget --no-check-certificate https://selfsigned.local/file.zip
```

## Best Practices

- Use -c for resume on large downloads
- Scope mirrors with -l depth and -np (no parent)
- Use -A/-R to control mirrored content
- Prefer --show-progress for readable logs in scripts
- Never put credentials in URLs; use --user/--password flags

## Capabilities

### download-operations
Download files with output control and resume.

**Parameters:**
- `url` (string): Download URL
- `output` (string): Output file name
- `dir` (string): Output directory

**Commands:**
- `wget http://localhost:8080/file.zip`
- `wget -O app.tar.gz http://localhost:8080/app.tar.gz`
- `wget -c http://localhost:8080/big.iso`
- `wget -P /downloads http://localhost:8080/file.zip`
- `wget -i urls.txt`
- `wget --limit-rate=2M http://localhost:8080/big.iso`

**Examples:**
- wget -c http://localhost:8080/big.iso
- wget -i urls.txt
- wget -O app.tar.gz http://localhost:8080/app.tar.gz

### mirroring-and-auth
Mirror sites recursively and authenticate downloads.

**Parameters:**
- `level` (integer): Recursion depth (-l)
- `accept` (string): Accepted extensions (-A)
- `reject` (string): Rejected extensions (-R)

**Commands:**
- `wget -r -l 2 -np http://localhost:8080/docs/`
- `wget --mirror -p --convert-links -P ./site http://localhost:8080`
- `wget -r -A pdf,epub http://localhost:8080/books/`
- `wget --user=jane --password=s3cr3t http://localhost:8080/private/file.zip`
- `wget -q --show-progress http://localhost:8080/file.zip`
- `wget --no-check-certificate https://selfsigned.local/file.zip`

**Examples:**
- wget -r -l 2 -np http://localhost:8080/docs/
- wget --mirror -p --convert-links -P ./site http://localhost:8080
- wget -r -A pdf,epub http://localhost:8080/books/

## References
- [GNU wget Manual](https://www.gnu.org/software/wget/manual/wget.html)
- [wget Linux Manual](https://man7.org/linux/man-pages/man1/wget.1.html)
