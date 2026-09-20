# Twirp Go

Builds Twirp services in Go using protoc code generation. Produces typed server skeletons and client stubs from protobuf definitions, runs the HTTP/JSON gateway, and verifies end-to-end with go test and curl.

## Instructions

# Twirp Go

Hand-crafted skill for building Twirp services in Go.

## What this skill does

- Generates Go + Twirp bindings from protos
- Produces a server skeleton and typed clients
- Runs the server and tests locally

## When to use

- Go services with protobuf contracts
- RPC clients that must stay dependency-light
- Migrating from net/rpc or raw JSON to protobuf

## Real commands

```bash
# Generate Go and Twirp code
protoc --go_out=. --twirp_out=. --go_opt=paths=source_relative types.proto

# Fetch the runtime
go get github.com/twitchtv/twirp

# Generate via go:generate if annotated
go generate ./...

# Build, run, test
go run ./cmd/server
go test ./...
```

## Server skeleton

```go
type server struct{}

func (s *server) MakeHat(ctx context.Context, size *twirp.example.Size) (*twirp.example.Hat, error) {
  if size.Inches <= 0 {
    return nil, twirp.InvalidArgumentError("inches", "must be positive")
  }
  return &twirp.example.Hat{Inches: size.Inches}, nil
}

func main() {
  handler := twirp.example.NewHaberdasherServer(&server{})
  http.ListenAndServe(":8080", handler)
}
```

## Client

```go
client := twirp.example.NewHaberdasherClient("http://localhost:8080", http.DefaultClient)
hat, err := client.MakeHat(ctx, &twirp.example.Size{Inches: 12})
```

## Testing

```bash
go run ./cmd/server &
curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H 'Content-Type: application/json' -d '{"inches": 12}'
go test ./...
```

## Best practices

- Keep proto-generated files out of manual editing
- Return typed twirp errors from handlers
- Test client and server together in integration tests

## Capabilities

### go-codegen
Generate Twirp Go code and call the service

**Commands:**
- `protoc --go_out=. --twirp_out=. --go_opt=paths=source_relative types.proto`
- `go get github.com/twitchtv/twirp`
- `go generate ./...`
- `go run ./cmd/server`
- `go test ./...`

**Examples:**
- protoc --go_out=. --twirp_out=. types.proto
- go run ./cmd/server
- go test ./...
