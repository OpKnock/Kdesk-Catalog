---
name: "api-testing-engineer"
description: "Builds API test automation frameworks: REST Assured for Java, pytest + httpx for Python, reusable fixtures, and CI integration."
globs: ["**/*.html", "**/*.java", "**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# api-testing-engineer

Builds API test automation frameworks: REST Assured for Java, pytest + httpx for Python, reusable fixtures, and CI integration.

## Instructions

# API Testing Engineer

API test automation frameworks.

## What This Skill Does
- Builds Java suites with REST Assured
- Builds Python suites with pytest/httpx
- Integrates into CI pipelines

## When to Use
- Long-lived API test suites
- Cross-team test infrastructure
- Replacing manual API checklists

## Real Commands

```bash
mvn -q test -Dtest=UserApiTest
pip install pytest httpx pytest-cov
pytest -q -k users
pytest --cov=api --cov-report=html
```

## REST Assured Example

```java
given()
  .contentType(ContentType.JSON)
  .body("{\"name\":\"alice\"}")
.when()
  .post("/api/users")
.then()
  .statusCode(201);
```

## Testing
- Run suites in CI with JUnit XML output
- Track coverage on new endpoints
- Parameterize environments


## Best Practices
- Model test data with factories
- Keep tests order-independent
- Centralize client setup in base classes

## Capabilities

### rest-assured
Write Java API tests with REST Assured

**Commands:**
- `mvn -q test -Dtest=UserApiTest`
- `mvn -q test -Dtest=UserApiTest#createUser`
- `mvn dependency:tree | grep -i rest-assured`
- `mvn verify`

**Examples:**
- -Dtest=UserApiTest runs one test class
- #createUser filters a single method
- mvn verify runs the full suite

### pytest-httpx
Write Python API tests with pytest

**Commands:**
- `pip install pytest httpx pytest-cov`
- `pytest -q`
- `pytest -q -k users`
- `pytest --cov=api --cov-report=html`
- `pytest -q --tb=short tests/test_users.py`

**Examples:**
- -cli --help
- -api --help