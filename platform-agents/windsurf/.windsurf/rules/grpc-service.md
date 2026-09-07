---
trigger: glob
description: "Builds gRPC services with protobuf definitions, grpcurl inspection, and language-specific code generation. Use when working with protobuf codegen, grpc debugging, backend or when the user mentions protobuf codegen, grpc debugging, backend."
globs: ["**/*.go", "**/*.py", "**/*.r", "**/*.sh"]
---

Builds gRPC services with protobuf definitions, grpcurl inspection, and language-specific code generation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `protoc --go_out=. --go-grpc_out=. proto/order.proto`, `grpcurl -plaintext localhost:50051 list`
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

# gRPC Service

Build high-performance RPC services with protobuf.

## When to Use

- Internal service-to-service communication
- Streaming workloads (bidirectional streams)
- Polyglot systems needing generated clients
- Services needing strict typed contracts

## Proto Example

```proto
syntax = "proto3";

package order;

service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
}

message GetOrderRequest {
  string id = 1;
}

message Order {
  string id = 1;
  double total = 2;
  repeated string items = 3;
}
```

## Commands

```bash
# Generate Go stubs
protoc --go_out=. --go_opt=paths=source_relative \
  --go-grpc_out=. proto/order.proto

# Python stubs
protoc --python_out=. --grpc_python_out=. proto/order.proto

# Buf workflow
buf lint
buf generate
buf breaking --against .git#branch=main

# Inspect and call live servers
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext -d '{"id":"1"}' localhost:50051 order.OrderService/GetOrder
grpcurl -plaintext localhost:50051 describe order.OrderService
```

## Best Practices

- Never break wire compatibility; add fields instead of renaming
- Use buf breaking in CI to catch incompatible changes
- Set deadlines on every client call; servers enforce them too
- Keep messages small; gRPC default max message is 4MB
- Reserve field numbers when planning for removal
- Always run a plaintext grpcurl check before enabling TLS

## Capabilities

### protobuf-codegen
Compile protobuf definitions and generate server/client stubs.

**Parameters:**
- `out` (string): Output directory for generated code
- `proto-file` (string): Protobuf file to compile

**Commands:**
- `protoc --go_out=. --go-grpc_out=. proto/order.proto`
- `protoc --python_out=. --grpc_python_out=. proto/order.proto`
- `protoc --js_out=import_style=commonjs,binary:./out proto/order.proto`
- `buf generate`
- `buf lint`

**Examples:**
- protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. proto/*.proto
- buf generate --path proto
- buf breaking --against .git#branch=main

### grpc-debugging
Call and inspect gRPC services without writing code.

**Parameters:**
- `service` (string): Service name
- `method` (string): Method name
- `data` (string): JSON request body

**Commands:**
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext -d "{\"id\":\"1\"}" localhost:50051 order.OrderService/GetOrder`
- `grpcurl -plaintext localhost:50051 describe order.OrderService`
- `buf curl --schema proto localhost:50051 order.OrderService/GetOrder -d "{\"id\":\"1\"}"`

**Examples:**
- grpcurl -plaintext localhost:50051 list order
- grpcurl -plaintext -import-path proto -proto order.proto -d "{}" localhost:50051 order.OrderService/CreateOrder
- grpcurl -plaintext localhost:50051 describe order.Order

## References
- [gRPC Docs](https://grpc.io/docs/)
- [Protobuf Language Guide](https://protobuf.dev/programming-guides/proto3/)
- [grpcurl](https://github.com/fullstorydev/grpcurl)
