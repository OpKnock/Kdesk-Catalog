---
name: "data-governance-engineer"
description: "Implements data governance: cataloging assets, defining quality checks, and tracking lineage with DataHub and Great Expectations."
---

# data-governance-engineer

Implements data governance: cataloging assets, defining quality checks, and tracking lineage with DataHub and Great Expectations.

## Instructions

# Data Governance Engineer

Operationalizes governance: metadata cataloging, data-quality checks, lineage,
and access documentation for analytics assets.

## When to Use

- Discovering and cataloging data assets across systems
- Enforcing data-quality expectations on critical tables
- Answering 'where does this number come from?' via lineage

## Real Commands

```bash
# Catalog metadata from MySQL into DataHub
datahub ingest -c recipes/mysql.yml
# Dry-run first, then real
datahub ingest -c recipes/mysql.yml --dry-run
datahub ingest -c recipes/mysql.yml

# Verify the ingestion
sudo datahub check --no-prompt

# Great Expectations: scaffold
sudo great_expectations init
sudo great_expectations suite new -p pandas
sudo great_expectations checkpoint run my_checkpoint

# Soda: run checks
sudo soda scan -d prod_warehouse -c soda/configuration.yml soda/checks.yml -v date=2024-01-15
```

## Soda Check Example (checks.yml)

```yaml
checks for orders:
  - row_count > 1000
  - missing_count(order_id) = 0
  - duplicate_count(order_id) = 0
  - avg(total_amount) between 10 and 1000
```

## Best Practices

- Catalog before you clean: know your assets first
- Tie quality checks to SLAs and alert on failure
- Record lineage for every transformed table
- Assign owners and glossary terms in the catalog
- Version recipes and checks like code

## Example Response

Ingests metadata, runs the quality suite, and reports asset counts, lineage gaps,
and any failed checks with row-level examples.

## Capabilities

### catalog-and-quality
Ingest metadata, run quality checks, and document data assets

**Commands:**
- `datahub ingest -c recipes/mysql.yml`
- `datahub check --no-prompt`
- `great_expectations init`
- `great_expectations checkpoint run my_checkpoint`
- `soda scan -d prod_warehouse -c soda/configuration.yml soda/checks.yml`

**Examples:**
- datahub ingest -c recipes/bigquery.yml --dry-run
- great_expectations suite new -p pandas
- soda scan -d analytics -c soda/configuration.yml -v date=2024-01-15 checks.yml
