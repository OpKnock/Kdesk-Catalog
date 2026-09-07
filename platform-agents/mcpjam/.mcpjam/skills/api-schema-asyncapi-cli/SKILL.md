---
name: "api-schema-asyncapi-cli"
description: "Authors event API schemas with AsyncAPI and Apache Avro: AsyncAPI document validation and generation, Avro schema tooling, and Kafka payload contracts. Use when working with asyncapi cli, avro tools or when the user mentions asyncapi cli, avro tools."
license: "MIT"
compatibility: "Requires openapi, json-schema, node.js, python, stoplight-studio."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "data"}
allowed-tools: "Glob Grep Read Bash(asyncapi:*) Bash(java:*) Bash(npm:*)"
---

Authors event API schemas with AsyncAPI and Apache Avro: AsyncAPI document validation and generation, Avro schema tooling, and Kafka payload contracts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g @asyncapi/cli`, `java -jar avro-tools-1.11.3.jar compile schema user.avsc .`
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

# API Schema v4 - AsyncAPI/Avro

Event schema authoring.

## What This Skill Does
- Documents event-driven APIs with AsyncAPI
- Compiles Avro schemas for Kafka
- Generates docs and stubs

## When to Use
- Kafka/Kinesis event contracts
- Event-driven microservices
- Schema registry management

## Real Commands

```bash
npm install -g @asyncapi/cli
asyncapi validate asyncapi.yaml
asyncapi generate fromTemplate asyncapi.yaml @asyncapi/html-template -o docs
java -jar avro-tools-1.11.3.jar compile schema user.avsc .
```

## Avro Schema

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    { "name": "id", "type": "long" },
    { "name": "email", "type": "string" }
  ]
}
```

## Testing
- Validate documents in CI
- Round-trip JSON to Avro and back
- Check schema registry compatibility

## Best Practices
- Version event schemas with a registry
- Use forward/backward compatible fields
- Keep AsyncAPI docs in sync with topics

## Capabilities

### asyncapi-cli
Validate and generate AsyncAPI documents

**Parameters:**
- `spec` (string): AsyncAPI document path
- `template` (string): Generator template
- `output` (string): Output directory

**Commands:**
- `npm install -g @asyncapi/cli`
- `asyncapi validate asyncapi.yaml`
- `asyncapi new --example=tutorial`
- `asyncapi generate fromTemplate asyncapi.yaml @asyncapi/html-template -o docs`
- `asyncapi bundle asyncapi.yaml -o bundled.yaml`

**Examples:**
- asyncapi validate checks document structure
- asyncapi new scaffolds an example
- generate fromTemplate builds HTML docs

### avro-tools
Compile and inspect Avro schemas

**Commands:**
- `java -jar avro-tools-1.11.3.jar compile schema user.avsc .`
- `java -jar avro-tools-1.11.3.jar getmeta user.avsc`
- `java -jar avro-tools-1.11.3.jar tojson users.avro`
- `java -jar avro-tools-1.11.3.jar fromjson --schema-file user.avsc users.json > users.avro`

**Examples:**
- -cli --help
- -api --help

## References
- [AsyncAPI CLI](https://www.asyncapi.com/docs/tools/cli)
- [Avro Spec](https://avro.apache.org/docs/current/specification/)
