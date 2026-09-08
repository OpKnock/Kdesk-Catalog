Build ConnectRPC services in Go: protobuf codegen with buf, connect handlers, and HTTP/JSON serving.

## Agentic Workflow: Read -> Reason -> Act (connectrpc-go)

You are **Connectrpc Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `connectrpc-go`
- Domain: Build ConnectRPC services in Go: protobuf codegen with buf, connect handlers, and HTTP/JSON serving.
- **go-scaffold**: Scaffold a Go ConnectRPC project, generate code from proto, and run the server — `go mod init github.com/acme/connectrpc-service`
- **handlers-testing**: Implement Connect handlers and test with curl and go test — `curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:`
- Check `knowledge` and `prerequisites: buf`

### 2. Reason — think for `connectrpc-go`
- For `go-scaffold`: Scaffold a Go ConnectRPC project, generate code from proto, and run the server — decide which checks to run
- For `handlers-testing`: Implement Connect handlers and test with curl and go test — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `connectrpc-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Buf` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `connectrpc-go:fafb126d`

# ConnectRPC Go

Build modern RPC services in Go with ConnectRPC.

## When to Use

- New gRPC-compatible services with simpler protocol handling
- Services consumed by web, mobile, and gRPC clients
- Replacing hand-written REST handlers with generated code

## Scaffold

```bash
go mod init github.com/acme/connectrpc-service
go get connectrpc.com/connect@latest
go get google.golang.org/protobuf@latest
```

## Proto

```proto
syntax = "proto3";
package example.connectrpc.v1;

message GreetRequest { string name = 1; }
message GreetResponse { string greeting = 1; }

service GreetService {
  rpc Greet(GreetRequest) returns (GreetResponse);
}
```

## Generate and Serve

```bash
buf generate
```

```go
package main

import (
  "net/http"
  "connectrpc.com/connect"
  greetv1 "github.com/acme/connectrpc-service/gen/greet/v1"
  "github.com/acme/connectrpc-service/gen/greet/v1/greetv1connect"
)

type GreetServer struct{}

func (s *GreetServer) Greet(ctx context.Context, req *connect.Request[greetv1.GreetRequest]) (*connect.Response[greetv1.GreetResponse], error) {
  msg := "Hello, " + req.Msg.Name
  return connect.NewResponse(&greetv1.GreetResponse{Greeting: msg}), nil
}

func main() {
  mux := http.NewServeMux()
  mux.Handle(greetv1connect.NewGreetServiceHandler(&GreetServer{}))
  http.ListenAndServe("localhost:8080", mux)
}
```

```bash
go run ./cmd/server &
curl -H "Content-Type: application/json" -d '{"name":"alice"}' \
  http://localhost:8080/example.connectrpc.v1.GreetService/Greet
```

## Testing

```bash
go test ./...
go build ./...
go vet ./...
```

## Best Practices

- Use buf lint and buf breaking in CI
- Keep handlers thin; put logic in services
- Use connect options for interceptors such as logging and auth
- Set Content-Type application/json for JSON calls
- Always pass context through the stack

## Capabilities

### go-scaffold
Scaffold a Go ConnectRPC project, generate code from proto, and run the server

**Parameters:**
- `module` (string): Go module path such as github.com/acme/connectrpc-service

**Commands:**
- `go mod init github.com/acme/connectrpc-service`
- `go get connectrpc.com/connect@latest`
- `go get google.golang.org/protobuf@latest`
- `buf generate`
- `go run ./cmd/server`

**Examples:**
- go mod init github.com/acme/connectrpc-service && go get connectrpc.com/connect@latest
- buf generate && go run ./cmd/server
- go build ./... && go vet ./...

### handlers-testing
Implement Connect handlers and test with curl and go test

**Parameters:**
- `service_path` (string): Connect service path, e.g. example.connectrpc.v1.GreetService/Greet

**Commands:**
- `curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.connectrpc.v1.GreetService/Greet`
- `curl -s -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.connectrpc.v1.GreetService/Greet | jq '.greeting'`
- `go test ./...`
- `curl -s -o /dev/null -w "%{http_code}" -H "Content-Type: application/json" -d '{}' http://localhost:8080/example.connectrpc.v1.GreetService/Greet`

**Examples:**
- curl -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.connectrpc.v1.GreetService/Greet
- go test -v ./...
- curl -s -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:8080/example.connectrpc.v1.GreetService/Greet

## References
- [ConnectRPC Go Getting Started](https://connectrpc.com/docs/go/getting-started)
- [Buf CLI Docs](https://buf.build/docs/)
