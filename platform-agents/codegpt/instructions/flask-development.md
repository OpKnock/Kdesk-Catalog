# Flask Development

Build Python APIs with Flask: run the dev server, use the Flask CLI, register blueprints and error handlers, and test with pytest.

## Instructions

# Flask v2

## What this skill does

Flask is a lightweight Python WSGI framework. Modern Flask (2.x+) has a rich CLI: `flask run`, `flask routes`, `flask shell`, and application factories for testability.

## When to use

- Building small to medium Python APIs and dashboards
- Prototyping services quickly
- Teaching or internal tooling with minimal framework

## Real commands

```bash
# Run with debug reloader
flask --app app run --debug

# Bind to all interfaces on another port
flask --app app run --host 0.0.0.0 --port 5001

# List registered routes
flask --app app routes

# Interactive shell with app context
flask --app app shell

# Tests
python -m pytest -v
```

## App factory example

```python
from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/api/orders/<order_id>")
    def get_order(order_id):
        if order_id not in (“1”, “2”):
            return jsonify({"error": "not found"}), 404
        return jsonify({"id": order_id})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found"}), 404

    return app
```

## Testing with the test client

```python
import pytest
from app import create_app

@pytest.fixture
def client():
    return create_app().test_client()

def test_missing_order(client):
    assert client.get("/api/orders/99").status_code == 404
```

## Best practices

- Use the app factory pattern for testability.
- Configure via env vars and app.config.from_prefixed_env.
- Register blueprints for larger apps.
- Run with a WSGI server (gunicorn) in production, not flask run.
- Use `flask routes` in CI to catch route typos.

## Capabilities

### flask-development
Run, debug, and test Flask applications with the flask CLI.

**Commands:**
- `flask --app app run --debug`
- `flask --app app run --host 0.0.0.0 --port 5001`
- `flask --app app routes`
- `python -m pytest -v`
- `flask --app app shell`

**Examples:**
- flask --app app run --debug
- flask --app app routes
- python -m pytest -v
