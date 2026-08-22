---
name: "Grpc Python"
description: "gRPC services and clients in Python with grpcio and grpcio-tools: python -m grpc_tools.protoc codegen, async/await servers, and interceptors."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Grpc Python

gRPC services and clients in Python with grpcio and grpcio-tools: python -m grpc_tools.protoc codegen, async/await servers, and interceptors.

## Instructions

# gRPC Python

Write and run gRPC services in Python with grpcio and grpcio-tools.

## What this skill does

- Generates Python stubs (_pb2 and _pb2_grpc) from proto files.
- Implements sync (thread-pool) and async (asyncio) gRPC servers.
- Calls RPCs from clients with retries and deadlines.
- Adds interceptors for logging and auth.

## When to use

- A Python service needs typed RPC communication.
- Building data pipelines that fan out gRPC requests.
- Prototyping gRPC services quickly.

## Real commands

```bash
# Install
pip install grpcio grpcio-tools grpcio-health-checking

# Generate stubs
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. helloworld.proto

# Run server and client
python server.py &
python client.py
```

## Server skeleton

```python
import grpc
import helloworld_pb2, helloworld_pb2_grpc

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"Hello {request.name}")

server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
```

## Async server (asyncio)

```python
async def say_hello(request, context):
    return helloworld_pb2.HelloReply(message=f"Hello {request.name}")

server = grpc.aio.server()
helloworld_pb2_grpc.add_GreeterServicer_to_server(servicer, server)
await server.start()
```

## Testing

```bash
python server.py &
grpcurl -plaintext -d '{"name":"Py"}' localhost:50051 helloworld.Greeter/SayHello
python client.py
```

## Best practices

- Run codegen in CI and commit stubs or regenerate on tagged proto versions.
- Use the asyncio API (`grpc.aio`) for concurrent servers; ThreadPoolExecutor blocks under load.
- Set per-call timeouts on the client: `stub.SayHello(req, timeout=5)`.
- Enable grpcio-health-checking and register health status for orchestration.

## Example exchange

```
User: My Python server only handles a few requests concurrently.
Agent: Switch to grpc.aio or increase ThreadPoolExecutor workers:
       grpc.server(grpc.ThreadPoolExecutor(max_workers=32))
```

## Capabilities

### python-grpc
Generate Python stubs with grpc_tools and implement sync or asyncio gRPC servers.

**Commands:**
- `pip install grpcio grpcio-tools`
- `python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. helloworld.proto`
- `python server.py`
- `python client.py`
- `pip install grpcio-health-checking`

**Examples:**
- python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. -I . helloworld.proto
- python server.py & python client.py
- python -m grpc_tools.protoc --help