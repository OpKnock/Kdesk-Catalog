---
trigger: glob
description: "Develop modern RPC services with ConnectRPC: protocol choice, buf codegen, and calling services from Go and browsers. Use when working with proto codegen, protocol calls, api or when the user mentions proto codegen, protocol calls, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Develop modern RPC services with ConnectRPC: protocol choice, buf codegen, and calling services from Go and browsers.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `buf lint`, `curl -H "Content-Type: application/json" -d '{"name":"alice"`
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
