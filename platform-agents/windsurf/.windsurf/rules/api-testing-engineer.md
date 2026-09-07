---
trigger: glob
description: "Builds API test automation frameworks: REST Assured for Java, pytest + httpx for Python, reusable fixtures, and CI integration. Use when working with rest assured, pytest httpx or when the user mentions rest assured, pytest httpx."
globs: ["**/*.html", "**/*.java", "**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Builds API test automation frameworks: REST Assured for Java, pytest + httpx for Python, reusable fixtures, and CI integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn -q test -Dtest=UserApiTest`, `pip install pytest httpx pytest-cov`
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

**Parameters:**
- `test-class` (string): Test class name
- `method` (string): Test method filter
- `profile` (string): Maven profile

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

## References
- [REST Assured Docs](https://rest-assured.io/)
- [pytest Docs](https://docs.pytest.org/)
