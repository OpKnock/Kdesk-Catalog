---
applyTo: "**/*.html **/*.py **/*.r **/*.sh"
---

Runs Python tests with pytest: fixtures, parametrization, markers, parallel execution, and coverage.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pytest`, `pytest --fixtures`
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

# pytest

The standard Python testing framework.

## What This Skill Does

- Runs tests with precise selectors and filters
- Writes fixtures for shared state and mocks
- Parametrizes tests for data-driven coverage
- Parallelizes runs and measures coverage


## When to Use

- Unit and integration tests for Python services
- Data-driven test matrices
- CI coverage gates

## Real Commands

```bash
# Run
pytest
pytest tests/test_app.py::test_login
pytest -k "login or signup"
pytest -m smoke --maxfail=1

# Debug
pytest --collect-only
pytest tests/test_order.py::test_calc[2-3-6] --pdb

# Parallel and coverage
pytest -n 4 --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=html:coverage_html
pytest --junitxml=results.xml
```

## Sample Test

```python
import pytest

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.parametrize("a,b,expected", [(2, 3, 6), (-1, 5, -5)])
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected

@pytest.mark.smoke
def test_health(client):
    assert client.get("/health").status_code == 200
```

## Best Practices

- Use fixtures over module-level setup
- Parametrize edge cases; keep one assertion intent per test
- Tag smoke tests and run them on every PR
- Use -n parallel in CI with careful fixture isolation
- Set coverage thresholds in pytest.ini

## Capabilities

### pytest-runs
Run tests with filters, markers, and ordering.

**Parameters:**
- `testPath` (string): File::test selector
- `keyword` (string): Expression filter (-k)
- `marker` (string): Marker filter (-m)

**Commands:**
- `pytest`
- `pytest tests/test_app.py::test_login`
- `pytest -k "login or signup"`
- `pytest -m slow`
- `pytest -x --maxfail=1`

**Examples:**
- pytest tests/test_app.py::test_login
- pytest -k login
- pytest -m smoke --maxfail=1

### fixtures-and-parametrize
Build shared fixtures and data-driven tests.

**Parameters:**
- `fixtures` (boolean): List available fixtures
- `pdb` (boolean): Drop into pdb on failure

**Commands:**
- `pytest --fixtures`
- `pytest --setup-show`
- `pytest tests/test_order.py::test_calc[2-3-6]`
- `pytest --collect-only`
- `pytest --pdb`

**Examples:**
- pytest --fixtures
- pytest --collect-only
- pytest tests/test_order.py::test_calc[2-3-6] --pdb

### parallel-and-coverage
Parallel runs and coverage reports.

**Parameters:**
- `workers` (number): Parallel workers (-n)
- `cov` (string): Package to measure coverage

**Commands:**
- `pytest -n 4`
- `pytest --cov=src --cov-report=term-missing`
- `pytest --cov=src --cov-report=html:coverage_html`
- `pytest --junitxml=results.xml`
- `pytest --lf --last-failed-no-failures=all`

**Examples:**
- pytest -n 4 --cov=src
- pytest --cov=src --cov-report=html:coverage_html
- pytest --junitxml=results.xml

## References
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-xdist](https://pytest-xdist.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
