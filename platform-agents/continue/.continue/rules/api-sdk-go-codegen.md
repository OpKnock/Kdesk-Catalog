---
name: "Api Sdk Go Codegen"
description: "Generates Go SDKs with oapi-codegen: typed clients from OpenAPI, server stubs, config generation, and go test verification."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Api Sdk Go Codegen

Generates Go SDKs with oapi-codegen: typed clients from OpenAPI, server stubs, config generation, and go test verification.

## Instructions

# API SDK v4 - Go

Go SDK generation with oapi-codegen.

## What This Skill Does
- Generates typed Go clients and servers
- Configures generation via YAML
- Validates with go build and tests

## When to Use
- Go services consuming the API
- Generating server stubs for parity
- Typed client SDKs

## Real Commands

```bash
go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest
oapi-codegen -package api -generate types,client -o client.gen.go openapi.yaml
go build ./...
go test ./...
```

## Config File

```yaml
package: api
output: gen/client.gen.go
generate:
  client: true
  models: true
  chi-server: true
```

## Testing
- Compile after regeneration
- Test client calls with httptest servers
- Run go vet in CI

## Best Practices
- Commit generated files with release tags
- Keep generation config in the repo
- Regenerate before each release

## Capabilities

### go-codegen
Generate Go client code from OpenAPI

**Commands:**
- `go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest`
- `oapi-codegen -package api -generate types,client -o client.gen.go openapi.yaml`
- `oapi-codegen -package api -generate types,chi-server -o server.gen.go openapi.yaml`
- `oapi-codegen -config oapi-codegen.yaml openapi.yaml`
- `go build ./...`

**Examples:**
- -generate types,client emits a typed Go client
- -generate chi-server emits a server stub
- -config uses a YAML config file

### go-testing
Test the generated Go client

**Commands:**
- `go test ./...`
- `go vet ./...`
- `go mod tidy`
- `go test -race ./...`

**Examples:**
- -cli --help
- -api --help