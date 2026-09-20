---
name: "fastapi"
description: "Build async Python APIs with FastAPI: run uvicorn, generate OpenAPI schemas, create Pydantic models, and test endpoints with TestClient."
type: knowledge
triggers: ["fastapi", "fastapi-server"]
---

# Fastapi

Build async Python APIs with FastAPI: run uvicorn, generate OpenAPI schemas, create Pydantic models, and test endpoints with TestClient.

## Instructions

# FastAPI

## What this skill does

FastAPI is a modern async Python framework with automatic OpenAPI generation and Pydantic validation. This skill covers running uvicorn, defining routes/models, exporting schemas, and testing.

## When to use

- Building a new Python REST API
- Generating client libraries from the auto OpenAPI schema
- Writing fast async endpoints with type validation

## Real commands

```bash
# Install and run
pip install fastapi uvicorn[standard] pydantic
uvicorn main:app --reload --port 8000

# Production: multiple workers on 0.0.0.0
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Inspect the auto-generated schema
curl -s http://localhost:8000/openapi.json | jq '.paths | keys'

# Tests
python -m pytest tests/ -v
```

## Minimal app

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Order(BaseModel):
    id: str
    amount: float

@app.get("/api/orders/{order_id}")
async def get_order(order_id: str) -> Order:
    order = find(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
```

## Testing with TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_missing_order():
    r = client.get("/api/orders/nope")
    assert r.status_code == 404
```

## Best practices

- Use async def for IO-bound routes; plain def for CPU-bound sync ones.
- Let Pydantic models drive both validation and response docs.
- Set `responses={404: ...}` on routes for accurate generated docs.
- Use dependency injection for auth and DB sessions instead of globals.
- In prod, run with `--workers` behind a process manager, not `--reload`.

## Capabilities

### fastapi-server
Run, generate schema for, and test FastAPI applications.

**Commands:**
- `uvicorn main:app --reload --port 8000`
- `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4`
- `curl -s http://localhost:8000/openapi.json | jq '.paths | keys'`
- `python -m pytest tests/ -v`
- `pip install fastapi uvicorn[standard] pydantic`

**Examples:**
- uvicorn main:app --reload --port 8000
- curl -s http://localhost:8000/openapi.json | jq '.paths | keys'
- python -m pytest tests/ -v
