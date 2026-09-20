---
name: "grpc-service"
description: "Builds gRPC services with protobuf definitions, grpcurl inspection, and language-specific code generation."
---

# Grpc Service

Builds gRPC services with protobuf definitions, grpcurl inspection, and language-specific code generation.

## Instructions

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

**Commands:**
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext -d "{\"id\":\"1\"}" localhost:50051 order.OrderService/GetOrder`
- `grpcurl -plaintext localhost:50051 describe order.OrderService`
- `buf curl --schema proto localhost:50051 order.OrderService/GetOrder -d "{\"id\":\"1\"}"`

**Examples:**
- grpcurl -plaintext localhost:50051 list order
- grpcurl -plaintext -import-path proto -proto order.proto -d "{}" localhost:50051 order.OrderService/CreateOrder
- grpcurl -plaintext localhost:50051 describe order.Order
