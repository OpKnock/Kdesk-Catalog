---
name: "Fiber"
description: "Build high-performance Go HTTP APIs with Fiber: run the server, wire middleware, and test routes."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Fiber

Build high-performance Go HTTP APIs with Fiber: run the server, wire middleware, and test routes.

## Instructions

# Fiber

## What this skill does

Fiber is an Express-inspired web framework for Go built on fasthttp, known for high throughput and low memory usage. It provides familiar routing, middleware, and context APIs.

## When to use

- Building fast Go REST APIs or BFFs
- Teams coming from Express/Node wanting Go performance
- Embedding HTTP servers in existing Go services

## Real commands

```bash
# Get the module and run
go get github.com/gofiber/fiber/v2
go run main.go

# Build and test
go build -o server main.go
 go test ./... -v

# Smoke test
curl -s localhost:3000/api/orders | jq
```

## Minimal app

```go
package main

import (
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/logger"
)

func main() {
    app := fiber.New()
    app.Use(logger.New())

    app.Get("/api/orders/:id", func(c *fiber.Ctx) error {
        if c.Params("id") == "" {
            return c.Status(400).JSON(fiber.Map{"error": "missing id"})
        }
        return c.JSON(fiber.Map{"id": c.Params("id")})
    })

    app.Listen(":3000")
}
```

## Testing

```go
func TestGetOrder(t *testing.T) {
    app := buildApp()
    req := httptest.NewRequest("GET", "/api/orders/1", nil)
    resp, _ := app.Test(req)
    if resp.StatusCode != 200 {
        t.Fatalf("expected 200, got %d", resp.StatusCode)
    }
}
```

## Best practices

- Use the embedded `app.Test()` in tests; no need to bind a port.
- Add recover and request-id middleware first in the stack.
- Use `fiber.Map` for ad hoc JSON, typed structs for contracts.
- Enable prefork only with a single process supervisor model.
- Set `IdleTimeout` and `ReadTimeout` on production listeners.

## Capabilities

### fiber-routing
Run Fiber apps, add middleware, and test endpoints.

**Commands:**
- `go get github.com/gofiber/fiber/v2`
- `go run main.go`
- `go build -o server main.go`
- `go test ./... -v`
- `curl -s localhost:3000/api/orders | jq`

**Examples:**
- go get github.com/gofiber/fiber/v2 && go run main.go
- go test ./... -v
- curl -s localhost:3000/api/orders | jq