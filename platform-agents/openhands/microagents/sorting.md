---
name: "sorting"
description: "Sorts data correctly on the command line and in code. Handles CSV columns with numeric awareness, human-readable sizes (4.2K vs 1.3G), JSON arrays with jq sort_by, and SQL results with ORDER BY for API response ordering. Use when working with sort data, api or when the user mentions sort data, api."
type: knowledge
triggers: ["sorting", "sort-data"]
---

Sorts data correctly on the command line and in code. Handles CSV columns with numeric awareness, human-readable sizes (4.2K vs 1.3G), JSON arrays with jq sort_by, and SQL results with ORDER BY for API response ordering.

## Agentic Workflow: Read -> Reason -> Act (sorting)

You are **Sorting** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `sorting`
- Domain: Sorts data correctly on the command line and in code. Handles CSV columns with numeric awareness, human-readable sizes (4.2K vs 1.3G), JSON arrays with jq sort_by, and SQL results with ORDER BY for AP
- **sort-data**: Sorts data correctly on the command line and in code. Handles CSV columns with numeric awareness, hu — `sort -k2 -n data.csv`
- Check `knowledge` and `prerequisites: python, sort, sqlite3`

### 2. Reason — think for `sorting`
- For `sort-data`: Sorts data correctly on the command line and in code. Handles CSV columns with numeric awareness, human-readable sizes ( — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sorting` tools
- Tools: `Glob`, `Grep`, `Read`, `Sort`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sorting:56385c58`

# Sorting

Hand-crafted skill for sorting data correctly on the CLI and in code.

## What this skill does

- Sorts CSV and text by column with numeric awareness
- Sorts human-readable sizes like 4.2K and 1.3G
- Sorts JSON arrays and SQL results for API work

## When to use

- Ordering report data before pasting into a table
- Checking the largest files or slowest endpoints
- Deciding the sort order an API should return

## Real commands

```bash
# CSV by column 2 numerically
sort -t, -k2 -n sales.csv

# Human sizes
du -sh * | sort -h | tail -5

# JSON by price, then reversed
jq 'sort_by(.price)' products.json
jq 'sort_by(.price) | reverse' products.json

# Python
python -c 'data = [3,1,2]; print(sorted(data, key=lambda x: -x))'

# SQL
sqlite3 app.db "SELECT name FROM users ORDER BY created_at DESC LIMIT 10;"
```

## Comparing strings vs numbers

- sort -n for numeric, plain sort for lexicographic (10 < 2!)
- sort -h understands 2K < 1M
- jq sort_by compares numbers correctly when they are numbers

## Testing

```bash
printf 'b,2
a,10
c,1
' | sort -t, -k2 -n   # c,1 b,2 a,10
printf 'b,2
a,10
c,1
' | sort              # a,10 b,2 c,1
```

## Best practices

- Always state -n or -h: lexicographic ordering of numbers misleads
- For APIs, sort server-side; clients should never re-sort big pages
- Add secondary keys: sort -k1,1 -k2,2n for stable results

## Capabilities

### sort-data
Sorts data correctly on the command line and in code. Handles CSV columns with numeric awareness, human-readable sizes (4.2K vs 1.3G), JSON arrays with jq sort_by, and SQL results with ORDER BY for API response ordering.

**Parameters:**
- `column` (integer): Column number to sort by (1-indexed)
- `numeric` (boolean): Enable numeric sort
- `json_field` (string): JSON field name to sort by
- `sql_column` (string): SQL column name for ORDER BY

**Commands:**
- `sort -k2 -n data.csv`
- `sort -h sizes.txt`
- `jq 'sort_by(.timestamp)' events.json`
- `sqlite3 db.sqlite "SELECT * FROM events ORDER BY timestamp DESC"`

**Examples:**
- sort -k2 -n data.csv
- sort -h sizes.txt
- jq 'sort_by(.timestamp)' events.json
- sqlite3 db.sqlite "SELECT * FROM events ORDER BY timestamp DESC"

## References
- [GNU sort manual](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html)
