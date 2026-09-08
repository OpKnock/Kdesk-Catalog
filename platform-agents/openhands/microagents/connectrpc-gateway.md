---
name: "connectrpc-gateway"
description: "Expose ConnectRPC services as REST/HTTP endpoints using buf-based codegen and the Connect gateway pattern, with real curl and buf commands. Use when working with gateway setup, rest routing, api or when the user mentions gateway setup, rest routing, api."
type: knowledge
triggers: ["connectrpc-gateway", "gateway-setup", "rest-routing"]
---

Expose ConnectRPC services as REST/HTTP endpoints using buf-based codegen and the Connect gateway pattern, with real curl and buf commands.

## Agentic Workflow: Read -> Reason -> Act (connectrpc-gateway)

You are **Connectrpc Gateway** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `connectrpc-gateway`
- Domain: Expose ConnectRPC services as REST/HTTP endpoints using buf-based codegen and the Connect gateway pattern, with real curl and buf commands.
- **gateway-setup**: Scaffold a ConnectRPC gateway, generate REST stubs with buf, and serve both Connect and REST on one  — `buf generate --path proto --output gen`
- **rest-routing**: Define HTTP/JSON routes with google.api.http annotations and validate them with buf — `buf lint`
- Check `knowledge` and `prerequisites: buf`

### 2. Reason — think for `connectrpc-gateway`
- For `gateway-setup`: Scaffold a ConnectRPC gateway, generate REST stubs with buf, and serve both Connect and REST on one port — decide which checks to run
- For `rest-routing`: Define HTTP/JSON routes with google.api.http annotations and validate them with buf — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `connectrpc-gateway` tools
- Tools: `Glob`, `Grep`, `Read`, `Buf`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `connectrpc-gateway:2fa4253c`

# ConnectRPC Gateway

Expose a ConnectRPC service as REST/HTTP with annotations and generated stubs.

## When to Use

- Serving Connect and REST/JSON from the same server
- Migrating a gRPC backend to a browser-friendly HTTP API
- Reusing one proto definition for both transports

## Setup

```bash
go mod init example.com/gateway
go get connectrpc.com/connect@latest
go get google.golang.org/protobuf@latest
```

## Annotate the Proto

```proto
import "google/api/annotations.proto";
service UserService {
  rpc GetUser(GetUserRequest) returns (User) {
    option (google.api.http) = {
      get: "/v1/users/{id}"
    };
  }
  rpc CreateUser(CreateUserRequest) returns (User) {
    option (google.api.http) = {
      post: "/v1/users"
      body: "*"
    };
  }
}
```

## Generate and Run

```bash
buf generate --path proto --output gen
go run ./cmd/server &
# Connect JSON over POST
curl -i -H "Content-Type: application/json" \
  -d '{"id":"42"}' \
  http://localhost:8080/connect.example.v1.UserService/GetUser
# REST route from annotations
curl -s http://localhost:8080/v1/users/42 | jq '.name'
```

## Validation

```bash
buf lint
buf breaking --against .git#branch=main
buf build -o image.bin
```

## Testing

```bash
curl -X POST http://localhost:8080/v1/users -H "Content-Type: application/json" -d '{"name":"alice"}'
curl -s http://localhost:8080/v1/users/42 -o /dev/null -w "%{http_code}\n"
```

## Best Practices

- Keep annotations on the proto so both transports share one contract
- Run `buf lint` and `buf breaking` in CI
- Use Connect JSON protocol for browser clients and REST for legacy consumers
- Version REST paths with /v1, /v2

## Capabilities

### gateway-setup
Scaffold a ConnectRPC gateway, generate REST stubs with buf, and serve both Connect and REST on one port

**Parameters:**
- `proto_path` (string): Directory containing .proto files
- `output_dir` (string): Directory where generated code is written

**Commands:**
- `buf generate --path proto --output gen`
- `go get connectrpc.com/connect@latest`
- `go get google.golang.org/protobuf@latest`
- `go run ./cmd/server`

**Examples:**
- buf lint proto && buf generate --path proto --output gen
- go mod init example.com/gateway && go get connectrpc.com/connect@latest
- curl -i -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/connect.example.v1.ExampleService/SayHello

### rest-routing
Define HTTP/JSON routes with google.api.http annotations and validate them with buf

**Parameters:**
- `route` (string): REST path such as /v1/users/{id}
- `method` (string): HTTP verb: GET, POST, PUT, DELETE

**Commands:**
- `buf lint`
- `buf breaking --against .git#branch=main`
- `curl -X POST http://localhost:8080/v1/users -H "Content-Type: application/json" -d '{"name":"alice"}'`
- `curl -X GET http://localhost:8080/v1/users/42`

**Examples:**
- buf lint proto && buf build -o image.bin
- curl -i -X DELETE http://localhost:8080/v1/users/42
- curl -s http://localhost:8080/v1/users/42 | jq '.name'

## References
- [ConnectRPC Gateway Docs](https://connectrpc.com/docs/go/gateway)
- [Buf Build Docs](https://buf.build/docs)
