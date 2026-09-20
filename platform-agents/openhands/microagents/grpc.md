---
name: "grpc"
description: "General gRPC API operations with grpcurl: listing services, describing schemas, invoking unary and streaming RPCs, and debugging from the CLI."
type: knowledge
triggers: ["grpc", "grpcurl-ops"]
---

# grpc

General gRPC API operations with grpcurl: listing services, describing schemas, invoking unary and streaming RPCs, and debugging from the CLI.

## Instructions

# gRPC

General gRPC API operations using the real `grpcurl` CLI.

## What this skill does

- Lists services and methods on a running gRPC server.
- Invokes unary and streaming RPCs with JSON payloads.
- Describes message and service schemas (from reflection or proto files).
- Handles both plaintext and TLS endpoints.

## When to use

- Testing gRPC services during development.
- Debugging a production gRPC call path.
- Learning a service contract before writing a client.

## Real commands

```bash
# Install
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# List services
grpcurl -plaintext localhost:50051 list

# List methods
grpcurl -plaintext localhost:50051 list mypackage.MyService

# Call a method
grpcurl -plaintext -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello

# Call with a local proto file
grpcurl -proto myservice.proto -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello

# Streaming call
grpcurl -plaintext -d '{"name":"John"}' localhost:50051 mypackage.MyService/StreamMessages

# Describe schemas
grpcurl -plaintext localhost:50051 describe mypackage.MyService
grpcurl -plaintext localhost:50051 describe mypackage.HelloRequest
```

## Server Reflection

```bash
# With reflection enabled on the server:
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe
```

## Example proto

```protobuf
syntax = "proto3";
package mypackage;

service MyService {
  rpc SayHello (HelloRequest) returns (HelloResponse);
  rpc StreamMessages (HelloRequest) returns (stream HelloResponse);
}

message HelloRequest { string name = 1; }
message HelloResponse { string message = 1; }
```

## Testing

```bash
grpcurl -plaintext -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello
# expected: { "message": "Hello John" }
```

## Best practices

- Use `-max-time` on flaky endpoints: `grpcurl -plaintext -max-time 10 ...`.
- Pipe responses through jq: `grpcurl ... | jq .`.
- Prefer reflection when available; fall back to `-proto` files otherwise.
- For interactive exploration, try evans (see grpc-v2 skill) with `-r` repl mode.

## Example exchange

```
User: What methods does the Greeter service expose?
Agent: grpcurl -plaintext localhost:50051 list helloworld.Greeter
```

## Capabilities

### grpcurl-ops
Inspect and call gRPC services from the command line with grpcurl.

**Commands:**
- `go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest`
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext localhost:50051 list mypackage.MyService`
- `grpcurl -plaintext -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello`
- `grpcurl -plaintext localhost:50051 describe mypackage.MyService`

**Examples:**
- grpcurl -plaintext -proto myservice.proto -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello
- grpcurl -plaintext localhost:50051 describe mypackage.HelloRequest
- grpcurl -plaintext -d '{"name":"x"}' localhost:50051 mypackage.MyService/StreamMessages
