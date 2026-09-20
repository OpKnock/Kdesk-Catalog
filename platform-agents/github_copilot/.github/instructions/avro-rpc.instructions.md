---
applyTo: "**/*.java **/*.json **/*.r **/*.sh"
---

# Avro Rpc

Implements RPC services with Apache Avro: schema compilation, avro-tools operations, and Java RPC server/client testing.

## Instructions

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
