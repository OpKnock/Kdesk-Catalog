---
name: "messagepack"
description: "MessagePack binary serialization: encode/decode payloads, integrate MessagePack into APIs, and debug binary message dumps."
---

# Messagepack

MessagePack binary serialization: encode/decode payloads, integrate MessagePack into APIs, and debug binary message dumps.

## Instructions

# MessagePack

MessagePack is an efficient binary serialization format that represents JSON-like objects as compact binary data.

## What this skill does

- Encodes JSON data into MessagePack binary for storage or wire transfer
- Decodes MessagePack binaries back into human-readable JSON
- Verifies that a production client and server agree on the same payload bytes

## When to use

- Replacing JSON with a compact binary format on HTTP or TCP APIs
- Debugging raw MessagePack payloads captured from a wire or a message queue
- Adding MessagePack support to Python/Go/Java services

## Real commands

```bash
# Encode JSON file to MessagePack
cat user-data.json | json2msgpack > user-data.msgpack

# Decode MessagePack to JSON
cat user-data.msgpack | msgpack2json
cat user-data.msgpack | msgpack2json -j   # pretty printed

# Inspect binary payload with Python
python3 -c "import msgpack; print(msgpack.unpackb(open('user-data.msgpack','rb').read(), raw=False))"

# Hex-dump to verify on-the-wire bytes
xxd user-data.msgpack
```

## Language integration

```python
# Python client
import msgpack
payload = msgpack.packb({"user": "alice", "roles": ["admin"]}, use_bin_type=True)
msg = msgpack.unpackb(payload, raw=False)
```

```go
// Go: gopkg.in/vmihailenco/msgpack.v2
b, _ := msgpack.Marshal(map[string]interface{}{"user": "alice"})
var m map[string]interface{}
msgpack.Unmarshal(b, &m)
```

## Testing

Round-trip a payload and compare bytes before and after re-encoding:

```bash
cat user-data.json | json2msgpack > user-data-roundtrip.msgpack
cat user-data-roundtrip.msgpack | msgpack2json -j > user-data-roundtrip.json
python3 -c "import json,sys; a=json.load(open('user-data.json')); b=json.load(open('user-data-roundtrip.json')); sys.exit(0 if a==b else 1)"
```

## Best practices

- Use `use_bin_type=True` / `use_ext_types` so strings and bytes stay distinct
- Always send `Content-Type: application/msgpack` on HTTP endpoints
- Never log raw binary; base64-encode first with `base64 user-data.msgpack`

## Capabilities

### messagepack-encode-decode
Encode JSON to MessagePack, decode MessagePack to JSON, and inspect binary payloads using the msgpack-tools utilities.

**Commands:**
- `cat user-data.json | json2msgpack > user-data.msgpack`
- `cat user-data.msgpack | msgpack2json`
- `cat user-data.msgpack | msgpack2json -j`
- `python3 -c "import msgpack,sys; print(msgpack.unpackb(open('user-data.msgpack','rb').read(), raw=False))"`
- `msgpack-cli decode user-data.msgpack`

**Examples:**
- cat user-data.json | json2msgpack > user-data.msgpack
- cat user-data.msgpack | msgpack2json -j
- python3 -c "import msgpack; print(msgpack.packb({'a':1,'b':[1,2,3]}, use_bin_type=True))"
