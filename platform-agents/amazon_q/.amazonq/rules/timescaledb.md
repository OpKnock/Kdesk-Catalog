# Timescaledb

Time-series data with TimescaleDB: hypertables, continuous aggregates, retention policies, and time_bucket queries.

## Instructions

# TimescaleDB

Time-series PostgreSQL: hypertables auto-partition by time, with continuous
aggregates and retention policies.

## When to Use

- Metrics, IoT, and event data at high write rates
- Rollups over long time ranges
- Data retention management

## Real Commands

```bash
# Enable the extension
psql -d app -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# Create a hypertable
psql -d app -c "SELECT create_hypertable('conditions', 'time', chunk_time_interval => INTERVAL '1 day');"

# Time-bucketed query
psql -d app -c "SELECT time_bucket('15 minutes', time) AS bucket, avg(temp) FROM conditions GROUP BY bucket ORDER BY bucket DESC LIMIT 10;"

# Continuous aggregate
psql -d app -c "SELECT create_continuous_aggregate('avg_temp_hour', 'SELECT time_bucket(""1 hour"", time) t, avg(temp) FROM conditions GROUP BY t');"

# Retention
psql -d app -c "SELECT add_retention_policy('conditions', INTERVAL '30 days');"

# Drop old chunks immediately
psql -d app -c "SELECT drop_chunks('conditions', older_than => INTERVAL '90 days');"

# Inspect
psql -d app -c "SELECT * FROM timescaledb_information.hypertables;"
```

## Best Practices

- Choose chunk_time_interval so chunks are 1-7 days of data
- Add indexes on (time, tag) columns
- Use continuous aggregates for hourly/daily rollups, not raw queries
- Set retention policies before data explodes
- Backfill with `time_bucket` queries on hypertables

## Example Response

Creates the hypertable, verifies chunk distribution, and sets up the aggregate
plus retention policy; reports expected storage savings.

## Capabilities

### timescaledb
Create hypertables, aggregates, and retention policies with psql

**Commands:**
- `psql -d app -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"`
- `psql -d app -c "SELECT create_hypertable('conditions', 'time', chunk_time_interval => INTERVAL '1 day');"`
- `psql -d app -c "SELECT time_bucket('15 minutes', time) AS bucket, avg(temp) FROM conditions GROUP BY bucket ORDER BY bucket DESC LIMIT 10;"`
- `psql -d app -c "SELECT add_retention_policy('conditions', INTERVAL '30 days');"`
- `psql -d app -c "SELECT * FROM timescaledb_information.hypertables;"`

**Examples:**
- psql -d app -c "SELECT create_continuous_aggregate('avg_temp', 'SELECT time_bucket(""1 hour"", time) t, avg(temp) FROM conditions GROUP BY t');"
- psql -d app -c "SELECT drop_chunks('conditions', older_than => INTERVAL '90 days');"
- psql -d app -c "SELECT chunks FROM chunk_relation_size_pretty('conditions');"