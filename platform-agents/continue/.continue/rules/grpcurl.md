---
name: "grpcurl"
description: "Interacts with gRPC servers from the CLI with grpcurl, including reflection, protobuf imports, and metadata headers."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# grpcurl

Interacts with gRPC servers from the CLI with grpcurl, including reflection, protobuf imports, and metadata headers.

## Instructions

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

**Commands:**
- `grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{"name":"x"}' localhost:50051 hello.Greeter/SayHello`
- `grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{}' localhost:50051 hello.Greeter/SayHello -format json`
- `grpcurl -import-path . -proto api/v1/orders.proto -plaintext localhost:50051 list`

**Examples:**
- grpcurl -import-path ./proto -proto hello.proto -plaintext -d '{"name":"x"}' localhost:50051 hello.Greeter/SayHello
- grpcurl -import-path . -proto api/v1/orders.proto -plaintext localhost:50051 list