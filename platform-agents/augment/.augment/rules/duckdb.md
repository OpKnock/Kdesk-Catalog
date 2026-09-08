---
type: agent_requested
description: "In-process analytical SQL with DuckDB: querying CSV/Parquet directly, extensions, and CLI use. Use when working with duckdb cli, database or when the user mentions duckdb cli, database."
---

In-process analytical SQL with DuckDB: querying CSV/Parquet directly, extensions, and CLI use.

## Agentic Workflow: Read -> Reason -> Act (duckdb)

You are **Duckdb** (database/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — database context for `duckdb`
- Domain: In-process analytical SQL with DuckDB: querying CSV/Parquet directly, extensions, and CLI use.
- **duckdb-cli**: Query files and databases with DuckDB's CLI and in-process SQL — `duckdb mydb.duckdb`
- Check `knowledge` and `prerequisites: duckdb`

### 2. Reason — think for `duckdb`
- For `duckdb-cli`: Query files and databases with DuckDB's CLI and in-process SQL — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `duckdb` tools
- Tools: `Glob`, `Grep`, `Read`, `Duckdb` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `duckdb:630da82d`

# DuckDB

Analytical SQL engine that runs in-process: query CSV/Parquet/JSON files directly
with no server.

## When to Use

- Ad-hoc analysis of local or remote files
- Lightweight warehouse-style queries in scripts
- Converting between formats (CSV -> Parquet)

## Real Commands

```bash
# One-shot query
sudo duckdb -c "SELECT count(*) FROM read_csv_auto('data.csv')"

# Interactive shell
sudo duckdb mydb.duckdb

# Parquet globs
sudo duckdb -c "SELECT year, sum(amount) FROM read_parquet('s3://bucket/orders/*.parquet') GROUP BY 1 ORDER BY 1 DESC LIMIT 5"

# Extensions for remote/JSON data
sudo duckdb -c "INSTALL httpfs; LOAD httpfs;"
sudo duckdb -c "INSTALL json; LOAD json;"

# JSON output
sudo duckdb -json -c "SELECT order_id, amount FROM 'orders.parquet' LIMIT 3"

# Convert CSV to Parquet
sudo duckdb -c "COPY (SELECT * FROM read_csv_auto('data.csv')) TO 'data.parquet' (FORMAT PARQUET)"
```

## Python Usage

```python
import duckdb
con = duckdb.connect()
con.sql("SELECT * FROM read_csv_auto('data.csv')").df()
```

## Best Practices

- Prefer Parquet over CSV for repeated queries
- Install extensions per database (httpfs, json, spatial)
- Use glob patterns instead of loading file lists
- For ad-hoc: use :memory: database; persist only for reuse

## Example Response

Answers the analytical question with the query run and results, and can convert
the source data into Parquet for faster future queries.

## Capabilities

### duckdb-cli
Query files and databases with DuckDB's CLI and in-process SQL

**Parameters:**
- `command` (string): SQL to execute in one-shot mode (-c)
- `json` (boolean): Output results as JSON
- `readonly` (boolean): Open the database read-only

**Commands:**
- `duckdb mydb.duckdb`
- `duckdb -c "SELECT count(*) FROM read_csv_auto('data.csv')"`
- `duckdb -c "SELECT * FROM read_parquet('s3://bucket/part-*.parquet')"`
- `duckdb -c "INSTALL httpfs; LOAD httpfs;"`
- `duckdb -json -c "SELECT 1 AS a"`

**Examples:**
- duckdb -c "SELECT * FROM 'orders.csv' WHERE amount > 100 LIMIT 5"
- python -c "import duckdb; print(duckdb.sql('SELECT 42').fetchall())"
- duckdb -c "ATTACH 's3://bucket/db.duckdb' AS remote; SHOW ALL TABLES"

## References
- [DuckDB docs](https://duckdb.org/docs/)
- [DuckDB data ingestion](https://duckdb.org/docs/data/overview)