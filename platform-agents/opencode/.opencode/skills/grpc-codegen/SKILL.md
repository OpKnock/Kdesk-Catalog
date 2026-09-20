---
name: "grpc-codegen"
description: "Generate gRPC service stubs and clients from .proto definitions using protoc, protoc-gen-* plugins, and buf for linting and breaking-change detection. Use when working with proto codegen, api or when the user mentions proto codegen, api."
---

Generate gRPC service stubs and clients from .proto definitions using protoc, protoc-gen-* plugins, and buf for linting and breaking-change detection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `protoc -I . --go_out=paths=source_relative:. --go-grpc_out=p`
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

# gRPC Code Generation

Turn .proto contracts into real client/server code with protoc and buf.

## What this skill does

- Compiles proto files into Go, Java, Python, JS, or C++ gRPC stubs.
- Lints proto schemas against style rules.
- Detects breaking API changes before they ship.
- Formats proto files consistently.

## When to use

- Adding a new RPC service and need generated stubs.
- Changing an existing proto and want to check backwards compatibility.
- Standardizing proto style in a monorepo.

## Real commands

```bash
# Go codegen (protoc-gen-go + protoc-gen-go-grpc)
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
export PATH="$PATH:$(go env GOPATH)/bin"

protoc -I . --go_out=paths=source_relative:. --go-grpc_out=paths=source_relative:. helloworld.proto

# Python codegen
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. helloworld.proto

# buf managed workflow
cat > buf.yaml <<EOF
version: v2
modules:
  - path: proto
EOF

cat > buf.gen.yaml <<EOF
version: v2
plugins:
  - local: protoc-gen-go
    out: gen
    opt: paths=source_relative
  - local: protoc-gen-go-grpc
    out: gen
    opt: paths=source_relative
EOF

buf generate
buf lint
buf breaking --against .git#branch=main
buf format -w
```

## Best practices

- Keep generated files out of git or commit them at a tagged version; pick one and stay consistent.
- Run `buf breaking` in CI before merging any proto change.
- Use source_relative paths for Go so imports match your module layout.
- Name files with underscores (user_service.proto), messages with PascalCase.

## Testing

```bash
buf lint && buf generate && go build ./...
```

## Example exchange

```
User: Regenerate the Go stubs after I added a field to Order.
Agent: buf generate && go build ./...  # stubs regenerated, build green
```

## Capabilities

### proto-codegen
Compile proto files to language stubs, lint schemas, and detect breaking API changes with buf.

**Parameters:**
- `out_dir` (string): Output directory for generated stubs (default .).
- `paths` (string): Module path mode: source_relative or import.
- `proto_file` (string): The .proto file to compile.

**Commands:**
- `protoc -I . --go_out=paths=source_relative:. --go-grpc_out=paths=source_relative:. helloworld.proto`
- `buf generate`
- `buf lint`
- `buf breaking --against .git#branch=main`
- `buf format -w`

**Examples:**
- buf generate --template buf.gen.yaml
- buf lint --error-format=json
- buf breaking --against buf.build/acme/apis:latest

## References
- [protobuf.dev](https://protobuf.dev)
- [Buf Docs](https://buf.build/docs)
