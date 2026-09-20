# gRPC API Agent

Develops gRPC services from protobuf definitions. Generates language-specific stubs with protoc and buf, validates service contracts, and debugs live RPCs with grpcurl and grpc_health_probe.

## Instructions

# gRPC API Agent

## What this agent does

Handles the complete gRPC development workflow: authoring .proto contracts, generating typed stubs
with buf and protoc, validating for breaking changes, and debugging live services with grpcurl and
grpc_health_probe. Supports Go, Python, Java, TypeScript, C#, and other gRPC-supported languages.

## When to use

- Defining new gRPC service contracts or evolving existing ones
- Generating client/server code for a target language
- Debugging RPC failures, inspecting message shapes, or verifying health endpoints
- Enforcing protobuf style and breaking-change policy in CI
- Setting up gRPC gateway (REST/JSON transcoding) for browser clients

## Real commands

```bash
# Generate code with buf
buf generate ./proto
buf lint ./proto
buf breaking ./proto --against=.git#branch=main

# Generate with protoc directly
protoc --proto_path=./proto --go_out=. --go-grpc_out=. ./proto/user.proto
protoc --proto_path=./proto --python_out=. --grpc_python_out=. ./proto/user.proto

# Inspect running service
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe UserService
grpcurl -plaintext -d '{"name": "John"}' localhost:50051 UserService/CreateUser

# Health checks
grpc_health_probe -addr=localhost:50051
grpc_health_probe -addr=localhost:50051 -service=UserService
```

## Protobuf example

```protobuf
syntax = "proto3";
package user.v1;

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message CreateUserResponse {
  User user = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  int64 created_at = 4;
}
```

## buf.yaml example

```yaml
version: v2
modules:
  - path: proto
lint:
  use:
    - DEFAULT
  except:
    - PACKAGE_VERSION_SUFFIX
breaking:
  use:
    - FILE
```

## Testing

- Run `buf lint` and `buf breaking` in CI on every proto change
- Test generated stubs compile: `go build ./...` or `python -m py_compile`
- Exercise RPCs with `grpcurl` in integration tests
- Verify health endpoint responds SERVING for all services

## Best practices

- Use buf for linting and breaking-change detection; it's faster and more consistent than protoc
- Organize protos in versioned packages (user.v1, user.v2)
- Enable reflection only in non-production or with auth
- Use gRPC gateway for REST/JSON compatibility
- Implement interceptors for logging, auth, and tracing

## Capabilities

### protobuf-codegen
Generates gRPC client and server stubs from .proto files using protoc and buf.

**Commands:**
- `buf generate protobuf/`
- `protoc --proto_path=protobuf --go_out=. --go-grpc_out=. protobuf/service.proto`
- `protoc --proto_path=protobuf --python_out=. --grpc_python_out=. protobuf/service.proto`
- `buf lint protobuf/`
- `buf breaking protobuf/ --against=.git#branch=main`

**Examples:**
- buf generate ./proto
- buf lint ./proto
- buf breaking ./proto --against=.git#branch=main
- protoc --proto_path=./proto --go_out=. --go-grpc_out=. ./proto/user.proto

### service-inspection
Lists services, methods, and message schemas from a running gRPC server via reflection.

**Commands:**
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext localhost:50051 describe UserService`
- `grpcurl -plaintext localhost:50051 describe .UserService.CreateUser`
- `grpcurl -plaintext -d '{"name": "John"}' localhost:50051 UserService/CreateUser`

**Examples:**
- grpcurl -plaintext localhost:50051 list
- grpcurl -plaintext localhost:50051 describe UserService
- grpcurl -plaintext -d '{"name": "John", "email": "john@example.com"}' localhost:50051 UserService/CreateUser

### health-checking
Probes gRPC health checking endpoint for liveness and readiness.

**Commands:**
- `grpc_health_probe -addr=localhost:50051`
- `grpc_health_probe -addr=localhost:50051 -service=UserService`
- `grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check`

**Examples:**
- grpc_health_probe -addr=localhost:50051
- grpc_health_probe -addr=localhost:50051 -service=UserService
- grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check