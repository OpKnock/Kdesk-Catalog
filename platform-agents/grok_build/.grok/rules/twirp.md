Implements RPC services using the Twirp framework with protobuf contracts. Defines services in proto3, serves methods over HTTP/JSON and protobuf, handles Twirp error codes, and verifies behavior with curl and Go tests.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `protoc --twirp_out=. --go_out=. types.proto`
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

# Twirp

Hand-crafted skill for the Twirp RPC framework.

## What this skill does

- Defines RPC contracts in proto3
- Serves methods over HTTP/JSON and protobuf
- Explains Twirp error codes and how to surface them
- Verifies behavior with curl and Go tests

## When to use

- Choosing or onboarding onto Twirp
- Debugging a 404 on an RPC route
- Enforcing error code conventions across services

## Real commands

```bash
# Generate code
protoc --twirp_out=. --go_out=. types.proto

# Happy path
curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H 'Content-Type: application/json' -d '{"inches": 12}'

# Inspect the full response for errors
curl -i -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H 'Content-Type: application/json' -d '{"inches": -1}'

# Run the suite
go test ./...
```

## Route and error rules

- Route: /twirp/<service>/<method>, POST only
- Errors: {"code": "...", "msg": "...", "meta": {...}} with proper HTTP status
- 404 usually means the route or service name is wrong

## Proto contract

```proto
syntax = "proto3";
package twirp.example;

message Size { int32 inches = 1; }
message Hat { int32 inches = 1; string color = 2; }

service Haberdasher {
  rpc MakeHat(Size) returns (Hat);
}
```

## Testing

```bash
curl -i -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H 'Content-Type: application/json' -d '{"inches": -1}'
go test ./...
```

## Best practices

- Model errors in the proto contract where possible
- Use invalid_argument for bad input, internal for bugs
- Keep routes predictable: service names must match exactly

## Capabilities

### twirp-basics
Design contracts, serve RPCs, and debug Twirp errors

**Parameters:**
- `method` (string): Twirp method name
- `body` (string): JSON payload
- `service` (string): Service package

**Commands:**
- `protoc --twirp_out=. --go_out=. types.proto`
- `curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": 12}"`
- `curl -i -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": -1}"`
- `go test ./...`
- `protoc --version`

**Examples:**
- curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -d "{\"inches\": 12}" -H "Content-Type: application/json"
- curl -i -s http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -d "{}" -H "Content-Type: application/json"
- go test ./...

## References
- [Twirp official docs](https://twitchtv.github.io/twirp/docs/intro.html)
- [Twirp errors spec](https://twitchtv.github.io/twirp/docs/errors.html)
- [Twirp Go reference](https://github.com/twitchtv/twirp)