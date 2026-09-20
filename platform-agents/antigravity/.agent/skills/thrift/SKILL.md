---
name: "thrift"
description: "Compile it IDL to client/server code in many languages. Use when working with thrift codegen, api or when the user mentions thrift codegen, api."
license: "MIT"
compatibility: "Requires thrift."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(thrift:*)"
---

Compile it IDL to client/server code in many languages.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `thrift --version`
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

# Apache Thrift

Hand-crafted skill for cross-language RPC with Apache Thrift.

## What this skill does

- Writes .thrift IDL files with structs, enums, and services
- Generates code for Python, Go, Java, Node, and more
- Runs strict mode to catch ambiguous IDL early

## When to use

- Polyglot teams sharing one RPC contract
- Legacy services already speaking Thrift
- When protobuf/gRPC tooling is not an option

## Real commands

```bash
# Check the compiler
thrift --version

# Python client/server code
thrift --gen py shared.thrift

# Go (include included files with -r)
thrift -r --gen go calculator.thrift

# Java into a specific dir
thrift -r --gen java --out gen/java calculator.thrift

# Node
thrift -r --gen js:node calculator.thrift

# Strict parsing: unknown fields and sloppy includes fail
thrift --gen py -out gen/ --strict calculator.thrift
```

## IDL example

```thrift
namespace py calculator
namespace go calculator

enum Operation {
  ADD = 1,
  SUBTRACT = 2
}

struct Work {
  1: i32 num1,
  2: i32 num2,
  3: Operation op
}

exception InvalidOperation {
  1: i32 code,
  2: string why
}

service Calculator {
  i32 calculate(1: Work w) throws (1: InvalidOperation e),
  oneway void ping()
}
```

## Testing

```bash
thrift -r --gen py calculator.thrift && ls -R gen-py
thrift --gen py --strict calculator.thrift
```

## Best practices

- Keep one .thrift per bounded domain, include shared definitions
- Never renumber fields: wire compatibility depends on IDs
- Generate at build time and pin the thrift compiler version

## Capabilities

### thrift-codegen
Compile Thrift IDL to client/server code in many languages

**Parameters:**
- `language` (string): Target language generator, e.g. py, go, java, cpp
- `idl_file` (string): Input .thrift file
- `out_dir` (string): Output directory with --out

**Commands:**
- `thrift --version`
- `thrift --gen py shared.thrift`
- `thrift -r --gen go calculator.thrift`
- `thrift -r --gen java --out gen/java calculator.thrift`
- `thrift --gen py -out gen/ --strict calculator.thrift`

**Examples:**
- thrift -r --gen go calculator.thrift
- thrift --gen py shared.thrift
- thrift -r --gen js:node calculator.thrift

## References
- [Thrift IDL docs](https://thrift.apache.org/docs/idl)
- [Thrift compiler](https://thrift.apache.org/docs/UsingThrift)
