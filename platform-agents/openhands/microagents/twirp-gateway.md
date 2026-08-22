---
name: "twirp-gateway"
description: "Exposes Twirp RPC services as plain HTTP/JSON endpoints. Generates Go handlers from protobuf definitions, serves methods at /twirp/<Service>/<Method> with JSON marshaling, and validates gateway behavior including error responses via curl."
type: knowledge
triggers: ["twirp-gateway", "http-gateway"]
---

# Twirp Gateway

Exposes Twirp RPC services as plain HTTP/JSON endpoints. Generates Go handlers from protobuf definitions, serves methods at /twirp/<Service>/<Method> with JSON marshaling, and validates gateway behavior including error responses via curl.

## Instructions

# Twirp Gateway

Hand-crafted skill for exposing Twirp RPCs as plain HTTP/JSON APIs.

## What this skill does

- Generates Twirp handlers from .proto files
- Serves methods at /twirp/Service/Method with JSON
- Tests the JSON gateway with curl, including error paths

## When to use

- Protobuf-defined services without gRPC transport
- Simple JSON APIs where protobuf is the source of truth
- Teaching Twirp routing and error behavior

## Real commands

```bash
# Generate code from the proto
protoc --twirp_out=. --go_out=. --go_opt=paths=source_relative types.proto
twirp --service=Haberdasher --output=generated types.proto

# Build and run
go build -o server ./cmd/server

# Call the JSON gateway
curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": 12}"

# Error path (inches < 0)
curl -s http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": -1}"
```

## Routing

- Path is /twirp/<full.ServiceName>/<Method>
- Content-Type: application/json (or application/protobuf)
- Errors come back as {"code": "invalid_argument", "msg": "..."} with non-200 status

## Testing

```bash
curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": 12}"
curl -s http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{}"
```

## Best practices

- Keep proto as the single contract; generate clients from it
- Document twirp error codes in your API guide
- Enable twirp server hooks to log method latency

## Capabilities

### http-gateway
Serve Twirp RPCs over plain HTTP with JSON

**Commands:**
- `twirp --service=Haberdasher --output=generated types.proto`
- `go build -o server ./cmd/server`
- `curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": 12}"`
- `curl -s http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": -1}"`
- `protoc --twirp_out=. --go_out=. --go_opt=paths=source_relative types.proto`

**Examples:**
- curl -X POST http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{\"inches\": 12}"
- protoc --twirp_out=. --go_out=. types.proto
- curl -s http://localhost:8080/twirp/twirp.example.Haberdasher/MakeHat -H "Content-Type: application/json" -d "{}"
