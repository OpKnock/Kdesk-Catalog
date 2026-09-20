---
name: "connectrpc"
description: "Develop modern RPC services with ConnectRPC: protocol choice, buf codegen, and calling services from Go and browsers."
type: knowledge
triggers: ["connectrpc", "proto-codegen", "protocol-calls"]
---

# Connectrpc

Develop modern RPC services with ConnectRPC: protocol choice, buf codegen, and calling services from Go and browsers.

## Instructions

# ConnectRPC

Develop modern RPC services with the Connect protocol.

## When to Use

- New services needing gRPC interop plus JSON for browsers
- Replacing REST with typed, generated RPC
- Streaming without the complexity of raw gRPC

## Setup

```bash
go mod init example.com/rpc
go get connectrpc.com/connect@latest
go get google.golang.org/protobuf@latest
```

## Proto

```proto
syntax = "proto3";
package example.v1;

service GreetService {
  rpc Greet(GreetRequest) returns (GreetResponse);
}
```

## buf.gen.yaml

```yaml
version: v2
plugins:
  - local: protoc-gen-go
    out: gen
  - local: protoc-gen-connect-go
    out: gen
```

## Generate and Serve

```bash
buf lint
buf generate
buf breaking --against .git#branch=main
go run ./cmd/server
```

## Call from Three Protocols

```bash
# Connect JSON
curl -H "Content-Type: application/json" -d '{"name":"alice"}' \
  http://localhost:8080/example.v1.GreetService/Greet

# gRPC (grpcurl)
grpcurl -plaintext -d '{"name":"alice"}' localhost:8080 example.v1.GreetService/Greet

# gRPC-Web via browser transport
```

## Testing

```bash
go test ./...
grpcurl -plaintext localhost:8080 list
curl -s -o /dev/null -w "%{http_code}\n" -H "Content-Type: application/json" -d '{}' http://localhost:8080/example.v1.GreetService/Greet
```

## Best Practices

- Prefer Connect protocol for browser and mobile clients
- Run buf lint and buf breaking in CI
- Use one proto as the single source of truth
- Version the package in the proto namespace
- Add interceptors for auth, logging, and metrics
- Check health with connect grpchealth

## Capabilities

### proto-codegen
Lint, generate, and manage protobuf with buf for ConnectRPC projects

**Commands:**
- `buf lint`
- `buf generate`
- `buf breaking --against .git#branch=main`
- `buf export --output gen`

**Examples:**
- buf lint proto && buf generate proto
- buf breaking --against .git#branch=main
- buf export --output gen && ls gen

### protocol-calls
Call ConnectRPC services over Connect, gRPC, and gRPC-Web protocols

**Commands:**
- `curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.v1.GreetService/Greet`
- `curl -H "Content-Type: application/proto" --data-binary @req.bin http://localhost:8080/example.v1.GreetService/Greet`
- `grpcurl -plaintext -d '{"name":"alice"}' localhost:8080 example.v1.GreetService/Greet`
- `grpcurl -plaintext localhost:8080 list`

**Examples:**
- curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.v1.GreetService/Greet
- grpcurl -plaintext localhost:8080 list
- grpcurl -plaintext -d '{}' localhost:8080 example.v1.GreetService/Greet
