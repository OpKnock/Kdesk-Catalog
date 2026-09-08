---
name: "grpc-go"
description: "gRPC servers and clients in Go: protoc-gen-go codegen, grpc.NewClient channels, interceptors, streaming RPCs, and vet-clean service wiring. Use when working with go grpc server, api or when the user mentions go grpc server, api."
license: "MIT"
compatibility: "Requires protoc."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(go:*) Bash(protoc:*)"
---

gRPC servers and clients in Go: protoc-gen-go codegen, grpc.NewClient channels, interceptors, streaming RPCs, and vet-clean service wiring.

## Agentic Workflow: Read -> Reason -> Act (grpc-go)

You are **Grpc Go** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `grpc-go`
- Domain: gRPC servers and clients in Go: protoc-gen-go codegen, grpc.NewClient channels, interceptors, streaming RPCs, and vet-clean service wiring.
- **go-grpc-server**: Build and run Go gRPC servers with registration, interceptors, and reflection. — `go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest`
- Check `knowledge` and `prerequisites: protoc`

### 2. Reason — think for `grpc-go`
- For `go-grpc-server`: Build and run Go gRPC servers with registration, interceptors, and reflection. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `grpc-go` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Protoc` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `grpc-go:c3303210`

# gRPC Go

Write and run gRPC services in Go using protoc-gen-go-grpc and google.golang.org/grpc.

## What this skill does

- Generates Go gRPC stubs from proto files.
- Implements unary, server-streaming, client-streaming, and bidi-streaming RPCs.
- Wires interceptors for logging, auth, and metrics.
- Runs and debugs servers with grpcurl and reflection.

## When to use

- Building a Go microservice with typed RPC contracts.
- Adding streaming endpoints (logs, live data, uploads).
- Writing Go clients for an existing gRPC API.

## Real commands

```bash
# Install generators
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Generate stubs (paths=source_relative keeps package layout)
protoc -I . --go_out=paths=source_relative:. --go-grpc_out=paths=source_relative:. helloworld.proto

# Build and run
go build ./...
go run ./server &
go run ./client

# Debug with reflection
grpcurl -plaintext localhost:50051 list
```

## Server skeleton

```go
lis, _ := net.Listen("tcp", ":50051")
s := grpc.NewServer(
  grpc.ChainUnaryInterceptor(logInterceptor, authInterceptor),
)
pb.RegisterGreeterServer(s, &server{})
reflection.Register(s)
s.Serve(lis)
```

## Client skeleton

```go
conn, _ := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
defer conn.Close()
client := pb.NewGreeterClient(conn)
resp, err := client.SayHello(ctx, &pb.HelloRequest{Name: "Ada"})
```

## Testing

```bash
go test ./... -race
go run ./server &
grpcurl -plaintext -d '{"name":"Ada"}' localhost:50051 helloworld.Greeter/SayHello
```

## Best practices

- Use `grpc.NewClient` (not deprecated grpc.Dial) with `WithTransportCredentials`.
- Set per-call deadlines with context.WithTimeout on the client side.
- Return `status.Error(codes.X, msg)` instead of plain errors.
- Register reflection in dev so grpcurl can discover services.

## Example exchange

```
User: My Go client hangs calling the Greeter.
Agent: Add a timeout context and check the server address:
       ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
       resp, err := client.SayHello(ctx, &pb.HelloRequest{Name: "Ada"})
```

## Capabilities

### go-grpc-server
Build and run Go gRPC servers with registration, interceptors, and reflection.

**Parameters:**
- `listen_addr` (string): TCP address the server listens on, e.g. :50051.
- `dial_target` (string): Client target address, e.g. localhost:50051.
- `secure` (boolean): Use TLS credentials (true) or insecure credentials (false).

**Commands:**
- `go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest`
- `go get google.golang.org/grpc@latest`
- `protoc -I . --go_out=. --go-grpc_out=. helloworld.proto`
- `go run ./server`
- `go build ./...`

**Examples:**
- go run ./server & grpcurl -plaintext localhost:50051 list
- go test ./...
- go vet ./...

## References
- [gRPC Go Docs](https://grpc.io/docs/languages/go/)
- [grpc-go Reference](https://pkg.go.dev/google.golang.org/grpc)
