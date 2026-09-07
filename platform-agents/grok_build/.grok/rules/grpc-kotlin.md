gRPC services and clients in Kotlin using grpc-kotlin coroutines stubs: suspend RPCs, Flow-based streaming, and Gradle codegen wiring.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `protoc --plugin=protoc-gen-grpckt=$(which protoc-gen-grpc-ko`
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

# gRPC Kotlin

Suspend-based gRPC services and clients with grpc-kotlin coroutines.

## What this skill does

- Generates Kotlin stubs (suspend functions and Flow streams) from protos.
- Implements servers without blocking: suspend RPC handlers run on coroutines.
- Consumes server-streaming RPCs as Kotlin Flow.
- Wires the Gradle build for both java and kotlin stub codegen.

## When to use

- A Kotlin backend wants idiomatic coroutine RPC handling.
- Streaming responses should map directly to Flow for reactive clients.
- Replacing hand-rolled retrofit calls with typed gRPC contracts.

## Real commands

```bash
# Download the codegen plugin from grpc-kotlin releases
curl -L -o protoc-gen-grpc-kotlin https://github.com/grpc/grpc-kotlin/releases/download/1.4.1/protoc-gen-grpc-kotlin
chmod +x protoc-gen-grpc-kotlin

protoc --plugin=protoc-gen-grpckt=$(pwd)/protoc-gen-grpc-kotlin \
  --grpckt_out=build/generated --proto_path src/main/proto greet.proto

# Build and run via Gradle
./gradlew generateProto
./gradlew run

# Verify
grpcurl -plaintext -d '{"name":"Kotlin"}' localhost:50051 helloworld.Greeter/SayHello
```

## Gradle deps

```kotlin
implementation("io.grpc:grpc-kotlin-stub:1.4.1")
implementation("io.grpc:grpc-netty-shaded:1.64.0")
implementation("com.google.protobuf:protobuf-kotlin:3.25.3")
```

## Server skeleton

```kotlin
object GreeterService : GreeterGrpcKt.GreeterCoroutineImplBase() {
  override suspend fun sayHello(request: HelloRequest): HelloReply =
    HelloReply.newBuilder().setMessage("Hello ${request.name}").build()
}
```

## Streaming via Flow

```kotlin
override fun streamMessages(request: HelloRequest): Flow<HelloReply> =
  flow { emit(HelloReply.newBuilder().setMessage("one").build())
         emit(HelloReply.newBuilder().setMessage("two").build()) }
```

## Testing

```bash
./gradlew test
```

Use `GrpcCleanupRule` with InProcessServerBuilder for unit tests.

## Best practices

- Prefer the coroutine stubs (`*CoroutineImplBase`, `*CoroutineStub`) over blocking stubs.
- Return `flow { }` lazily; never pre-buffer infinite streams.
- Cancel client Flows to cancel the underlying call.
- Keep protoc and grpc-kotlin versions aligned with grpc-java.

## Example exchange

```
User: My streaming handler buffers the whole list before returning.
Agent: Return a cold flow and emit as data arrives:
       override fun streamMessages(request: HelloRequest) = flow { ... }
```

## Capabilities

### kotlin-grpc
Generate Kotlin gRPC stubs with protoc-gen-grpc-kotlin and write coroutine-based RPC services.

**Parameters:**
- `grpc_kotlin_version` (string): grpc-kotlin library version, e.g. 1.4.1.
- `plugin_path` (string): Path to the protoc-gen-grpc-kotlin executable.
- `proto_dir` (string): Directory containing .proto files.

**Commands:**
- `protoc --plugin=protoc-gen-grpckt=$(which protoc-gen-grpc-kotlin) --grpckt_out=build/generated --proto_path src/main/proto greet.proto`
- `./gradlew generateProto`
- `./gradlew run`
- `./gradlew build`
- `grpcurl -plaintext localhost:50051 helloworld.Greeter/SayHello`

**Examples:**
- protoc --plugin=protoc-gen-grpckt=$(which protoc-gen-grpc-kotlin) --grpckt_out=build/generated --proto_path src/main/proto greet.proto
- ./gradlew test --tests '*GreeterTest'
- grpcurl -plaintext -d '{"name":"Kotlin"}' localhost:50051 helloworld.Greeter/SayHello

## References
- [gRPC Kotlin Docs](https://grpc.io/docs/languages/kotlin/)
- [grpc-kotlin GitHub](https://github.com/grpc/grpc-kotlin)