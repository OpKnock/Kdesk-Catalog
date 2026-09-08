---
name: "Chi"
description: "Build Go HTTP APIs with the chi router: routing, middleware, URL params, and subrouters. Use when working with chi routing, chi testing, api or when the user mentions chi routing, chi testing, api."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Build Go HTTP APIs with the chi router: routing, middleware, URL params, and subrouters.

## Agentic Workflow: Read -> Reason -> Act (chi)

You are **Chi** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `chi`
- Domain: Build Go HTTP APIs with the chi router: routing, middleware, URL params, and subrouters.
- **chi-routing**: Create chi routers with groups, middleware, and path parameters — `go get github.com/go-chi/chi/v5`
- **chi-testing**: Test chi handlers and verify responses with curl — `go test ./...`
- Check `knowledge` references before acting

### 2. Reason — think for `chi`
- For `chi-routing`: Create chi routers with groups, middleware, and path parameters — decide which checks to run
- For `chi-testing`: Test chi handlers and verify responses with curl — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `chi` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `chi:7f254ce5`

# Chi Router

Build lightweight Go HTTP APIs with chi.

## When to Use

- Go services needing a simple, composable router
- REST APIs with path parameters and middleware
- Adding CORS, logging, and request IDs without a framework

## Setup

```bash
go mod init example.com/api
go get github.com/go-chi/chi/v5
go get github.com/go-chi/cors
```

## Basic Server

```go
package main

import (
  "net/http"
  "github.com/go-chi/chi/v5"
  "github.com/go-chi/chi/v5/middleware"
)

func main() {
  r := chi.NewRouter()
  r.Use(middleware.Logger)
  r.Use(middleware.Recoverer)

  r.Get("/health", func(w http.ResponseWriter, req *http.Request) {
    w.Write([]byte("ok"))
  })

  r.Route("/api", func(r chi.Router) {
    r.Get("/users", listUsers)
    r.Get("/users/{id}", getUser)
    r.Post("/users", createUser)
  })

  http.ListenAndServe(":3000", r)
}
```

## Path Parameters

```go
func getUser(w http.ResponseWriter, req *http.Request) {
  id := chi.URLParam(req, "id")
  w.Write([]byte(id))
}
```

## Run and Test

```bash
go run main.go &
curl -i http://localhost:3000/api/users
curl -s http://localhost:3000/api/users/42
curl -s -X POST -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:3000/api/users
```

## Testing

```bash
go test -v ./...
go test -race ./...
go vet ./...
```

## Best Practices

- Use r.Route groups to namespace endpoints
- Add middleware early: Logger, Recoverer, Timeout, RealIP
- Validate JSON bodies and return proper 400s
- Use chi.URLParam for path params
- Keep handlers small and unit-testable

## Capabilities

### chi-routing
Create chi routers with groups, middleware, and path parameters

**Parameters:**
- `route` (string): Route pattern such as /api/users/{id}

**Commands:**
- `go get github.com/go-chi/chi/v5`
- `go get github.com/go-chi/cors`
- `go run main.go`
- `go build ./...`

**Examples:**
- go get github.com/go-chi/chi/v5 && go run main.go
- go mod tidy && go build ./...
- go test -v ./...

### chi-testing
Test chi handlers and verify responses with curl

**Parameters:**
- `port` (string): Server listen port, default 3000

**Commands:**
- `go test ./...`
- `curl -i http://localhost:3000/api/users`
- `curl -s http://localhost:3000/api/users/42`
- `curl -s -X POST -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:3000/api/users`

**Examples:**
- curl -s http://localhost:3000/api/users | jq '.[0].name'
- curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:3000/api/users
- go test -race ./...

## References
- [chi GitHub Repo](https://github.com/go-chi/chi)
- [chi Middleware Docs](https://pkg.go.dev/github.com/go-chi/chi/v5/middleware)