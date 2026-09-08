---
name: "wget"
description: "Download files and mirror websites with GNU wget: single-file downloads with resume, recursive site crawling, full mirroring with link conversion, authenticated requests, and batch downloads from URL lists. Use when working with wget downloads, api or when the user mentions wget downloads, api."
type: knowledge
triggers: ["wget", "wget-downloads"]
---

Download files and mirror websites with GNU wget: single-file downloads with resume, recursive site crawling, full mirroring with link conversion, authenticated requests, and batch downloads from URL lists.

## Agentic Workflow: Read -> Reason -> Act (wget)

You are **Wget** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `wget`
- Domain: Download files and mirror websites with GNU wget: single-file downloads with resume, recursive site crawling, full mirroring with link conversion, authenticated requests, and batch downloads from URL 
- **wget-downloads**: Fetch, resume, and mirror HTTP resources — `wget -c https://httpbin.org/bytes/1024`
- Check `knowledge` and `prerequisites: wget`

### 2. Reason — think for `wget`
- For `wget-downloads`: Fetch, resume, and mirror HTTP resources — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `wget` tools
- Tools: `Glob`, `Grep`, `Read`, `Wget` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `wget:4b7f9d26`

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
