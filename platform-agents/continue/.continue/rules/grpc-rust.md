---
name: "Grpc Rust"
description: "gRPC services and clients in Rust with tonic: tonic-build codegen from protos, Prost message types, and tower-based interceptors."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh"]
alwaysApply: false
---

# Grpc Rust

gRPC services and clients in Rust with tonic: tonic-build codegen from protos, Prost message types, and tower-based interceptors.

## Instructions

# gRPC Rust

gRPC services and clients in Rust with the tonic framework.

## What this skill does

- Compiles .proto files to Rust at build time with tonic-build.
- Runs async servers with tokio and tower service layers.
- Generates typed clients with tonic::client::Grpc.
- Supports TLS via rustls and interceptors via tower.

## When to use

- A high-throughput Rust service needs typed RPC contracts.
- Adding streaming RPCs to an async Rust codebase.
- Integrating with gRPC services from other languages.

## Real commands

```bash
# Add dependencies
cargo add tonic tonic-prost prost
cargo add --build tonic-build
cargo add tokio --features macros,rt-multi-thread

# Generate and build (build.rs runs protoc via tonic-build)
cargo build

# Run server binary and probe
cargo run --bin server &
grpcurl -plaintext localhost:50051 list

# Lint and test
cargo clippy -- -D warnings
cargo test
```

## build.rs

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("proto/helloworld.proto")?;
    Ok(())
}
```

## Server skeleton

```rust
use tonic::{transport::Server, Request, Response, Status};
use helloworld::{greeter_server::{Greeter, GreeterServer}, HelloReply, HelloRequest};

#[derive(Default)]
pub struct MyGreeter;

#[tonic::async_trait]
impl Greeter for MyGreeter {
    async fn say_hello(&self, request: Request<HelloRequest>) -> Result<Response<HelloReply>, Status> {
        Ok(Response::new(HelloReply { message: format!("Hello {}", request.into_inner().name) }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    Server::builder().add_service(GreeterServer::new(MyGreeter)).serve(addr).await?;
    Ok(())
}
```

## Testing

```bash
cargo test
cargo run --bin server &
grpcurl -plaintext -d '{"name":"Rust"}' localhost:50051 helloworld.Greeter/SayHello
```

## Best practices

- Commit generated code or regenerate deterministically; tonic-build output lives in OUT_DIR.
- Keep proto_paths minimal in build.rs to reduce rebuild churn.
- Use tonic's tower layers for auth/logging instead of hand-rolled middleware.
- Match tonic/prost versions to avoid codegen incompatibilities.

## Example exchange

```
User: The build fails with "protoc not found".
Agent: Install protoc (apt install protobuf-compiler) or set PROTOC env var to the binary.
```

## Capabilities

### rust-grpc-tonic
Generate tonic stubs from protos at build time and run async gRPC servers.

**Commands:**
- `cargo add tonic tonic-prost prost`
- `cargo add --build tonic-build`
- `cargo build`
- `cargo run --bin server`
- `cargo test`

**Examples:**
- cargo add tokio --features macros,rt-multi-thread
- cargo run --bin server & grpcurl -plaintext localhost:50051 list
- cargo clippy -- -D warnings