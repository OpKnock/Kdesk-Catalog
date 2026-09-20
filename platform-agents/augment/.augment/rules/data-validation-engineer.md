---
type: agent_requested
description: "Validates data quality with Great Expectations and Soda: suites, checkpoints, and CI integration."
---

# data-validation-engineer

Validates data quality with Great Expectations and Soda: suites, checkpoints, and CI integration.

## Instructions

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