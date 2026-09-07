---
trigger: glob
description: "Builds Twirp services in Go using protoc code generation. Produces typed server skeletons and client stubs from protobuf definitions, runs the HTTP/JSON gateway, and verifies end-to-end with go test and curl. Use when working with go codegen, api, rpc or when the user mentions go codegen, api, rpc."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

Builds Twirp services in Go using protoc code generation. Produces typed server skeletons and client stubs from protobuf definitions, runs the HTTP/JSON gateway, and verifies end-to-end with go test and curl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `protoc --go_out=. --twirp_out=. --go_opt=paths=source_relati`
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

**Parameters:**
- `proto` (string): Input .proto file
- `package` (string): Go package path for output
- `service` (string): Service name from the proto

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

## References
- [Twirp Go quickstart](https://github.com/twitchtv/twirp/tree/main/example)
- [protoc-gen-twirp plugin](https://github.com/twitchtv/twirp/tree/main/protoc-gen-twirp)
- [Twirp error handling](https://twitchtv.github.io/twirp/docs/errors.html)
