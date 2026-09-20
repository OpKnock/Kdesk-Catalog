---
applyTo: "**/*.css **/*.json **/*.r **/*.sh"
---

Download files and mirror websites with GNU wget: single-file downloads with resume, recursive site crawling, full mirroring with link conversion, authenticated requests, and batch downloads from URL lists.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `wget -c https://httpbin.org/bytes/1024`
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

# wget

## What this skill does
Download files and mirror websites with GNU wget: single-file downloads with resume, recursive site crawling, full mirroring with link conversion, authenticated requests, and batch downloads from URL lists.

## When to use
- Downloading large artifacts reliably
- Mirroring documentation for offline use
- Scripting downloads in CI

## Real commands
```bash
# Resume an interrupted download
wget -c https://httpbin.org/bytes/1024

# Recursive crawl (2 levels, no parent)
wget -r -l 2 -np https://httpbin.org/

# Full mirror with assets and converted links
wget --mirror -p --convert-links -P ./mirror https://httpbin.org/

# Batch download with bandwidth cap
wget -i urls.txt --limit-rate=1m -q

# Authenticated API export
wget --header='Authorization: Bearer token123' -O data.json https://httpbin.org/json

# Basic auth
wget --user=ci --password=secret https://httpbin.org/bytes/1024

# Retry-tolerant download
wget -c -t 10 --timeout=30 https://httpbin.org/bytes/1048576
```

## Common flags
- `-c` continue/resume
- `-r -l N -np` recursive, depth, no parent
- `-p` page requisites (css/js/img)
- `--convert-links` rewrite links for offline use
- `-P DIR` output directory
- `-q` quiet for scripts

## Best practices
- Use `-c` for large downloads
- Cap recursion depth before mirroring big sites
- Prefer `--header` over `--user` for token auth
- Never mirror sites that forbid it in robots.txt

## Testing
```bash
wget --spider -S https://httpbin.org/ 2>&1 | grep -E 'HTTP|Content-Length'
wget -q -O /dev/null -w '%{http_code}' https://httpbin.org/
```

## Capabilities

### wget-downloads
Fetch, resume, and mirror HTTP resources

**Parameters:**
- `recursive` (boolean): Follow links recursively (-r)
- `level` (integer): Maximum recursion depth (-l)
- `rate` (string): Bandwidth limit, e.g. 1m, 500k (--limit-rate)

**Commands:**
- `wget -c https://httpbin.org/bytes/1024`
- `wget -r -l 2 -np https://httpbin.org/`
- `wget --mirror -p --convert-links -P ./mirror https://httpbin.org/`
- `wget -i urls.txt --limit-rate=1m -q`
- `wget --header='Authorization: Bearer token123' -O data.json https://httpbin.org/json`

**Examples:**
- wget -c -t 10 --timeout=30 https://httpbin.org/bytes/1048576
- wget -r -A '*.pdf' -np -l 3 https://httpbin.org/
- wget --user=ci --password=secret https://httpbin.org/bytes/1024

## References
- [GNU Wget Manual](https://www.gnu.org/software/wget/manual/wget.html)
- [Wget WARC Guide](https://www.gnu.org/software/wget/manual/wget.html#WARC)
