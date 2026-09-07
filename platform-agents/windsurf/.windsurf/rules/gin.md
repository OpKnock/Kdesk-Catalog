---
trigger: glob
description: "Build Go HTTP APIs with the Gin framework: run the server, register middleware, and test handlers. Use when working with gin development, api or when the user mentions gin development, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

Build Go HTTP APIs with the Gin framework: run the server, register middleware, and test handlers.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go get github.com/gin-gonic/gin`
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

# Gin

## What this skill does

Gin is a popular Go web framework with a martini-like API, fast HTTP router, JSON binding/validation, and a middleware chain. This skill covers running, routing, and testing.

## When to use

- Building Go REST APIs quickly
- Teams preferring express-like syntax in Go
- JSON-heavy services with validation needs

## Real commands

```bash
# Get and run
go get github.com/gin-gonic/gin
go run main.go

# Build and test
go build -o server main.go
go test ./... -race -v

# Smoke test
curl -s localhost:8080/api/orders | jq
```

## Minimal app

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    r.GET("/api/orders/:id", func(c *gin.Context) {
        id := c.Param("id")
        if id == "" {
            c.JSON(400, gin.H{"error": "missing id"})
            return
        }
        c.JSON(200, gin.H{"id": id})
    })

    r.Run(":8080")
}
```

## Middleware example

```go
func RequestID() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Header("X-Request-ID", uuid.New().String())
        c.Next()
    }
}
```

## Testing

```go
func TestGetOrder(t *testing.T) {
    router := setupRouter()
    w := httptest.NewRecorder()
    req, _ := http.NewRequest("GET", "/api/orders/1", nil)
    router.ServeHTTP(w, req)
    if w.Code != 200 { t.Fatalf("got %d", w.Code) }
}
```

## Best practices

- Set `GIN_MODE=release` in production; debug mode is slow.
- Use `ShouldBindJSON` with explicit struct tags for validation.
- Register recovery middleware; never let a panic escape.
- Test handlers with httptest against the router, not a live port.
- Keep handlers thin; put logic in services for testability.

## Capabilities

### gin-development
Run Gin apps, add middleware, and test handlers with Go testing.

**Parameters:**
- `port` (integer): Gin listen port
- `mode` (string): GIN_MODE debug/release
- `middleware` (string): logger, recovery, cors, custom

**Commands:**
- `go get github.com/gin-gonic/gin`
- `go run main.go`
- `go build -o server main.go`
- `go test ./... -race -v`
- `curl -s localhost:8080/api/orders | jq`

**Examples:**
- go get github.com/gin-gonic/gin && go run main.go
- go test ./... -race -v
- curl -s localhost:8080/api/orders | jq

## References
- [Gin documentation](https://gin-gonic.com/docs/)
- [Gin GitHub](https://github.com/gin-gonic/gin)
