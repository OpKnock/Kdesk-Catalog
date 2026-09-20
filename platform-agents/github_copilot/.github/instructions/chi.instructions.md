---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

# Chi

Build Go HTTP APIs with the chi router: routing, middleware, URL params, and subrouters.

## Instructions

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

**Commands:**
- `go test ./...`
- `curl -i http://localhost:3000/api/users`
- `curl -s http://localhost:3000/api/users/42`
- `curl -s -X POST -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:3000/api/users`

**Examples:**
- curl -s http://localhost:3000/api/users | jq '.[0].name'
- curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Content-Type: application/json" -d '{"name":"alice"}' http://localhost:3000/api/users
- go test -race ./...
