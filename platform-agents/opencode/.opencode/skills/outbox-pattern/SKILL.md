---
name: "outbox-pattern"
description: "Implements the transactional outbox approach with database outbox tables, poll-and-forward relay workers, and Debezium CDC connectors for reliable event publishing without dual-write problems. Use when working with outbox implementation, api or when the user mentions outbox implementation, api."
---

Implements the transactional outbox approach with database outbox tables, poll-and-forward relay workers, and Debezium CDC connectors for reliable event publishing without dual-write problems.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mysql -u app -p -e "SELECT * FROM outbox WHERE status='pendi`
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

# Outbox Pattern

The transactional outbox writes events to the same DB transaction as the business change, then relays them to the broker.

## What this skill does

- Designs outbox table schemas
- Implements relay workers (poll or CDC)
- Deploys Debezium connectors

## When to use

- Publishing events reliably from DB-backed services
- Avoiding dual-write problems (DB + broker)

## Real commands

```bash
# Relay worker polling
mysql -u app -p -e "SELECT * FROM outbox WHERE status='pending' ORDER BY id LIMIT 100;"
mysql -u app -p -e "UPDATE outbox SET status='sent' WHERE id IN (...);"

# Debezium connector lifecycle
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @outbox-connector.json
curl -s http://localhost:8083/connectors/outbox-connector/status
curl -X DELETE http://localhost:8083/connectors/outbox-connector
```

## Table schema

```sql
CREATE TABLE outbox (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  aggregate_type VARCHAR(100) NOT NULL,
  aggregate_id VARCHAR(100) NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  payload JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status ENUM('pending','sent') DEFAULT 'pending'
);
```

## Best practices

- Write event + business row in ONE transaction
- Make relay idempotent (publish, then mark sent)
- Add retention cleanup for old sent rows

## Capabilities

### outbox-implementation
Design outbox tables, poll-and-forward relay SQL, and Debezium outbox event router connectors.

**Parameters:**
- `table` (string): Outbox table name
- `status` (string): pending, sent or failed
- `connector_name` (string): Debezium connector name

**Commands:**
- `mysql -u app -p -e "SELECT * FROM outbox WHERE status='pending' ORDER BY id LIMIT 100;"`
- `mysql -u app -p -e "UPDATE outbox SET status='sent' WHERE id IN (...);"`
- `curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @outbox-connector.json`
- `curl -s http://localhost:8083/connectors`
- `curl -s http://localhost:8083/connectors/outbox-connector/status`

**Examples:**
- curl -s http://localhost:8083/connectors/outbox-connector/status | jq .
- mysql -u app -p -e "SELECT COUNT(*) FROM outbox WHERE status='pending';"
- curl -X DELETE http://localhost:8083/connectors/outbox-connector

## References
- [Debezium Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
- [Microservices.io Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html)
