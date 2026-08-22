# Decorator

Implements the Decorator pattern in Python with unittest: adding behavior to objects at runtime without subclass explosion.

## Instructions

# Decorator Pattern

Wrap objects with behavior without changing their contract.

## When to Use

- Adding logging, caching, retries to operations
- Layering behavior without subclass explosion
- Compose combinations at runtime

## Example (Python)

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> str: ...

class EmailNotifier(Notifier):
    def send(self, message: str) -> str:
        return f"email: {message}"

class LoggingDecorator(Notifier):
    def __init__(self, inner: Notifier) -> None:
        self._inner = inner

    def send(self, message: str) -> str:
        result = self._inner.send(message)
        return f"[logged] {result}"

class RetryDecorator(Notifier):
    def __init__(self, inner: Notifier, tries: int = 3) -> None:
        self._inner = inner
        self._tries = tries

    def send(self, message: str) -> str:
        last = None
        for _ in range(self._tries):
            last = self._inner.send(message)
        return f"[retried] {last}"
```

## Test

```python
import unittest

def test_logging_wrapper(self):
    n = LoggingDecorator(EmailNotifier())
    self.assertIn("logged", n.send("hi"))
```

```bash
python -m unittest discover -s tests -v
```

## Best practices

- Decorators implement the same interface as the wrapped object.
- Keep decorators stateless and order-independent where possible.
- Prefer composition (decorators) over inheritance trees.
- Document wrapper order - it matters.

## Testing

Test each decorator in isolation and in combination.

## Capabilities

### python-unittest
Implement and test Decorator pattern examples.

**Commands:**
- `python -m unittest discover -s tests`
- `python -m unittest tests.test_decorators -v`
- `python -m unittest tests.test_decorators.DecoratorTest.test_logging_wrapper`
- `python -m compileall decorators.py`
- `python -m unittest discover -s tests -p '*_test.py'`

**Examples:**
- python -m unittest discover -s tests -v
- python -m unittest tests.test_decorators -k log
- python -m unittest tests.test_decorators.DecoratorTest -v