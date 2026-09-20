# Ksql

Stream processing with ksqlDB: create streams/tables from Kafka topics, run push/pull queries, and build materialized views with SQL.

## Instructions

# ksqlDB

Stream-process Kafka data with SQL.

## What this skill does

- Defines STREAMs and TABLEs over Kafka topics.
- Runs push queries (continuous) and pull queries (point lookups).
- Builds materialized aggregates with windowing.

## When to use

- Quick analytics on Kafka topics without writing Java/Go code.
- Materialized views: per-key state backed by Kafka.
- Prototyping stream pipelines before productionizing.

## Real commands

```bash
# Interactive shell in the CLI container
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

# Run a file of statements
ksql http://localhost:8088 --file statements.sql

# Declare a stream
ksql> CREATE STREAM ORDERS (ID BIGINT, AMOUNT DOUBLE, CURRENCY STRING) \
      WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='JSON', PARTITIONS=6);

# Materialized table of per-currency sums
ksql> CREATE TABLE HIGH_VALUE_ORDERS AS \
      SELECT ID, AMOUNT FROM ORDERS \
      WHERE AMOUNT > 1000 EMIT CHANGES;

# Push query over REST
curl -X POST http://localhost:8088/query \
  -H 'Content-Type: application/vnd.ksql.v1+json' \
  -d '{"ksql":"SELECT * FROM ORDERS EMIT CHANGES;"}'

# Tumbling-window aggregate
curl -X POST http://localhost:8088/query \
  -H 'Content-Type: application/vnd.ksql.v1+json' \
  -d '{"ksql":"SELECT CURRENCY, COUNT(*) FROM ORDERS WINDOW TUMBLING (SIZE 1 MINUTE) GROUP BY CURRENCY EMIT CHANGES;"}'

# Pull query (materialized table)
curl -X POST http://localhost:8088/query \
  -H 'Content-Type: application/vnd.ksql.v1+json' \
  -d '{"ksql":"SELECT * FROM HIGH_VALUE_ORDERS WHERE ID=42;"}'
```

## statements.sql example

```sql
CREATE STREAM ORDERS (ID BIGINT, AMOUNT DOUBLE, CURRENCY STRING)
  WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='JSON');

CREATE STREAM HIGH_VALUE AS
  SELECT ID, AMOUNT, CURRENCY
  FROM ORDERS
  WHERE AMOUNT > 1000
  EMIT CHANGES;
```

## Testing

```bash
# Feed an order and watch the push query
echo '{"ID":7,"AMOUNT":2500,"CURRENCY":"USD"}' | \
  kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
```

## Best practices

- Streams map 1:1 to topics; tables materialize keys with changelogs.
- Pull queries only work on materialized (TABLE) data.
- Prefer EMIT CHANGES for continuous output; specify limits for one-shot reads.

## Capabilities

### ksql-shell
Connect to the ksqlDB server and run SQL statements.

**Commands:**
- `docker exec -it ksqldb-cli ksql http://ksqldb-server:8088`
- `ksql http://localhost:8088 --file statements.sql`
- `ksql http://localhost:8088`
- `curl -X POST http://localhost:8088/ksql -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SHOW STREAMS;"}'`

**Examples:**
- docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
- ksql http://localhost:8088 --file statements.sql
- curl -X POST http://localhost:8088/ksql -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SHOW STREAMS;"}'

### sql-queries
Run push and pull queries against streams and tables.

**Commands:**
- `curl -X POST http://localhost:8088/query -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SELECT * FROM ORDERS EMIT CHANGES;"}'`
- `curl -X POST http://localhost:8088/query -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SELECT COUNT(*) FROM ORDERS WINDOW TUMBLING (SIZE 1 MINUTE) GROUP BY CURRENCY EMIT CHANGES;"}'`
- `curl -X POST http://localhost:8088/ksql -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SHOW TABLES;"}'`
- `curl -X POST http://localhost:8088/query -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SELECT * FROM HIGH_VALUE_ORDERS WHERE ID=42;"}'`

**Examples:**
- curl -X POST http://localhost:8088/query -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SELECT * FROM ORDERS EMIT CHANGES;"}'
- curl -X POST http://localhost:8088/ksql -H 'Content-Type: application/vnd.ksql.v1+json' -d '{"ksql":"SHOW TABLES;"}'