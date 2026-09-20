# Connectrpc Gateway

Expose ConnectRPC services as REST/HTTP endpoints using buf-based codegen and the Connect gateway pattern, with real curl and buf commands.

## Instructions

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

**Commands:**
- `buf lint`
- `buf breaking --against .git#branch=main`
- `curl -X POST http://localhost:8080/v1/users -H "Content-Type: application/json" -d '{"name":"alice"}'`
- `curl -X GET http://localhost:8080/v1/users/42`

**Examples:**
- buf lint proto && buf build -o image.bin
- curl -i -X DELETE http://localhost:8080/v1/users/42
- curl -s http://localhost:8080/v1/users/42 | jq '.name'