---
name: "grpc-java"
description: "gRPC services and clients in Java with the Gradle protobuf plugin: proto codegen, ManagedChannel clients, and ServerBuilder-based servers. Use when working with java grpc, api or when the user mentions java grpc, api."
license: "MIT"
compatibility: "Requires ./gradlew, grpcurl, java. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(./gradlew:*) Bash(grpcurl:*) Bash(java:*)"
---

gRPC services and clients in Java with the Gradle protobuf plugin: proto codegen, ManagedChannel clients, and ServerBuilder-based servers.

## Agentic Workflow: Read -> Reason -> Act (grpc-java)

You are **Grpc Java** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `grpc-java`
- Domain: gRPC services and clients in Java with the Gradle protobuf plugin: proto codegen, ManagedChannel clients, and ServerBuilder-based servers.
- **java-grpc**: Configure Gradle protobuf codegen, implement Java gRPC servers, and run clients. — `./gradlew generateProto`
- Check `knowledge` and `prerequisites: ./gradlew, grpcurl, java`

### 2. Reason — think for `grpc-java`
- For `java-grpc`: Configure Gradle protobuf codegen, implement Java gRPC servers, and run clients. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `grpc-java` tools
- Tools: `Glob`, `Grep`, `Read`, `./gradlew`, `Java` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `grpc-java:d0eb90c1`

# gRPC Java

Write gRPC services and clients in Java with the protobuf Gradle plugin.

## What this skill does

- Generates Java gRPC stubs from proto files during the Gradle build.
- Implements servers with ServerBuilder and clients with ManagedChannel.
- Probes generated stubs with grpcurl for verification.
- Writes service unit tests with in-process channels.

## When to use

- A JVM microservice team adopts gRPC contracts.
- Backend clients need typed RPC calls.
- Migrating REST endpoints to gRPC in an existing Gradle repo.

## Real commands

```bash
# Generate stubs and build
./gradlew generateProto
./gradlew build

# Run server and client
./gradlew run
java -cp build/libs/app.jar com.example.GreeterServer &
java -cp build/libs/app.jar com.example.GreeterClient

# Probe from outside
grpcurl -plaintext -d '{"name":"Java"}' localhost:50051 helloworld.Greeter/SayHello
```

## Gradle config

```groovy
plugins {
  id 'com.google.protobuf' version '0.9.4'
  id 'java'
}

dependencies {
  implementation 'io.grpc:grpc-netty-shaded:1.64.0'
  implementation 'io.grpc:grpc-protobuf:1.64.0'
  implementation 'io.grpc:grpc-stub:1.64.0'
  compileOnly 'org.apache.tomcat:annotations-api:6.0.53'
}

protobuf {
  protoc { artifact = 'com.google.protobuf:protoc:3.25.3' }
  plugins { grpc { artifact = 'io.grpc:protoc-gen-grpc-java:1.64.0' } }
  generateProtoTasks { all()*.plugins { grpc {} } }
}
```

## Server skeleton

```java
Server server = ServerBuilder.forPort(50051)
  .addService(new GreeterServiceImpl())
  .build();
server.start();
server.awaitTermination();
```

## Testing

```java
GrpcCleanupRule cleanupRule = new GrpcCleanupRule();
InProcessServerBuilder.forName("test").directExecutor().addService(new GreeterServiceImpl()).build();
```

## Best practices

- Use grpc-netty-shaded to avoid Netty version conflicts.
- Add the tomcat annotations-api compileOnly dep or javax.annotation is unresolved.
- Set `deadline = 10, TimeUnit.SECONDS` on blocking stubs.
- Pin protoc and protoc-gen-grpc-java to matching versions.

## Example exchange

```
User: Gradle fails: package javax.annotation does not exist.
Agent: Add compileOnly 'org.apache.tomcat:annotations-api:6.0.53' to dependencies.
```

## Capabilities

### java-grpc
Configure Gradle protobuf codegen, implement Java gRPC servers, and run clients.

**Parameters:**
- `main_class` (string): Java main class to run the server or client.
- `grpc_version` (string): gRPC Java version, e.g. 1.64.0.
- `port` (integer): Server listen port, default 50051.

**Commands:**
- `./gradlew generateProto`
- `./gradlew build`
- `./gradlew run`
- `java -cp build/libs/app.jar com.example.GreeterServer`
- `grpcurl -plaintext localhost:50051 helloworld.Greeter/SayHello -d '{"name":"Java"}'`

**Examples:**
- ./gradlew clean generateProto build
- java -cp build/libs/app.jar com.example.GreeterClient
- ./gradlew test --tests '*.GreeterServiceTest'

## References
- [gRPC Java Docs](https://grpc.io/docs/languages/java/)
- [grpc-java GitHub](https://github.com/grpc/grpc-java)
