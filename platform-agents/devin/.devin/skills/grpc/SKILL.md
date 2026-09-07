---
name: "grpc"
description: "General gRPC API operations with grpcurl: listing services, describing schemas, invoking unary and streaming RPCs, and debugging from the CLI. Use when working with grpcurl ops, api or when the user mentions grpcurl ops, api."
license: "MIT"
compatibility: "Requires grpcurl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(go:*) Bash(grpcurl:*)"
---

General gRPC API operations with grpcurl: listing services, describing schemas, invoking unary and streaming RPCs, and debugging from the CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go install github.com/fullstorydev/grpcurl/cmd/grpcurl@lates`
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

**Parameters:**
- `target` (string): gRPC endpoint host:port.
- `method` (string): Fully-qualified method, e.g. mypackage.MyService/SayHello.
- `data` (string): JSON payload for the call (-d).

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

## References
- [gRPC Core Docs](https://grpc.io/docs/)
- [grpcurl README](https://github.com/fullstorydev/grpcurl)
