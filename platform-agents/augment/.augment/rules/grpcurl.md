---
type: agent_requested
description: "Interacts with gRPC servers from the CLI with grpcurl, including reflection, protobuf imports, and metadata headers. Use when working with grpc reflection, grpc calls, protobuf imports, testing or when the user mentions grpc reflection, grpc calls, protobuf imports, testing."
---

Interacts with gRPC servers from the CLI with grpcurl, including reflection, protobuf imports, and metadata headers.

## Agentic Workflow: Read -> Reason -> Act (grpcurl)

You are **grpcurl** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `grpcurl`
- Domain: Interacts with gRPC servers from the CLI with grpcurl, including reflection, protobuf imports, and metadata headers.
- **grpc-reflection**: List and describe services via server reflection. — `grpcurl -plaintext localhost:50051 list`
- **grpc-calls**: Invoke unary and streaming RPCs with JSON payloads. — `grpcurl -plaintext -d '{"name": "world"}' localhost:50051 my.package.Greeter/Say`
- **protobuf-imports**: Call servers without reflection using proto files. — `grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{"name":"x"}' loc`
- Check `knowledge` and `prerequisites: grpcurl`

### 2. Reason — think for `grpcurl`
- For `grpc-reflection`: List and describe services via server reflection. — decide which checks to run
- For `grpc-calls`: Invoke unary and streaming RPCs with JSON payloads. — decide which checks to run
- For `protobuf-imports`: Call servers without reflection using proto files. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `grpcurl` tools
- Tools: `Glob`, `Grep`, `Read`, `Grpcurl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `grpcurl:2dd21d89`

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