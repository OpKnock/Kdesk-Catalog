---
applyTo: "**/*.go **/*.r **/*.sh **/*.{yaml,yml}"
---

Designs gRPC services with protobuf and buf: linting conventions, breaking-change checks, and live server probing with grpcurl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `buf lint`, `grpcurl -plaintext localhost:50051 list`
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

# gRPC Service Design

Design robust gRPC services: proto contracts, conventions, and live testing.

## When to Use

- Defining new service APIs between teams
- Reviewing protobuf changes for compatibility
- Debugging services during development

## Service definition

```proto
syntax = "proto3";
package acme.orders.v1;

service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (stream Order);
}

message GetOrderRequest {
  string id = 1;
}

message Order {
  string id = 1;
  string sku = 2;
  int64 price_cents = 3;
}
```

## Lint and check

```bash
buf lint
buf breaking --against '.git#branch=main,subdir=proto'
```

Never reuse field numbers, never change types in place, and never remove deprecated fields.

## Generate stubs

```yaml
# buf.gen.yaml
version: v2
plugins:
  - local: protoc-gen-go
    out: gen
    opt: paths=source_relative
  - local: protoc-gen-go-grpc
    out: gen
    opt: paths=source_relative
```

```bash
buf generate
```

## Live probing

```bash
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext -d '{"id":"42"}' localhost:50051 acme.orders.v1.OrderService/GetOrder
```

## Best practices

- Version packages in the proto package name (v1, v2).
- Use wrappers/nullable via google.protobuf where truly optional.
- Keep request messages flat; avoid deeply nested option bundles.
- Add comments to every field - they become documentation.

## Testing

Add buf lint and buf breaking to CI, plus grpcurl smoke calls in staging.

## Capabilities

### buf
Lint, format, and check protobuf definitions for breaking changes.

**Parameters:**
- `against` (string): Baseline source to diff for breaking changes
- `path` (string): Subset of files to lint/generate
- `template` (string): buf.gen.yaml generation template

**Commands:**
- `buf lint`
- `buf breaking --against '.git#branch=main,subdir=proto'`
- `buf format -w`
- `buf generate`
- `buf dep update`

**Examples:**
- buf lint proto/ --path proto/acme/v1/order.proto
- buf breaking --against 'https://github.com/acme/api.git#branch=main,subdir=proto' --exclude-imports
- buf generate --template buf.gen.yaml proto/acme/v1

### grpcurl
Probe gRPC servers, list services, and call methods.

**Parameters:**
- `plaintext` (string): Skip TLS for local development
- `import-path` (string): Proto import roots for reflection fallback
- `d` (string): JSON request message

**Commands:**
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext localhost:50051 describe acme.orders.v1.OrderService`
- `grpcurl -plaintext -d '{"id":"42"}' localhost:50051 acme.orders.v1.OrderService/GetOrder`
- `grpcurl -plaintext -import-path proto -proto acme/orders/v1/order.proto localhost:50051 acme.orders.v1.OrderService/ListOrders`
- `grpcurl -plaintext -d '{}' localhost:50051 acme.orders.v1.OrderService/StreamOrders`

**Examples:**
- grpcurl -plaintext localhost:50051 list | grep acme
- grpcurl -plaintext -d '{"id":"42","fields":{"name":true}}' localhost:50051 acme.orders.v1.OrderService/GetOrder
- grpcurl -plaintext -rpc-header 'authorization: Bearer eyJ...' localhost:50051 acme.orders.v1.OrderService/GetOrder -d '{}'

## References
- [Protobuf Docs](https://protobuf.dev/)
- [Buf Docs](https://buf.build/docs/)
- [grpcurl](https://github.com/fullstorydev/grpcurl)
