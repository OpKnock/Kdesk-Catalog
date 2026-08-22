---
name: "grpc-gateway"
description: "Expose gRPC services as RESTful JSON APIs using grpc-gateway v2: google.api.http annotations, protoc plugins, and OpenAPI generation."
type: knowledge
triggers: ["grpc-gateway", "gateway-generation"]
---

# Grpc Gateway

Expose gRPC services as RESTful JSON APIs using grpc-gateway v2: google.api.http annotations, protoc plugins, and OpenAPI generation.

## Instructions

# grpc-gateway

Expose gRPC backends as REST/JSON APIs with grpc-gateway v2.

## What this skill does

- Maps REST paths and verbs to gRPC methods via `google.api.http` annotations.
- Generates a standalone gateway binary that reverse-proxies JSON to gRPC.
- Produces OpenAPI (swagger) specs for downstream API consumers.
- Supports query params, request body binding, and custom route patterns.

## When to use

- The same service must serve mobile/web REST clients and internal gRPC clients.
- You want a single source of truth (the proto) for both protocols.
- Generating OpenAPI docs for the API portal without hand-writing them.

## Real commands

```bash
# Install plugins
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway@latest
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@latest

# Generate gateway code + OpenAPI spec
protoc -I . --grpc-gateway_out=logtostderr=true:./gen \
  --openapiv2_out=logtostderr=true:./swagger ./proto/helloworld.proto

# Run the gateway
go run ./gateway

# Call the REST endpoint
curl http://localhost:8080/v1/hello/John
```

## Annotation example

```proto
import "google/api/annotations.proto";

service Greeter {
  rpc SayHello(HelloRequest) returns (HelloReply) {
    option (google.api.http) = {
      get: "/v1/hello/{name}"
      additional_bindings { post: "/v1/greet" body: "*" }
    };
  }
}
```

## Gateway main

```go
mux := runtime.NewServeMux()
opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}
err := pb.RegisterGreeterHandlerFromEndpoint(ctx, mux, "localhost:50051", opts)
http.ListenAndServe(":8080", mux)
```

## Testing

```bash
go run ./gateway &
curl -s http://localhost:8080/v1/hello/World | jq .message
curl -s -X POST http://localhost:8080/v1/greet -d '{"name":"World"}' | jq .message
```

## Best practices

- Use `additional_bindings` when the same RPC deserves GET and POST shapes.
- Return canonical gRPC status codes; the gateway maps them to HTTP codes automatically.
- Regenerate the OpenAPI spec on every contract change and diff it in CI.
- Keep the gateway in a separate binary so gRPC service and gateway scale independently.

## Example exchange

```
User: Add a REST POST /v1/greet to the Greeter service and regenerate.
Agent: Annotate SayHello with additional_bindings, then run protoc --grpc-gateway_out and restart the gateway.
```

## Capabilities

### gateway-generation
Generate REST gateway stubs and OpenAPI specs from protos annotated with google.api.http.

**Commands:**
- `go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway@latest`
- `go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@latest`
- `protoc -I . --grpc-gateway_out=logtostderr=true:./gen ./proto/helloworld.proto`
- `protoc -I . --openapiv2_out=logtostderr=true:./swagger ./proto/helloworld.proto`
- `go run ./gateway`

**Examples:**
- protoc -I . --grpc-gateway_out=logtostderr=true:./gen --go_out=./gen --go-grpc_out=./gen ./proto/helloworld.proto
- curl http://localhost:8080/v1/hello/John
- curl -X POST http://localhost:8080/v1/greet -d '{"name":"John"}'
