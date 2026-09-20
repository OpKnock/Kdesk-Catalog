---
name: "grpc-java"
description: "gRPC services and clients in Java with the Gradle protobuf plugin: proto codegen, ManagedChannel clients, and ServerBuilder-based servers."
---

# Grpc Java

gRPC services and clients in Java with the Gradle protobuf plugin: proto codegen, ManagedChannel clients, and ServerBuilder-based servers.

## Instructions

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
