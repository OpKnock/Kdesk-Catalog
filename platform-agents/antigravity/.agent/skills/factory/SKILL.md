---
name: "factory"
description: "Implements the Factory Method and Abstract Factory patterns in Go: creating objects through interfaces with go test verification. Use when working with go, patterns or when the user mentions go, patterns."
license: "MIT"
compatibility: "No special requirements."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "patterns"}
allowed-tools: "Glob Grep Read Bash(go:*)"
---

Implements the Factory Method and Abstract Factory patterns in Go: creating objects through interfaces with go test verification.

## Agentic Workflow: Read -> Reason -> Act (factory)

You are **Factory** (patterns/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — patterns context for `factory`
- Domain: Implements the Factory Method and Abstract Factory patterns in Go: creating objects through interfaces with go test verification.
- **go**: Implement and test factory patterns in Go. — `go mod init localhost/factory`
- Check `knowledge` references before acting

### 2. Reason — think for `factory`
- For `go`: Implement and test factory patterns in Go. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `factory` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `factory:b92621bf`

# Factory Pattern

Create objects without coupling callers to concrete types.

## When to Use

- Object creation varies by config/context
- Decoupling construction from usage
- Encapsulating complex initialization

## Example (Go)

```go
package factory

type Payment interface {
	Charge(amount int) string
}

type CardPayment struct{}

func (CardPayment) Charge(amount int) string { return "card:" + fmt.Sprint(amount) }

type WalletPayment struct{}

func (WalletPayment) Charge(amount int) string { return "wallet:" + fmt.Sprint(amount) }

func NewPayment(kind string) Payment {
	switch kind {
	case "card":
		return CardPayment{}
	case "wallet":
		return WalletPayment{}
	}
	panic("unknown payment kind: " + kind)
}
```

## Test

```go
func TestNewPayment(t *testing.T) {
	if got := NewPayment("card").Charge(100); got != "card:100" {
		t.Errorf("unexpected: %s", got)
	}
}
```

```bash
go test ./...
```

## Variants

- Factory Method: one creation point, subclasses decide.
- Abstract Factory: families of related objects.
- In Go, a plain function returning an interface is the idiomatic factory.

## Best practices

- Return interfaces, consume interfaces.
- Validate inputs in the factory and fail fast.
- Keep factories side-effect free where possible.
- Test every product the factory can produce.

## Testing

Table-test all kinds, including unknown kind panics.

## Capabilities

### go
Implement and test factory patterns in Go.

**Parameters:**
- `run` (string): Test regex filter
- `cover` (string): Coverage report
- `module` (string): Go module path

**Commands:**
- `go mod init localhost/factory`
- `go build ./...`
- `go vet ./...`
- `go test ./...`
- `go test -run TestCreatePayment -v`

**Examples:**
- go test ./... -cover
- go run ./cmd/example
- go test -run 'Test.*Card' -v ./...

## References
- [Refactoring Guru: Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Go by Example](https://gobyexample.com/interfaces)
