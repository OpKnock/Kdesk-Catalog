---
name: "bson"
description: "Works with BSON (binary JSON) data: conversion with bsondump, mongoexport/mongorestore round-trips, and Python bson handling. Use when working with bsondump, mongo tools, python bson, api or when the user mentions bsondump, mongo tools, python bson, api."
---

Works with BSON (binary JSON) data: conversion with bsondump, mongoexport/mongorestore round-trips, and Python bson handling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bsondump file.bson`, `mongoexport --collection=users --out=users.bson --uri mongod`
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

# BSON

## What this skill does

Works with BSON data: converting BSON files to JSON with bsondump, exporting/importing with mongo tools, and encoding/decoding with Python's bson module.

## When to use

- Inspecting MongoDB dump files without a server
- Round-tripping data between clusters
- Handling BSON binary fields (ObjectId, dates) in scripts

## Real commands

```bash
# Inspect a BSON file
bsondump --pretty dump.bson | head -20

# Convert to JSON
bsondump --type=json collection.bson > collection.json

# Dump a database to archive
mongodump --uri mongodb://localhost:27017/app --archive=dump.bson

# Restore
mongorestore --drop --archive=dump.bson --uri mongodb://localhost:27017/app

# Python
python -c "from bson import BSON; d=BSON.encode({'hello': 'world'}); print(d.hex()); print(BSON.decode(d))"
```

## Testing

- Round-trip: decode a file, re-encode, and diff documents
- Verify ObjectId and ISODate fields survive conversion

## Best practices

- Use mongodump --archive for consistent snapshots
- Keep BSON sizes small: prefer compact field names
- Use json_util for JSON interop with extended types

## Capabilities

### bsondump
Convert BSON files to JSON for inspection.

**Parameters:**
- `file` (string): BSON file path
- `type` (string): Output type: json or debug

**Commands:**
- `bsondump file.bson`
- `bsondump --pretty file.bson`
- `bsondump --type=json file.bson > file.json`
- `bsondump --quiet file.bson`

**Examples:**
- bsondump --pretty dump.bson | head -20
- bsondump --type=json collection.bson > collection.json
- bsondump file.bson | jq .

### mongo-tools
Export/import BSON with mongo tools.

**Parameters:**
- `collection` (string): Collection name
- `uri` (string): MongoDB connection URI
- `archive` (string): Archive file

**Commands:**
- `mongoexport --collection=users --out=users.bson --uri mongodb://localhost:27017/app`
- `mongoexport --collection=users --out=users.json --uri mongodb://localhost:27017/app`
- `mongorestore --archive=users.bson --uri mongodb://localhost:27017/app`
- `mongorestore --drop --archive=dump.bson --uri mongodb://localhost:27017/app`
- `mongodump --uri mongodb://localhost:27017/app --archive=dump.bson`

**Examples:**
- mongodump --uri mongodb://localhost:27017/app --archive=dump.bson
- mongoexport --collection=orders --out=orders.bson --uri mongodb://localhost:27017/app --query '{"status":"paid"}'
- mongorestore --drop --archive=dump.bson --uri mongodb://localhost:27017/app

### python-bson
Encode/decode BSON with pymongo's bson module.

**Parameters:**
- `document` (string): Python dict to encode

**Commands:**
- `pip install pymongo`
- `python -c "from bson import BSON; d=BSON.encode({'a': 1, 'b': 'x'}); print(d.hex())"`
- `python -c "from bson import BSON; d=BSON.encode({'a': 1}); print(BSON.decode(d))"`
- `python -c "from bson import encode; print(encode({'ts': __import__('datetime').datetime.now()}).hex())"`

**Examples:**
- python -c "from bson import BSON; d=BSON.encode({'hello': 'world'}); print(d.hex()); print(BSON.decode(d))"
- python -c "from bson import json_util; print(json_util.dumps({'ts': __import__('datetime').datetime.utcnow()}))"
- python -c "from bson import ObjectId; print(ObjectId())"

## References
- [bsondump Reference](https://www.mongodb.com/docs/database-tools/bsondump/)
- [BSON Specification](https://bsonspec.org/)
- [MongoDB Database Tools](https://www.mongodb.com/docs/database-tools/)
