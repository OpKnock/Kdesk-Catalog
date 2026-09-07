---
name: "grpc-reflection"
description: "gRPC server reflection: enabling reflection on servers and discovering services, methods, and message schemas at runtime with grpcurl. Use when working with reflection discovery, api or when the user mentions reflection discovery, api."
license: "MIT"
compatibility: "Requires grpcurl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(grpcurl:*)"
---

gRPC server reflection: enabling reflection on servers and discovering services, methods, and message schemas at runtime with grpcurl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `grpcurl -plaintext localhost:50051 list`
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

# gRPC Reflection

Discover and introspect gRPC servers at runtime with server reflection.

## What this skill does

- Lists all services exposed by a gRPC server.
- Describes methods and message schemas without proto files.
- Checks which services are registered (health, reflection itself).
- Enables reflection on Go, Java, Python, and Node servers.

## When to use

- You have a running gRPC server but no proto files locally.
- Verifying that a newly registered service is actually exposed.
- Generating client code by exporting the schema from the live server.

## Real commands

```bash
# List all services
grpcurl -plaintext localhost:50051 list

# List methods of one service
grpcurl -plaintext localhost:50051 list helloworld.Greeter

# Describe a service
grpcurl -plaintext localhost:50051 describe helloworld.Greeter

# Describe a message
grpcurl -plaintext localhost:50051 describe helloworld.HelloRequest

# Describe everything
grpcurl -plaintext localhost:50051 describe

# Check the health service is registered
grpcurl -plaintext localhost:50051 list | grep -i health
```

## Enabling reflection (Go)

```go
import "google.golang.org/grpc/reflection"
reflection.Register(s)  // after pb.RegisterGreeterServer(s, svc)
```

## Enabling reflection (Java)

```java
import io.grpc.services.ReflectionService;
Server server = ServerBuilder.forPort(50051)
    .addService(new GreeterServiceImpl())
    .addService(ReflectionService.newInstance())
    .build();
```

## Enabling reflection (Python)

```python
from grpc_reflection.v1alpha import reflection
from grpc_reflection.v1alpha import reflection_pb2_grpc
reflection.enable_server_reflection(SERVICE_NAMES, server)
```

## Testing

```bash
# Expect 4+ lines: grpc.health.v1.Health, grpc.reflection.v1alpha.ServerReflection, helloworld.Greeter
grpcurl -plaintext localhost:50051 list
```

## Best practices

- Enable reflection in dev and staging; disable in production or gate it behind a flag.
- Use reflection output to validate proto versions match the running binary.
- `grpcurl describe` prints the full schema: pipe it into a protoset export for clients.
- Verify the reflection service itself appears in `list` before debugging clients.

## Example exchange

```
User: I can't find the new OrderService on the running server.
Agent: grpcurl -plaintext localhost:50051 list | grep Order  # if missing, the server binary is stale
```

## Capabilities

### reflection-discovery
Discover services, methods, and message types from a running gRPC server without proto files.

**Parameters:**
- `target` (string): gRPC endpoint host:port, e.g. localhost:50051.
- `symbol` (string): Fully-qualified service, method, or message symbol to describe.
- `use_tls` (boolean): Use TLS (default) or -plaintext for dev.

**Commands:**
- `grpcurl -plaintext localhost:50051 list`
- `grpcurl -plaintext localhost:50051 describe helloworld.Greeter`
- `grpcurl -plaintext localhost:50051 describe helloworld.HelloRequest`
- `grpcurl -plaintext localhost:50051 list helloworld.Greeter`
- `grpcurl -plaintext localhost:50051 describe`

**Examples:**
- grpcurl -plaintext localhost:50051 list | grep -i health
- grpcurl -plaintext localhost:50051 describe helloworld.Greeter.SayHello
- grpcurl -plaintext localhost:50051 list my.package.Service

## References
- [gRPC Server Reflection](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md)
- [grpcurl README](https://github.com/fullstorydev/grpcurl)
