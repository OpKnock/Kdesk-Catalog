---
name: "pytest-requests"
description: "API testing with pytest and requests: fixtures, session reuse, assertions, and coverage-driven test suites."
type: knowledge
triggers: ["pytest-requests", "pytest-api-testing"]
---

# Pytest Requests

API testing with pytest and requests: fixtures, session reuse, assertions, and coverage-driven test suites.

## Instructions

# pytest + requests

Test HTTP APIs with pytest fixtures and the requests library for readable, maintainable suites.

## What this skill does

- Sets up session fixtures and clients
- Writes API assertions
- Reports coverage

## When to use

- Contract/regression tests for REST APIs
- Validating API behavior after changes

## Real commands

```bash
pip install pytest requests pytest-cov

# Run
pytest tests/ -v
pytest tests/test_orders.py -x --tb=short
pytest -k "auth"

# Coverage
pytest --cov=src tests/
pytest --cov=src --cov-report=term-missing tests/
```

## Test example

```python
import requests

BASE = "http://localhost:8080/api"

def test_create_order():
    r = requests.post(f"{BASE}/orders", json={"item": "lamp"})
    assert r.status_code == 201
    assert r.json()["id"]
```

## Session fixture

```python
import pytest, requests

@pytest.fixture(scope="session")
def client():
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {TOKEN}"})
    return s
```

## Best practices

- One test per behavior; use pytest.raises for errors
- Keep tests independent with fixture scopes
- Run with -x in CI and coverage thresholds

## Capabilities

### pytest-api-testing
Write and run pytest suites for HTTP APIs using the requests library with fixtures and coverage.

**Commands:**
- `pip install pytest requests pytest-cov`
- `pytest tests/ -v`
- `pytest tests/ -k "api"`
- `pytest --cov=src tests/`
- `pytest tests/test_orders.py -x --tb=short`

**Examples:**
- pytest tests/test_orders.py -v
- pytest --cov=src --cov-report=term-missing tests/
- pytest -k "auth and not slow"
