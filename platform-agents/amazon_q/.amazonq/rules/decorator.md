Implements the Decorator pattern in Python with unittest: adding behavior to objects at runtime without subclass explosion.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m unittest discover -s tests`
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

**Parameters:**
- `discover` (string): Auto-discover tests in a directory
- `pattern` (string): Test file glob pattern
- `k` (string): Test name filter

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

## References
- [Refactoring Guru: Decorator](https://refactoring.guru/design-patterns/decorator)
- [Python unittest](https://docs.python.org/3/library/unittest.html)