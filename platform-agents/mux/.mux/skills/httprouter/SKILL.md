---
name: "httprouter"
description: "Go httprouter: radix-tree routing with typed path params, method handlers, middleware wrapping, and benchmark-grade request dispatch."
---

# httprouter

Go httprouter: radix-tree routing with typed path params, method handlers, middleware wrapping, and benchmark-grade request dispatch.

## Instructions

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
