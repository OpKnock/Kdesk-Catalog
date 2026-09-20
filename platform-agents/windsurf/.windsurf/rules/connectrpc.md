---
trigger: glob
description: "Develop modern RPC services with ConnectRPC: protocol choice, buf codegen, and calling services from Go and browsers. Use when working with proto codegen, protocol calls, api or when the user mentions proto codegen, protocol calls, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Develop modern RPC services with ConnectRPC: protocol choice, buf codegen, and calling services from Go and browsers.

## Agentic Workflow: Read -> Reason -> Act (connectrpc)

You are **Connectrpc** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `connectrpc`
- Domain: Develop modern RPC services with ConnectRPC: protocol choice, buf codegen, and calling services from Go and browsers.
- **proto-codegen**: Lint, generate, and manage protobuf with buf for ConnectRPC projects — `buf lint`
- **protocol-calls**: Call ConnectRPC services over Connect, gRPC, and gRPC-Web protocols — `curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:`
- Check `knowledge` and `prerequisites: buf, grpcurl`

### 2. Reason — think for `connectrpc`
- For `proto-codegen`: Lint, generate, and manage protobuf with buf for ConnectRPC projects — decide which checks to run
- For `protocol-calls`: Call ConnectRPC services over Connect, gRPC, and gRPC-Web protocols — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `connectrpc` tools
- Tools: `Glob`, `Grep`, `Read`, `Buf`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `connectrpc:f492cac9`

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

**Parameters:**
- `proto_dir` (string): Directory of proto files
- `output_dir` (string): Generation output directory

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

**Parameters:**
- `service_fqrn` (string): Fully qualified RPC path such as example.v1.GreetService/Greet
- `content_type` (string): application/json, application/proto, application/connect+proto

**Commands:**
- `curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.v1.GreetService/Greet`
- `curl -H "Content-Type: application/proto" --data-binary @req.bin http://localhost:8080/example.v1.GreetService/Greet`
- `grpcurl -plaintext -d '{"name":"alice"}' localhost:8080 example.v1.GreetService/Greet`
- `grpcurl -plaintext localhost:8080 list`

**Examples:**
- curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.v1.GreetService/Greet
- grpcurl -plaintext localhost:8080 list
- grpcurl -plaintext -d '{}' localhost:8080 example.v1.GreetService/Greet

## References
- [ConnectRPC Docs](https://connectrpc.com/docs/)
- [buf Docs](https://buf.build/docs/)
