Produce, consume, and inspect Kafka topics with it. Kafka topics.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kcat -b localhost:9092 -t orders -P`
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