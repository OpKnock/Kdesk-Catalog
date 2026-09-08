---
name: "mysql-replication"
description: "Set up and manage MySQL source/replica replication: binary log config, CHANGE REPLICATION SOURCE TO, and replica health checks. Use when working with mysql replication setup, api or when the user mentions mysql replication setup, api."
license: "MIT"
compatibility: "Requires mysql."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(mysql:*)"
---

Set up and manage MySQL source/replica replication: binary log config, CHANGE REPLICATION SOURCE TO, and replica health checks.

## Agentic Workflow: Read -> Reason -> Act (mysql-replication)

You are **Mysql Replication** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mysql-replication`
- Domain: Set up and manage MySQL source/replica replication: binary log config, CHANGE REPLICATION SOURCE TO, and replica health checks.
- **mysql-replication-setup**: Configure binary logging, start/stop replicas, and monitor replication lag using mysql client SQL. — `mysql -u root -p -e "SHOW MASTER STATUS;"`
- Check `knowledge` and `prerequisites: mysql`

### 2. Reason — think for `mysql-replication`
- For `mysql-replication-setup`: Configure binary logging, start/stop replicas, and monitor replication lag using mysql client SQL. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mysql-replication` tools
- Tools: `Glob`, `Grep`, `Read`, `Mysql` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mysql-replication:50e15368`

# MySQL Replication

MySQL replication copies changes from a source server to one or more replicas via the binary log.

## What this skill does

- Enables binary logging and creates a replication user
- Points a replica at a source with CHANGE REPLICATION SOURCE TO
- Monitors lag, errors and thread state

## When to use

- Read scaling and HA architectures
- Migrating to a new server with minimal downtime
- Backing up without locking the source

## Real commands

```bash
# On the source: check binlog position
mysql -u root -p -e "SHOW MASTER STATUS;"
mysql -u root -p -e "SHOW BINARY LOGS;"

# Create replication user on source
mysql -u root -p -e "CREATE USER 'repl'@'%' IDENTIFIED BY 'secret'; GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';"

# On the replica: point at source
mysql -u root -p -e "CHANGE REPLICATION SOURCE TO SOURCE_HOST='10.0.0.2', SOURCE_USER='repl', SOURCE_PASSWORD='secret', SOURCE_LOG_FILE='mysql-bin.000123', SOURCE_LOG_POS=154;"

# Start and verify
mysql -u root -p -e "START REPLICA;"
mysql -u root -p -e "SHOW REPLICA STATUS\G"
```

## Initial snapshot

```bash
mysqldump -u root -p --all-databases --source-data=2 > dump.sql
mysql -u root -p < dump.sql
```

## Config (source)

```ini
[mysqld]
server-id=1
log_bin=mysql-bin
binlog_format=ROW
gtid_mode=ON
enforce_gtid_consistency=ON
```

## Best practices

- Use GTID-based replication on 8.x
- Watch `Seconds_Behind_Source` and `Last_SQL_Errno`
- Test failover by promoting the replica before you need it

## Capabilities

### mysql-replication-setup
Configure binary logging, start/stop replicas, and monitor replication lag using mysql client SQL.

**Parameters:**
- `source_host` (string): Host of the replication source
- `source_log_file` (string): Binary log file from SHOW MASTER STATUS
- `source_log_pos` (integer): Binary log position to replicate from

**Commands:**
- `mysql -u root -p -e "SHOW MASTER STATUS;"`
- `mysql -u root -p -e "SHOW BINARY LOGS;"`
- `mysql -u root -p -e "SHOW REPLICA STATUS\G"`
- `mysql -u root -p -e "START REPLICA;"`
- `mysql -u root -p -e "STOP REPLICA; RESET REPLICA ALL;"`

**Examples:**
- mysql -u root -p -e "CHANGE REPLICATION SOURCE TO SOURCE_HOST='10.0.0.2', SOURCE_USER='repl', SOURCE_PASSWORD='secret', SOURCE_LOG_FILE='mysql-bin.000123', SOURCE_LOG_POS=154;"
- mysqldump -u root -p --all-databases --source-data=2 > dump.sql
- mysql -u root -p -e "SELECT * FROM performance_schema.replication_connection_status\G"

## References
- [MySQL Replication docs](https://dev.mysql.com/doc/refman/8.0/en/replication.html)
- [CHANGE REPLICATION SOURCE TO](https://dev.mysql.com/doc/refman/8.0/en/change-replication-source-to.html)
