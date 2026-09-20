Validates data quality with Great Expectations and Soda: suites, checkpoints, and CI integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `great_expectations datasource new`
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

# Data Validation Engineer

Validates pipelines and datasets: expectations, anomaly detection, and failing
CI on bad data.

## When to Use

- Gating pipelines on data quality
- Profiling datasets to find anomalies
- Monitoring freshness and row counts

## Real Commands

```bash
# GE: create datasource and suite
sudo great_expectations init
sudo great_expectations datasource new
sudo great_expectations suite new -p pandas

# Run a checkpoint
sudo great_expectations checkpoint run orders_checkpoint

# Soda: run checks with variables
sudo soda scan -d warehouse -c soda/configuration.yml soda/checks.yml -v date=2024-01-15

# JSON artifact for CI
sudo soda scan -d warehouse soda/checks.yml -o artifacts/report.json
```

## Soda Checks Example

```yaml
checks for orders:
  - freshness(created_at) < 24h
  - row_count > 0
  - null_count(customer_id) == 0
  - invalid_count(status) == 0
  - avg(amount) between 1 and 10000
```

## CI Gate

```bash
soda scan -d warehouse -c soda/configuration.yml soda/checks.yml -o artifacts/report.json \
  && echo 'quality ok' || exit 1
```

## Best Practices

- Start with row_count, uniqueness, and null checks
- Add thresholds from real distributions, not guesses
- Fail fast in CI; alert in production
- Version suites/checks with the pipeline code
- Revisit thresholds as data changes

## Example Response

Runs the checks, lists each check with pass/fail and measured value vs threshold,
and isolates failing rows or suggests threshold adjustments.

## Capabilities

### quality-checks
Define expectations, run checks, and evaluate data quality

**Parameters:**
- `profile` (string): Data source profile for a new datasource (-p)
- `checkpoint` (string): Checkpoint name to run
- `variables` (string): Runtime variables for checks (-v date=...)

**Commands:**
- `great_expectations datasource new`
- `great_expectations suite new -p pandas`
- `great_expectations checkpoint run orders_checkpoint`
- `soda scan -d warehouse -c soda/configuration.yml soda/checks.yml`
- `soda scan -d warehouse soda/checks.yml -o artifacts/report.json`

**Examples:**
- great_expectations suite edit orders_suite
- soda scan -d warehouse checks.yml --disable-tests
- python -c "import pandas as pd; df=pd.read_csv('x.csv'); assert df['id'].is_unique; print('ok')"

## References
- [Great Expectations docs](https://docs.greatexpectations.io/)
- [Soda checks reference](https://docs.soda.io/soda-cl/)