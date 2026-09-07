---
name: "python"
description: "Develops Python backends: virtual environments, packaging, dependency management, debugging, and testing with pytest. Use when working with python env, python dev, backend or when the user mentions python env, python dev, backend."
license: "MIT"
compatibility: "Requires .venv\\\\scripts\\\\activate, pip, pytest, python."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(.venv\\\\Scripts\\\\activate:*) Bash(pip:*) Bash(pytest:*) Bash(python:*)"
---

Develops Python backends: virtual environments, packaging, dependency management, debugging, and testing with pytest.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m venv .venv`, `python -m pdb app.py`
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

# Python

Backend development with Python.

## When to Use

- APIs, data pipelines, automation, and ML services
- Rapid iteration with rich stdlib and ecosystem
- Teams working in data-heavy domains

## Commands

```bash
# Environment
python -m venv .venv
# Windows: .venv\Scripts\activate | Unix: source .venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt

# Debug
python -m pdb app.py
python -m pdb -c continue app.py

# Tests
pytest -q
pytest --cov=src tests/
pytest tests/test_api.py -k "login" -v

# Compile check
python -m compileall src/
```

## Example

```python
# app.py
from http.server import HTTPServer, BaseHTTPRequestHandler

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

HTTPServer(("", 8000), H).serve_forever()
```

## Best Practices

- Always work inside a virtualenv; never pip install globally
- Pin versions with pip freeze or a lockfile in CI
- Add type hints and run mypy where practical
- Run pytest with coverage in CI and enforce a threshold
- Use python -m pdb for quick diagnosis before adding logging
- Keep requirements and pyproject metadata in sync

## Capabilities

### python-env
Manage virtual environments and dependencies.

**Parameters:**
- `env-path` (string): Virtual env path
- `requirements` (string): Requirements file path

**Commands:**
- `python -m venv .venv`
- `.venv\\Scripts\\activate`
- `pip install -r requirements.txt`
- `pip freeze > requirements.txt`
- `pip install -e .`

**Examples:**
- python -m venv --upgrade-deps .venv
- pip install --upgrade pip setuptools wheel
- python -m pip cache info

### python-dev
Run, debug, and test Python code.

**Parameters:**
- `target` (string): Module path or test selector
- `cov` (boolean): Collect coverage

**Commands:**
- `python -m pdb app.py`
- `python -c "import urllib.request; print(urllib.request.urlopen(\"http://localhost:8000/health\").status)"`
- `pytest -q`
- `pytest --cov=src tests/`
- `python -m compileall src/`

**Examples:**
- python -m pdb -c continue app.py
- pytest tests/test_api.py -k "login" -v
- python -m trace --count app.py

## References
- [Python Docs](https://docs.python.org/3/)
- [Python Packaging Guide](https://packaging.python.org)
- [pytest Docs](https://docs.pytest.org)
