---
name: "cbor"
description: "Encodes and decodes CBOR (RFC 8949) data with cbor2 (Python) and cbor (Node.js), including hex inspection and streaming. Use when working with python cbor2, node cbor, inspect, api or when the user mentions python cbor2, node cbor, inspect, api."
---

Encodes and decodes CBOR (RFC 8949) data with cbor2 (Python) and cbor (Node.js), including hex inspection and streaming.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install cbor2`, `npm install cbor`
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

# CBOR

## What this skill does

Encodes and decodes CBOR (RFC 8949) data: cbor2 for Python, cbor for Node.js, hex inspection with xxd, and size comparison against JSON.

## When to use

- Compact binary encoding for APIs or IoT payloads
- Reducing payload size vs JSON
- Debugging raw CBOR byte streams

## Real commands

```bash
# Python
pip install cbor2
python -c "import cbor2; d=cbor2.dumps({'hello':'world'}); print(d.hex())"
python -c "import cbor2; print(cbor2.loads(bytes.fromhex('a16568656c6c6f65776f726c64')))"

# Node
npm install cbor
node -e "const cbor=require('cbor'); console.log(cbor.encode({hello:'world'}).toString('hex'))"
node -e "const cbor=require('cbor'); cbor.decodeFirst(Buffer.from('a16568656c6c6f65776f726c64','hex')).then(console.log)"

# Inspect raw bytes
xxd data.cbor | head -10
file data.cbor
```

## Testing

- Round-trip encode/decode and compare with the original
- Compare byte lengths vs JSON.stringify for the same data

## Best practices

- Use canonical encoding when hashing payloads
- Prefer definite-length items for streaming
- Validate sizes; CBOR can embed large indefinite strings

## Capabilities

### python-cbor2
Encode/decode CBOR with the cbor2 library.

**Parameters:**
- `value` (string): Value to encode
- `hex` (string): Hex string to decode

**Commands:**
- `pip install cbor2`
- `python -c "import cbor2; d=cbor2.dumps({'hello':'world'}); print(d.hex())"`
- `python -c "import cbor2; print(cbor2.loads(bytes.fromhex('a16568656c6c6f65776f726c64')))"`
- `python -c "import cbor2; print(len(cbor2.dumps({'hello':'world'})))"`

**Examples:**
- python -c "import cbor2; d=cbor2.dumps({'hello':'world', 'n': 42}); print(d.hex())"
- python -c "import cbor2; print(cbor2.loads(cbor2.dumps({'a':[1,2,3]})))"
- python -c "import cbor2; print(cbor2.dumps(1234567890123456789).hex())"

### node-cbor
Encode/decode CBOR with the Node.js cbor package.

**Parameters:**
- `value` (string): JS value to encode
- `hex` (string): Hex input to decode

**Commands:**
- `npm install cbor`
- `node -e "const cbor=require('cbor'); console.log(cbor.encode({hello:'world'}).toString('hex'))"`
- `node -e "const cbor=require('cbor'); cbor.decodeFirst(Buffer.from('a16568656c6c6f65776f726c64','hex')).then(console.log)"`
- `node -e "const cbor=require('cbor'); const b=cbor.encode([1,2,3]); console.log(b.length, b.toString('hex'))"`

**Examples:**
- node -e "const cbor=require('cbor'); console.log(cbor.encode({a:1,b:'x'}).toString('hex'))"
- node -e "const cbor=require('cbor'); cbor.decodeFirst(cbor.encode(1234567890123456789n ? 1234567890123456789 : 42)).then(console.log)"
- node -e "const cbor=require('cbor'); cbor.encodeCanonical({b:1,a:2}).toString('hex').then ? cbor.encodeCanonical({b:1,a:2}).then(b=>console.log(b.toString('hex'))) : console.log(cbor.encodeCanonical({b:1,a:2}).toString('hex'))"

### inspect
Inspect raw CBOR bytes.

**Parameters:**
- `file` (string): CBOR file path

**Commands:**
- `xxd data.cbor | head -20`
- `xxd data.cbor | grep -A2 -B2 'a1'`
- `python -c "import cbor2; data=open('data.cbor','rb').read(); print(cbor2.loads(data))"`
- `file data.cbor`

**Examples:**
- xxd data.cbor | head -10
- python -c "import cbor2; print(cbor2.loads(open('data.cbor','rb').read()))"
- file data.cbor && xxd data.cbor | head -5

## References
- [RFC 8949 (CBOR)](https://www.rfc-editor.org/rfc/rfc8949)
- [cbor2 (Python)](https://cbor2.readthedocs.io/)
- [cbor.me Playground](https://cbor.me/)
