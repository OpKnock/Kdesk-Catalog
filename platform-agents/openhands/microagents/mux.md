---
name: "mux"
description: "HTTP routing in Go with gorilla/mux: path variables, method matching, middleware, and route testing."
type: knowledge
triggers: ["mux", "gorilla-mux-routing"]
---

# Mux

HTTP routing in Go with gorilla/mux: path variables, method matching, middleware, and route testing.

## Instructions

# gorilla/mux

gorilla/mux is the classic HTTP router for Go REST APIs, with rich matchers and middleware support.

## What this skill does

- Registers routes with path variables and method constraints
- Chains middleware and uses subrouters
- Tests route behavior with httptest

## When to use

- REST APIs that need path parameters and named routes
- Migrating from the standard mux to a richer router

## Real commands

```bash
# Add the dependency
 go get github.com/gorilla/mux
go mod tidy

# Run and verify
 go run main.go
curl -s http://localhost:8080/users/42

# Static checks and tests
 go vet ./...
go test ./...
```

## Router setup

```go
r := mux.NewRouter()
r.HandleFunc("/users/{id:[0-9]+}", getUser).Methods("GET")
r.HandleFunc("/users", createUser).Methods("POST")
r.Use(loggingMiddleware)
api := r.PathPrefix("/api/v1").Subrouter()
log.Fatal(http.ListenAndServe(":8080", r))
```

## Handler using variables

```go
func getUser(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    fmt.Fprintf(w, "user %s", vars["id"])
}
```

## Best practices

- Use regex constraints (`{id:[0-9]+}`) to avoid route collisions
- Group versioned endpoints under subrouters
- Test handlers with httptest and the mux router directly

## Capabilities

### gorilla-mux-routing
Build REST routers with gorilla/mux: variables, method/host constraints, middleware chains and subrouters.

**Commands:**
- `go get github.com/gorilla/mux`
- `go mod tidy`
- `go run main.go`
- `go vet ./...`
- `go test ./...`

**Examples:**
- go run main.go
- curl -s http://localhost:8080/users/42
- go test -run TestRouter -v ./...
