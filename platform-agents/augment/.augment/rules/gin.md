---
type: agent_requested
description: "Build Go HTTP APIs with the Gin framework: run the server, register middleware, and test handlers. Use when working with gin development, api or when the user mentions gin development, api."
---

Build Go HTTP APIs with the Gin framework: run the server, register middleware, and test handlers.

## Agentic Workflow: Read -> Reason -> Act (gin)

You are **Gin** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gin`
- Domain: Build Go HTTP APIs with the Gin framework: run the server, register middleware, and test handlers.
- **gin-development**: Run Gin apps, add middleware, and test handlers with Go testing. — `go get github.com/gin-gonic/gin`
- Check `knowledge` references before acting

### 2. Reason — think for `gin`
- For `gin-development`: Run Gin apps, add middleware, and test handlers with Go testing. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gin` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gin:c720f994`

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