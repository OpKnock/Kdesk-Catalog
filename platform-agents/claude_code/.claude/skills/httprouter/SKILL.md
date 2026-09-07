---
name: "httprouter"
description: "Go httprouter: radix-tree routing with typed path params, method handlers, middleware wrapping, and benchmark-grade request dispatch. Use when working with httprouter routing, api or when the user mentions httprouter routing, api."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(go:*)"
---

Go httprouter: radix-tree routing with typed path params, method handlers, middleware wrapping, and benchmark-grade request dispatch.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go get github.com/julienschmidt/httprouter@latest`
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

# httprouter

High-performance radix-tree routing for Go.

## What this skill does
45:   
- Registers typed routes with :param path segments.
- Dispatches by HTTP method automatically.
46:   - Wraps handlers with middleware the standard library way.
- Serves 404/405 with method-specific handling.
47:   
## When to use

- A Go service needs fast routing without framework weight.
- You want explicit48:    path parameters instead of string parsing.
- Serving REST endpoints with clean method separation.
49:   
## Real commands

```bash
# Install
go get github.com/julienschmidt/httprouter@latest

# Build,50:    vet, test
go build -o app .
go vet ./...
go test ./...

# Run and hit a param route
go run .51:    &
curl -X GET http://localhost:8080/users/42
```

## Router setup

```go
package main

import52:    (
    "fmt"
    "net/http"
    "github.com/julienschmidt/httprouter"
)

func Hello(w http.ResponseWriter,53:    r *http.Request, ps httprouter.Params) {
    fmt.Fprintf(w, "hello, %s!", ps.ByName("name"))
54:   }

func main() {
    router := httprouter.New()
    router.GET("/hello/:name", Hello)
    router.POST("55:   /users", CreateUser)
    router.PUT("/users/:id", UpdateUser)
    router.DELETE("/users/:id"56:   , DeleteUser)
    http.ListenAndServe(":8080", router)
}
```

## Middleware wrapper

```go
57:   func logging(next httprouter.Handle) httprouter.Handle {
    return func(w http.ResponseWriter, r *http.Request,58:    ps httprouter.Params) {
        log.Printf("%s %s", r.Method, r.URL.Path)
        next(w, r, ps)
59:       }
}

router.GET("/users/:id", logging(GetUser))
```

## Testing

```bash
curl -s http://localhost:8080/hello/world
60:   go test -bench=. -benchmem ./...
```

## Best practices

- Path params are matched in a single61:    segment; use `:name` not `*` for required parts.
- Wrap handlers with standard `func(http.Handler,62:    ...) http.Handler` style for reuse.
- Set `router.RedirectTrailingSlash = true` consciously; it can63:    surprise clients.
- Keep handlers httprouter.Handle-typed to use Params without globals.

## Example64:    exchange

```
User: Add a GET /users/:id route.
Agent: router.GET("/users/:id", func(w, r, ps)65:    { id := ps.ByName("id") ... })
```

## Capabilities

### httprouter-routing
Build typed HTTP routes with httprouter and wrap handlers with middleware.

**Parameters:**
- `path` (string): Route pattern, e.g. /users/:id.
- `method` (string): HTTP method to register.
- `port` (integer): Listen port, default 8080.

**Commands:**
- `go get github.com/julienschmidt/httprouter@latest`
- `go build -o app .`
- `go test ./...`
- `go vet ./...`
- `curl -X GET http://localhost:8080/users/42`

**Examples:**
- go run . & curl -s http://localhost:8080/hello/world
- go test -bench=. -benchmem ./...
- curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/users/42

## References
- [httprouter GitHub](https://github.com/julienschmidt/httprouter)
- [Go net/http docs](https://pkg.go.dev/net/http)
