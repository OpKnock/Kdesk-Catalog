---
name: "chi"
description: "Build Go HTTP APIs with the chi router: routing, middleware, URL params, and subrouters. Use when working with chi routing, chi testing, api or when the user mentions chi routing, chi testing, api."
license: "MIT"
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(go:*)"
---

Build Go HTTP APIs with the chi router: routing, middleware, URL params, and subrouters.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `go get github.com/go-chi/chi/v5`, `go test ./...`
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
