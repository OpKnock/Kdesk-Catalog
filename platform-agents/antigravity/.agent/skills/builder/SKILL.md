---
name: "builder"
description: "Implements the Builder pattern in Python: constructing complex objects step-by-step with fluent APIs. Use when working with python, builder or when the user mentions python, builder."
license: "MIT"
compatibility: "Requires python."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "patterns"}
allowed-tools: "Glob Grep Read Bash(python:*)"
---

Implements the Builder pattern in Python: constructing complex objects step-by-step with fluent APIs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m venv .venv && .venv/Scripts/activate`
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

# Builder Pattern

Construct complex objects step by step.

## When to Use

- Objects with many optional parameters
- Immutable value objects assembled from parts
- Reducing constructor overloads

## Example (Python)

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Order:
    sku: str
    qty: int
    priority: str = "normal"
    note: str = ""

class OrderBuilder:
    def __init__(self) -> None:
        self._sku = ""
        self._qty = 1
        self._priority = "normal"
        self._note = ""

    def with_sku(self, sku: str) -> "OrderBuilder":
        self._sku = sku
        return self

    def with_qty(self, qty: int) -> "OrderBuilder":
        self._qty = qty
        return self

    def with_priority(self, priority: str) -> "OrderBuilder":
        self._priority = priority
        return self

    def build(self) -> Order:
        return Order(self._sku, self._qty, self._priority, self._note)
```

## Test

```python
from builder import OrderBuilder

def test_builder_defaults():
    order = OrderBuilder().with_sku("A1").with_qty(2).build()
    assert order.sku == "A1"
    assert order.qty == 2
    assert order.priority == "normal"
```

```bash
python -m pytest tests/ -v
```

## Best practices

- Return self from setters for fluent chaining.
- Validate in build() - fail fast on missing requireds.
- Keep the builder mutable, the product immutable.
- Consider a Director only for standard configurations.

## Testing

Cover defaults, overrides, and validation errors.

## Capabilities

### python
Implement and test Builder pattern examples.

**Parameters:**
- `test-path` (string): pytest path filter
- `k` (string): pytest -k expression
- `maxfail` (number): Stop after N failures

**Commands:**
- `python -m venv .venv && .venv/Scripts/activate`
- `python -m pip install pytest`
- `python -m pytest tests/ -v`
- `python -m pytest tests/test_builder.py -k price`
- `python -m compileall builder.py`

**Examples:**
- python -m pytest tests/ -q
- python -m pytest tests/test_builder.py --maxfail=1
- python -c 'from builder import OrderBuilder; print(OrderBuilder().with_sku("A1").with_qty(2).build())'

## References
- [Refactoring Guru: Builder](https://refactoring.guru/design-patterns/builder)
- [Python Typing](https://docs.python.org/3/library/typing.html)
