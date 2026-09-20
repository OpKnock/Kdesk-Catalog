---
applyTo: "**/*.json **/*.py **/*.r **/*.sh **/*.sql"
---

# Flask

Builds Python web apps with Flask: routes, templates, blueprints, CLI commands, and testing with pytest.

## Instructions

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
