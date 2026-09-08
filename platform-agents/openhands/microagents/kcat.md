---
name: "kcat"
description: "Produce, consume, and inspect Kafka topics with it. Kafka topics.'. Use when working with kcat commands, database or when the user mentions kcat commands, database."
type: knowledge
triggers: ["kcat", "kcat-commands"]
---

Produce, consume, and inspect Kafka topics with it. Kafka topics.'

## Agentic Workflow: Read -> Reason -> Act (kcat)

You are **kcat** (database/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — database context for `kcat`
- Domain: Produce, consume, and inspect Kafka topics with it. Kafka topics.'
- **kcat-commands**: Produce, consume, and inspect Kafka topics with kcat — `kcat -b localhost:9092 -t orders -P`
- Check `knowledge` and `prerequisites: kcat`

### 2. Reason — think for `kcat`
- For `kcat-commands`: Produce, consume, and inspect Kafka topics with kcat — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kcat` tools
- Tools: `Glob`, `Grep`, `Read`, `Kcat` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kcat:77f2089b`

# kcat

Lightweight CLI for Kafka: produce messages from stdin, consume to stdout, and
inspect topics and brokers.

## When to Use

- Debugging message flow during development
- One-off data injection for tests
- Inspecting topic layout, offsets, and consumer info

## Real Commands

```bash
# Produce from stdin (one message per line)
echo '{"order_id": 1, "amount": 99.5}' | kcat -b localhost:9092 -t orders -P

# Produce from a file
sudo kcat -b localhost:9092 -t orders -P -l messages.jsonl

# Consume the last 10 messages
sudo kcat -b localhost:9092 -t orders -C -o -10

# Structured output with key/offset
sudo kcat -b localhost:9092 -t orders -C -f '%t %p %o %k %s\n' -c 5

# Metadata listing
sudo kcat -b localhost:9092 -L
sudo kcat -b localhost:9092 -L -J | jq '.topics'
```

## Format Placeholders

- `%t` topic, `%p` partition, `%o` offset, `%k` key, `%s` value
- `%h` headers, `%T` timestamp

## Best Practices

- Use `-c N` to bound consumption in scripts
- Pipe keys with `-K: ` delimiter when keys are needed
- Use `-e` to exit when the end of a finite partition is reached
- Prefer `-J` JSON metadata for scripting

## Example Response

Produces the test messages, consumes them back with offsets, and reports the
topic metadata layout.

## Capabilities

### kcat-commands
Produce, consume, and inspect Kafka topics with kcat

**Parameters:**
- `offset` (string): Start offset: beginning, end, or -10
- `format` (string): Message output format string (-f)
- `exit` (boolean): Exit after consuming (-e) or print parsed exit codes

**Commands:**
- `kcat -b localhost:9092 -t orders -P`
- `kcat -b localhost:9092 -t orders -C -o -10`
- `kcat -b localhost:9092 -L`
- `kcat -b localhost:9092 -t orders -C -f '%t %p %o %k %s\n' -c 5`
- `kcat -b localhost:9092 -t orders -C -e -o beginning -c 10`

**Examples:**
- echo '{"id":1}' | kcat -b localhost:9092 -t orders -P -l
- kcat -b localhost:9092 -t orders -C -q -o end -c 5
- kcat -b localhost:9092 -L -J | jq '.topics[0]'

## References
- [kcat GitHub](https://github.com/edenhill/kcat)
- [kcat usage examples](https://github.com/edenhill/kcat#examples)
