---
trigger: glob
description: "Implements the Builder pattern in Python: constructing complex objects step-by-step with fluent APIs."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
---

# Builder

Implements the Builder pattern in Python: constructing complex objects step-by-step with fluent APIs.

## Instructions

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
