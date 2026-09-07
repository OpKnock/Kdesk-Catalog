---
name: "mongodb"
description: "Operates MongoDB: mongosh queries, indexes, backups with mongodump/restore, and exports. Use when working with mongodb shell, database or when the user mentions mongodb shell, database."
---

Operates MongoDB: mongosh queries, indexes, backups with mongodump/restore, and exports.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mongosh mongodb://localhost:27017/app`
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

# MongoDB

Document database operations: queries, indexes, aggregation, and backup/restore
via the database tools.

## When to Use

- Querying and aggregating documents
- Creating and analyzing indexes
- Backing up or moving data

## Real Commands

```bash
# Connect
sudo mongosh mongodb://localhost:27017/app

# CRUD via --eval
sudo mongosh app --eval "db.users.insertOne({name: 'jane', age: 34})"
sudo mongosh app --eval "db.users.find({age: {\$gt: 21}}).limit(5).toArray()"

# Indexes
sudo mongosh app --eval "db.users.createIndex({email: 1}, {unique: true})"
sudo mongosh app --eval "db.users.getIndexes()"

# Aggregation
sudo mongosh app --eval "db.orders.aggregate([{\$group: {_id: null, total: {\$sum: '\$amount'}}}]).toArray()"

# Backups
sudo mongodump --uri mongodb://localhost:27017/app --out ./backup
sudo mongorestore --uri mongodb://localhost:27017/ ./backup/app

# Export/import collections
sudo mongoexport --db app --collection users --out users.json
sudo mongoimport --db app --collection users --file users.json
```

## Best Practices

- Index every query field; explain before deploying
- Use aggregation pipeline, not mapReduce
- Test backup restore regularly
- Enable auth; never expose mongod publicly
- Watch `serverStatus().connections` for connection growth

## Example Response

For a slow query: runs explain(), reports the winning plan, and creates the
missing index, verifying with a re-run.

## Capabilities

### mongodb-shell
Query, manage, and diagnose MongoDB via mongosh

**Parameters:**
- `eval` (string): JavaScript expression to evaluate
- `quiet` (boolean): Suppress banner and shell output
- `authenticationDatabase` (string): Database that holds user credentials

**Commands:**
- `mongosh mongodb://localhost:27017/app`
- `mongosh app --eval "db.users.find({age: {$gt: 21}}).limit(5).toArray()"`
- `mongosh app --eval "db.users.createIndex({email: 1}, {unique: true})"`
- `mongosh app --eval "db.runCommand({serverStatus: 1}).connections"`
- `mongosh --eval "db.adminCommand({setParameter: 1, logLevel: 1})"`

**Examples:**
- mongosh app --eval "db.orders.aggregate([{$group: {_id: null, total: {$sum: '$amount'}}}]).toArray()"
- mongosh app --quiet --eval "db.users.countDocuments({})"
- mongosh --host localhost --port 27017 -u admin -p --authenticationDatabase admin

## References
- [MongoDB Shell docs](https://www.mongodb.com/docs/mongodb-shell/)
- [MongoDB Database Tools](https://www.mongodb.com/docs/database-tools/)
