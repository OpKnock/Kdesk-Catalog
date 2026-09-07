---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

API testing with pytest and requests: fixtures, session reuse, assertions, and coverage-driven test suites.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install pytest requests pytest-cov`
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

**Parameters:**
- `test_path` (string): Path to tests directory or file
- `marker` (string): pytest -k expression or marker
- `coverage` (boolean): Enable coverage reporting

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

## References
- [pytest Documentation](https://docs.pytest.org/en/stable/)
- [requests Documentation](https://requests.readthedocs.io/)
