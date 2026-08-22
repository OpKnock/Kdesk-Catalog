---
name: "bson"
description: "Works with BSON (binary JSON) data: conversion with bsondump, mongoexport/mongorestore round-trips, and Python bson handling."
type: knowledge
triggers: ["bson", "bsondump", "mongo-tools", "python-bson"]
---

# Bson

Works with BSON (binary JSON) data: conversion with bsondump, mongoexport/mongorestore round-trips, and Python bson handling.

## Instructions

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

**Commands:**
- `pip install pymongo`
- `python -c "from bson import BSON; d=BSON.encode({'a': 1, 'b': 'x'}); print(d.hex())"`
- `python -c "from bson import BSON; d=BSON.encode({'a': 1}); print(BSON.decode(d))"`
- `python -c "from bson import encode; print(encode({'ts': __import__('datetime').datetime.now()}).hex())"`

**Examples:**
- python -c "from bson import BSON; d=BSON.encode({'hello': 'world'}); print(d.hex()); print(BSON.decode(d))"
- python -c "from bson import json_util; print(json_util.dumps({'ts': __import__('datetime').datetime.utcnow()}))"
- python -c "from bson import ObjectId; print(ObjectId())"
