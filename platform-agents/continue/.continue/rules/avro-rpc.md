---
name: "Avro Rpc"
description: "Implements RPC services with Apache Avro: schema compilation, avro-tools operations, and Java RPC server/client testing. Use when working with schema tools, rpc protocol, java server, api or when the user mentions schema tools, rpc protocol, java server, api."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Implements RPC services with Apache Avro: schema compilation, avro-tools operations, and Java RPC server/client testing.

## Agentic Workflow: Read -> Reason -> Act (avro-rpc)

You are **Avro Rpc** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `avro-rpc`
- Domain: Implements RPC services with Apache Avro: schema compilation, avro-tools operations, and Java RPC server/client testing.
- **schema-tools**: Compile schemas and convert data with avro-tools. — `java -jar avro-tools.jar compile schema user.avsc .`
- **rpc-protocol**: Define and compile RPC protocols with avro-tools. — `java -jar avro-tools.jar compile protocol chat.avpr .`
- **java-server**: Build and test a Java Avro RPC server. — `mvn package`
- Check `knowledge` and `prerequisites: java, mvn`

### 2. Reason — think for `avro-rpc`
- For `schema-tools`: Compile schemas and convert data with avro-tools. — decide which checks to run
- For `rpc-protocol`: Define and compile RPC protocols with avro-tools. — decide which checks to run
- For `java-server`: Build and test a Java Avro RPC server. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `avro-rpc` tools
- Tools: `Glob`, `Grep`, `Read`, `Java`, `Mvn` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `avro-rpc:a68a7717`

# Avro RPC

## What this skill does

Implements RPC services with Apache Avro: writing schemas and IDL, compiling them with avro-tools, generating Java stubs, and running/test the server and client.

## When to use

- A typed, schema-driven RPC layer instead of raw JSON
- Generating stubs from .avsc/.avpr for Java services
- Evolving message formats safely (Avro schema resolution)

## Real commands

```bash
# Compile a schema to Java
java -jar avro-tools.jar compile schema user.avsc src/main/java

# Generate a protocol from IDL
java -jar avro-tools.jar idl src/main/avro/chat.avdl chat.avpr
java -jar avro-tools.jar compile protocol chat.avpr src/main/java

# Convert data
java -jar avro-tools.jar tojson user.avro
java -jar avro-tools.jar fromjson user.json --schema-file user.avsc

# Run the RPC server
mvn exec:java -Dexec.mainClass=com.example.ChatServer
```

## IDL example (chat.avdl)

```avdl
@namespace("com.example")
protocol Chat {
  string send(string message);
}
```

## Testing

- Start the server, run the client with mvn exec:java, assert the echo returns
- Round-trip JSON: fromjson then tojson must match the input

## Best practices

- Keep .avsc/.avdl in src/main/avro and regenerate on build
- Use schema evolution rules (defaults, unions) for backward compat
- Prefer the Avro RPC handshake over ad-hoc endpoints for typed services

## Capabilities

### schema-tools
Compile schemas and convert data with avro-tools.

**Parameters:**
- `schema_file` (string): Avro schema .avsc file
- `output_dir` (string): Directory for compiled classes

**Commands:**
- `java -jar avro-tools.jar compile schema user.avsc .`
- `java -jar avro-tools.jar tojson user.avro`
- `java -jar avro-tools.jar fromjson user.json --schema-file user.avsc`
- `java -jar avro-tools.jar getmeta user.avro`
- `java -jar avro-tools.jar cat user.avro`

**Examples:**
- java -jar avro-tools.jar compile schema user.avsc src/main/java
- java -jar avro-tools.jar tojson user.avro > user.json
- java -jar avro-tools.jar fromjson user.json --schema-file user.avsc > out.avro

### rpc-protocol
Define and compile RPC protocols with avro-tools.

**Parameters:**
- `protocol_file` (string): .avpr protocol file or .avdl IDL
- `output_dir` (string): Output for generated stubs

**Commands:**
- `java -jar avro-tools.jar compile protocol chat.avpr .`
- `java -jar avro-tools.jar idl src/main/avro/chat.avdl chat.avpr`
- `java -jar avro-tools.jar idl2schemata chat.avdl`
- `java -jar avro-tools.jar jsonschema chat.avsc`

**Examples:**
- java -jar avro-tools.jar idl src/main/avro/chat.avdl chat.avpr
- java -jar avro-tools.jar compile protocol chat.avpr src/main/java
- java -jar avro-tools.jar idl2schemata chat.avdl

### java-server
Build and test a Java Avro RPC server.

**Parameters:**
- `main_class` (string): Server/client main class
- `port` (number): RPC server port (default 8080)

**Commands:**
- `mvn package`
- `mvn exec:java -Dexec.mainClass=com.example.ChatServer`
- `mvn exec:java -Dexec.mainClass=com.example.ChatClient`
- `curl -s http://localhost:8080/health`
- `mvn test`

**Examples:**
- mvn package && java -jar target/chat-rpc-1.0.jar server
- mvn exec:java -Dexec.mainClass=com.example.ChatClient -Dexec.args=localhost
- mvn test -Dtest=ChatRpcTest

## References
- [Apache Avro Docs](https://avro.apache.org/docs/current/)
- [Avro Spec](https://avro.apache.org/docs/current/specification/)
- [avro-tools Reference](https://avro.apache.org/docs/current/getting-started-java/)