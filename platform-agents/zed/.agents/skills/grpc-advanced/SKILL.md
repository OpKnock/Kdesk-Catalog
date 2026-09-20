---
name: "grpc-advanced"
description: "Advanced gRPC client workflows: interactive REPL with evans, rich output formats, large-message limits, deadlines, and request streaming from the CLI. Use when working with advanced grpc client, api or when the user mentions advanced grpc client, api."
license: "MIT"
compatibility: "Requires evans, grpcurl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(evans:*) Bash(go:*) Bash(grpcurl:*)"
---

Advanced gRPC client workflows: interactive REPL with evans, rich output formats, large-message limits, deadlines, and request streaming from the CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go install github.com/ktr0731/evans@latest`
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

# gRPC v2 (Advanced Client Workflows)

Interactive and advanced CLI workflows for gRPC services.

## What this skill does

- Explores gRPC services interactively with the evans REPL.
- Calls RPCs with rich formats, large payloads, and deadlines.
- Streams requests from stdin with `grpcurl -d @`.
- Configures keepalive and channel options for flaky networks.

## When to use

- Exploratory debugging of an unfamiliar gRPC API.
- Sending payloads larger than the default 4MB limit.
- Scripting RPC calls from CI with stdin-driven payloads.

## Real commands

```bash
# Install evans REPL client
go install github.com/ktr0731/evans@latest

# Interactive REPL using server reflection
evans --host localhost --port 50051 -r

# One-shot call with a proto file
evans --proto helloworld.proto call helloworld.Greeter.SayHello

# grpcurl with deadlines and bigger message limit
grpcurl -plaintext -max-time 5 -max-msg-sz 4194304 \
  -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello

# Stream a payload from stdin
echo '{"name":"John"}' | grpcurl -plaintext -d @ localhost:50051 mypackage.MyService/SayHello

# Explicit JSON format output
grpcurl -plaintext -format json -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello
```

## evans REPL workflow

```
> package mypackage
mypackage.MyService@localhost:50051> service MyService
mypackage.MyService@localhost:50051> call SayHello
name (TYPE_STRING) => John
```

## Keepalive client (Go)

```go
conn, _ := grpc.NewClient("localhost:50051",
  grpc.WithTransportCredentials(insecure.NewCredentials()),
  grpc.WithKeepaliveParams(keepalive.ClientParameters{Time: 10 * time.Second, Timeout: 3 * time.Second}))
```

## Testing

```bash
# Large-message round trip
dd if=/dev/zero bs=1M count=5 | base64 | tr -d '\n' > big.json
grpcurl -plaintext -max-msg-sz 8388608 -d @ localhost:50051 mypackage.MyService/SayHello < big.json
```

## Best practices

- Raise -max-msg-sz only as far as needed; huge limits hide bugs.
- Use `-d @` with jq to build payloads: `jq -n '{name:"x"}' | grpcurl -d @ ...`.
- For long-running streams, verify keepalive config on both client and server.
- Save evans call history (`history`) to reuse complex RPCs.

## Example exchange

```
User: My RPC fails with RESOURCE_EXHAUSTED on a 5MB upload.
Agent: Raise the client and server limits:
       grpcurl -plaintext -max-msg-sz 8388608 -d @ localhost:50051 mypackage.MyService/Upload
```

## Capabilities

### advanced-grpc-client
Interactively explore and call gRPC services with evans, plus advanced grpcurl flags.

**Parameters:**
- `host` (string): gRPC host for evans/grpcurl, default localhost.
- `port` (integer): gRPC port, default 50051.
- `max_msg_size` (integer): Maximum message size in bytes (grpcurl -max-msg-sz).

**Commands:**
- `go install github.com/ktr0731/evans@latest`
- `evans --host localhost --port 50051 -r`
- `evans --proto helloworld.proto call helloworld.Greeter.SayHello`
- `grpcurl -plaintext -max-time 5 -max-msg-sz 4194304 -d '{"name":"John"}' localhost:50051 mypackage.MyService/SayHello`
- `grpcurl -plaintext -format json -d @ localhost:50051 mypackage.MyService/SayHello`

**Examples:**
- evans --tls --host localhost --port 50051 -r
- echo '{"name":"John"}' | grpcurl -plaintext -d @ localhost:50051 mypackage.MyService/SayHello
- evans --proto hello.proto --host localhost --port 50051

## References
- [evans GitHub](https://github.com/ktr0731/evans)
- [gRPC Keepalive Guide](https://grpc.io/docs/guides/keepalive/)
