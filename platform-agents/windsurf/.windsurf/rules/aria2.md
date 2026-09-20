---
trigger: glob
description: "Downloads files at high speed with aria2c: multi-connection, segmented downloads, batch URL lists, and BitTorrent/Metalink support. Use when working with fast downloads, torrent and metalink, devtools or when the user mentions fast downloads, torrent and metalink, devtools."
globs: ["**/*.r", "**/*.sh"]
---

Downloads files at high speed with aria2c: multi-connection, segmented downloads, batch URL lists, and BitTorrent/Metalink support.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aria2c -x 16 -s 16 http://localhost:8080/file.iso`, `aria2c --seed-time=0 ubuntu-24.04.iso.torrent`
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

# aria2 Downloads

Download large files fast with multi-connection aria2c.

## What This Skill Does

- Segments downloads across connections for higher throughput
- Resumes interrupted downloads (-c)
- Handles batch URL lists and Metalink/Torrent formats
- Limits bandwidth and summaries progress
- Verifies checksums with --check-integrity

## When to Use

- Large artifacts (ISOs, model weights, datasets)
- Flaky network downloads needing resume
- Batch mirror downloads from a URL list

## Real Commands

```bash
# Fast single download
aria2c -x 16 -s 16 https://example.com/file.iso
aria2c -d /downloads -o app.tar.gz https://example.com/app.tar.gz

# Resume and limits
aria2c -c https://example.com/big-file.zip
aria2c --max-download-limit=5M https://example.com/file.iso

# Batch
aria2c -i urls.txt
aria2c -Z https://a.com/1.zip https://b.com/2.zip

# Torrent / Metalink
aria2c --seed-time=0 ubuntu-24.04.iso.torrent
aria2c --check-integrity --metalink-file=files.meta4
```

## Best Practices

- Use -x 16 -s 16 for HTTP(S) CDNs that allow range requests
- Always -c for large downloads to survive disconnects
- Use --seed-time=0 for torrents when you only want the file
- Add --file-allocation=none on flash storage
- Use -i urls.txt with one URL per line for batch mirrors

## Capabilities

### fast-downloads
Download files with multiple connections and segments.

**Parameters:**
- `url` (string): File URL
- `connections` (integer): Connections per server (-x)
- `out` (string): Output file name
- `dir` (string): Download directory

**Commands:**
- `aria2c -x 16 -s 16 http://localhost:8080/file.iso`
- `aria2c -d /downloads -o app.tar.gz http://localhost:8080/app.tar.gz`
- `aria2c -c http://localhost:8080/big-file.zip`
- `aria2c --max-download-limit=5M http://localhost:8080/file.iso`
- `aria2c -Z https://a.com/1.zip https://b.com/2.zip`
- `aria2c -i urls.txt`

**Examples:**
- aria2c -x 16 -s 16 http://localhost:8080/file.iso
- aria2c -c http://localhost:8080/big-file.zip
- aria2c -i urls.txt

### torrent-and-metalink
Download BitTorrent and Metalink files with checksums.

**Parameters:**
- `torrent` (string): Torrent file path
- `seed-time` (integer): Seed time in minutes (0 = no seeding)

**Commands:**
- `aria2c --seed-time=0 ubuntu-24.04.iso.torrent`
- `aria2c --check-integrity --metalink-file=files.meta4`
- `aria2c --torrent-file=file.torrent -d /data`
- `aria2c --bt-max-peers=200 file.torrent`
- `aria2c --summary-interval=10 http://localhost:8080/file.bin`

**Examples:**
- aria2c --seed-time=0 ubuntu-24.04.iso.torrent
- aria2c --check-integrity --metalink-file=files.meta4
- aria2c --bt-max-peers=200 file.torrent

## References
- [aria2c Manual](https://aria2.github.io/manual/en/html/aria2c.html)
- [aria2 GitHub](https://github.com/aria2/aria2)
