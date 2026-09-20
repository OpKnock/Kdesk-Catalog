---
trigger: glob
description: "Implements the Strategy pattern in Python with pytest: interchangeable algorithms selected at runtime."
globs: ["**/*.go", "**/*.py", "**/*.r", "**/*.sh"]
---

# Strategy

Implements the Strategy pattern in Python with pytest: interchangeable algorithms selected at runtime.

## Instructions

# Strategy Pattern

Swap algorithms at runtime behind one interface.

## When to Use

- Multiple ways to do one thing (pricing, auth, format)
- Avoiding conditional chains in business logic
- Testing algorithms independently

## Example (Python)

```python
from dataclasses import dataclass
from typing import Protocol

class DiscountStrategy(Protocol):
    def apply(self, amount: float) -> float: ...

class NoDiscount:
    def apply(self, amount: float) -> float:
        return amount

class TenPercent:
    def apply(self, amount: float) -> float:
        return amount * 0.9

class HolidayDiscount:
    def apply(self, amount: float) -> float:
        return amount * 0.75

def apply_discount(amount: float, kind: str) -> float:
    strategies: dict[str, DiscountStrategy] = {
        "none": NoDiscount(),
        "10pct": TenPercent(),
        "holiday": HolidayDiscount(),
    }
    return strategies[kind].apply(amount)
```

## Test

```python
import pytest
from strategy import apply_discount

def test_holiday_discount():
    assert apply_discount(100, "holiday") == 75.0

def test_unknown_strategy():
    with pytest.raises(KeyError):
        apply_discount(100, "nope")
```

```bash
python -m pytest tests/ -v
```

## Best practices

- Strategies implement the same protocol - no type checks.
- Register strategies in a lookup, not if/elif chains.
- Make strategies stateless when possible.
- Name by behavior: TenPercent, not Strategy1.

## Testing

Test each strategy and the registry lookups, including unknown keys.

## Capabilities

### python-pytest
Implement and test strategy examples.

**Commands:**
- `python -m pytest tests/ -v`
- `python -m pytest tests/test_strategy.py -k discount`
- `python -m pytest tests/ -q --tb=short`
- `python -m pytest --cov=strategy tests/`
- `python -m pytest tests/test_strategy.py --maxfail=1`

**Examples:**
- python -m pytest tests/test_strategy.py -v
- python -m pytest --cov=strategy --cov-report=term-missing tests/
- python -c 'from strategy import apply_discount; print(apply_discount(100, "holiday"))'
