---
name: "grpcurl"
description: "Interacts with gRPC servers from the CLI with grpcurl, including reflection, protobuf imports, and metadata headers. Use when working with grpc reflection, grpc calls, protobuf imports, testing or when the user mentions grpc reflection, grpc calls, protobuf imports, testing."
license: "MIT"
compatibility: "Requires grpcurl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(grpcurl:*)"
---

Interacts with gRPC servers from the CLI with grpcurl, including reflection, protobuf imports, and metadata headers.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `grpcurl -plaintext localhost:50051 list`, `grpcurl -plaintext -d '{"name": "world"}' localhost:50051 my`
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

# grpcurl

Test and debug gRPC services from the command line.

## What This Skill Does

- Lists and describes services via server reflection
- Invokes unary and streaming RPCs with JSON input
- Sends metadata headers (auth, tracing)
- Works with proto files when reflection is off

## When to Use

- Smoke-testing a gRPC endpoint
- Exploring an unknown service's API
- Debugging auth or deadline issues

## Real Commands

```bash
# Reflection
 grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe my.package.Greeter

# Calls
 grpcurl -plaintext -d '{"name": "world"}' localhost:50051 my.package.Greeter/SayHello
grpcurl -plaintext -d '{"id": 1}' -H 'authorization: Bearer TOKEN' localhost:50051 my.package.Users/Get

# Streaming (stdin)
 grpcurl -plaintext -d @ localhost:50051 my.package.Chat/Send <<< '{"msg": "hi"}'

# Proto imports without reflection
 grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{"name":"x"}' localhost:50051 hello.Greeter/SayHello
```

## Best Practices

- Enable server reflection in dev environments
- Always set -max-time to avoid hangs
- Verify error details in the grpc-status trailer
- Test with real auth headers against staging
- Pair with protoc for offline schema inspection

## Capabilities

### grpc-reflection
List and describe services via server reflection.

**Parameters:**
- `addr` (string): Server address host:port
- `plaintext` (boolean): Use plaintext instead of TLS
- `symbol` (string): Service or message to describe

**Commands:**
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext localhost:50051 list my.package`
- `grpcurl -plaintext localhost:50051 describe my.package.Greeter`
- `grpcurl -plaintext localhost:50051 describe my.package.HelloRequest`

**Examples:**
- grpcurl -plaintext localhost:50051 list
- grpcurl -plaintext localhost:50051 describe my.package.Greeter
- grpcurl -plaintext localhost:50051 list my.package

### grpc-calls
Invoke unary and streaming RPCs with JSON payloads.

**Parameters:**
- `data` (object): JSON request body
- `header` (string): Metadata header, e.g. authorization: Bearer X
- `maxTime` (number): Request timeout in seconds

**Commands:**
- `grpcurl -plaintext -d '{"name": "world"}' localhost:50051 my.package.Greeter/SayHello`
- `grpcurl -plaintext -d @ localhost:50051 my.package.Chat/Send <<< '{"msg": "hi"}'`
- `grpcurl -plaintext -d '{"id": 1}' -H 'authorization: Bearer TOKEN' localhost:50051 my.package.Users/Get`
- `grpcurl -plaintext -d '{}' -max-time 30 localhost:50051 my.package.Orders/List`

**Examples:**
- grpcurl -plaintext -d '{"name": "world"}' localhost:50051 my.package.Greeter/SayHello
- grpcurl -plaintext -d '{"id": 1}' -H 'authorization: Bearer TOKEN' localhost:50051 my.package.Users/Get
- grpcurl -plaintext -d '{}' -max-time 30 localhost:50051 my.package.Orders/List

### protobuf-imports
Call servers without reflection using proto files.

**Parameters:**
- `importPath` (string): Proto import root
- `proto` (string): Proto file path

**Commands:**
- `grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{"name":"x"}' localhost:50051 hello.Greeter/SayHello`
- `grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{}' localhost:50051 hello.Greeter/SayHello -format json`
- `grpcurl -import-path . -proto api/v1/orders.proto -plaintext localhost:50051 list`

**Examples:**
- grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{"name":"x"}' localhost:50051 hello.Greeter/SayHello
- grpcurl -import-path . -proto api/v1/orders.proto -plaintext localhost:50051 list

## References
- [grpcurl GitHub](https://github.com/fullstorydev/grpcurl)
- [gRPC Documentation](https://grpc.io/docs/)
