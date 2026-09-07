In-process analytical SQL with DuckDB: querying CSV/Parquet directly, extensions, and CLI use.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `duckdb mydb.duckdb`
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