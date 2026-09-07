---
name: "flask"
description: "Builds Python web apps with Flask: routes, templates, blueprints, CLI commands, and testing with pytest. Use when working with flask cli, flask extensions, backend or when the user mentions flask cli, flask extensions, backend."
---

Builds Python web apps with Flask: routes, templates, blueprints, CLI commands, and testing with pytest.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `flask --app app run --debug`, `pip install Flask-SQLAlchemy flask-migrate`
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

# Flask

Lightweight Python web framework.

## When to Use

- Small to medium web apps and JSON APIs
- Server-rendered pages with Jinja templates
- Internal tools and admin dashboards
- Applications that grow cleanly with blueprints

## Commands

```bash
pip install flask

# Run with debug
flask --app app run --debug

# Run with create_app factory
flask --app app:create_app run --debug

# List routes
flask --app app routes

# Interactive shell
flask --app app shell

# Database migrations (flask-migrate)
flask --app app db init
flask --app app db migrate -m "add users"
flask --app app db upgrade
flask --app app db downgrade -1
```

## App Example

```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.post("/items")
def create_item():
    data = request.get_json()
    return jsonify(received=data), 201
```

## Best Practices

- Use an app factory with create_app for testability
- Structure larger apps with blueprints per domain
- Run flask --app app routes to keep the surface area visible
- Enable debug only in development; never in production
- Add pytest tests with the app.test_client()

## Capabilities

### flask-cli
Run the Flask dev server and app CLI commands.

**Parameters:**
- `import` (string): App import path
- `debug` (boolean): Enable debugger and reloader

**Commands:**
- `flask --app app run --debug`
- `flask --app app run --host 0.0.0.0 --port 5001`
- `flask --app app routes`
- `flask --app app shell`
- `flask --app app --help`

**Examples:**
- flask --app app:create_app run --debug
- flask --app app routes --sort rule
- python -m flask --app app run

### flask-extensions
Manage extensions like migrate, SQLAlchemy, and testing.

**Parameters:**
- `message` (string): Migration message
- `app-import` (string): Flask app import path for CLI commands

**Commands:**
- `pip install Flask-SQLAlchemy flask-migrate`
- `flask --app app db init`
- `flask --app app db migrate -m "add users"`
- `flask --app app db upgrade`
- `pytest`

**Examples:**
- flask --app app db downgrade -1
- flask --app app db history
- pytest -q tests/

## References
- [Flask Docs](https://flask.palletsprojects.com)
- [Flask Migrate Docs](https://flask-migrate.readthedocs.io)
