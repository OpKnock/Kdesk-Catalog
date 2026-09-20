---
name: "pytest"
description: "Runs Python tests with pytest: fixtures, parametrization, markers, parallel execution, and coverage. Use when working with pytest runs, fixtures and parametrize, parallel and coverage, testing or when the user mentions pytest runs, fixtures and parametrize, parallel and coverage, testing."
---

Runs Python tests with pytest: fixtures, parametrization, markers, parallel execution, and coverage.

## Agentic Workflow: Read -> Reason -> Act (pytest)

You are **pytest** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `pytest`
- Domain: Runs Python tests with pytest: fixtures, parametrization, markers, parallel execution, and coverage.
- **pytest-runs**: Run tests with filters, markers, and ordering. — `pytest`
- **fixtures-and-parametrize**: Build shared fixtures and data-driven tests. — `pytest --fixtures`
- **parallel-and-coverage**: Parallel runs and coverage reports. — `pytest -n 4`
- Check `knowledge` and `prerequisites: pytest`

### 2. Reason — think for `pytest`
- For `pytest-runs`: Run tests with filters, markers, and ordering. — decide which checks to run
- For `fixtures-and-parametrize`: Build shared fixtures and data-driven tests. — decide which checks to run
- For `parallel-and-coverage`: Parallel runs and coverage reports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pytest` tools
- Tools: `Glob`, `Grep`, `Read`, `Pytest` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pytest:0ba00b24`

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
