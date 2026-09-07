---
name: "grpc-rust"
description: "gRPC services and clients in Rust with tonic: tonic-build codegen from protos, Prost message types, and tower-based interceptors. Use when working with rust grpc tonic, api or when the user mentions rust grpc tonic, api."
license: "MIT"
compatibility: "Requires cargo."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(cargo:*)"
---

gRPC services and clients in Rust with tonic: tonic-build codegen from protos, Prost message types, and tower-based interceptors.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cargo add tonic tonic-prost prost`
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

**Parameters:**
- `proto_dir` (string): Directory containing .proto files for tonic-build.
- `grpc_port` (integer): Server listen port, default 50051.
- `crate_type` (string): bin or lib crate layout for generated code.

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

## References
- [tonic docs.rs](https://docs.rs/tonic)
- [tonic GitHub](https://github.com/hyperium/tonic)
