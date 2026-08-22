---
name: "Fastapi"
description: "Builds modern Python APIs with FastAPI: automatic OpenAPI docs, Pydantic models, async routes, and deployment with uvicorn."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Fastapi

Builds modern Python APIs with FastAPI: automatic OpenAPI docs, Pydantic models, async routes, and deployment with uvicorn.

## Instructions

# FastAPI

Modern, fast Python API framework with automatic OpenAPI docs.

## When to Use

- REST APIs with automatic validation and interactive docs
- Async and sync endpoints mixed in one service
- Data-heavy services with Pydantic response models
- Rapid prototyping that scales to production

## Commands

```bash
pip install "fastapi[standard]"

# Dev server with reload
fastapi dev main.py

# Production server
fastapi run main.py
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Docs
curl http://localhost:8000/docs
curl -s http://localhost:8000/openapi.json | python -m json.tool
```

## App Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Shop API")

class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id > 1000:
        raise HTTPException(404, "Item not found")
    return {"id": item_id}
```

## Best Practices

- Use response_model to guarantee API output shape
- Raise HTTPException instead of returning error dicts
- Prefer async routes for I/O; sync routes run in a threadpool anyway
- Validate with Pydantic constraints, not manual if-statements
- Run with workers > 1 behind a load balancer in production
- Check /openapi.json and /docs to confirm the contract

## Capabilities

### fastapi-dev
Scaffold and run FastAPI applications with auto-reload.

**Commands:**
- `pip install "fastapi[standard]"`
- `fastapi dev main.py`
- `fastapi run main.py`
- `uvicorn main:app --reload`
- `uvicorn main:app --host 0.0.0.0 --port 8000`

**Examples:**
- fastapi dev main.py --port 8080
- uvicorn main:app --reload --reload-dir app
- fastapi run main.py --workers 4

### fastapi-openapi
Inspect generated OpenAPI schema and test endpoints.

**Commands:**
- `curl http://localhost:8000/openapi.json`
- `curl http://localhost:8000/docs`
- `curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d "{\"name\":\"widget\"}"`
- `python -c "import json,urllib.request; print(json.load(urllib.request.urlopen(\"http://localhost:8000/openapi.json\"))[\"paths\"])"`

**Examples:**
- curl -s http://localhost:8000/openapi.json | python -m json.tool | head -50
- curl -X GET "http://localhost:8000/items/1?verbose=true"