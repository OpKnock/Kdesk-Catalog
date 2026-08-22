---
name: "api-rest-fastapi-routes"
description: "Implements REST APIs with FastAPI and Pydantic: typed routes, automatic OpenAPI docs, dependency injection, and TestClient-based testing."
---

# Api Rest Fastapi Routes

Implements REST APIs with FastAPI and Pydantic: typed routes, automatic OpenAPI docs, dependency injection, and TestClient-based testing.

## Instructions

# API REST Engineer v2 - FastAPI

REST APIs with FastAPI.

## What This Skill Does
- Builds typed routes with Pydantic validation
- Auto-generates OpenAPI docs
- Uses dependencies for auth and DB access

## When to Use
- Python REST services
- Prototyping with instant docs
- Validation-heavy APIs

## Real Commands

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
curl -s http://127.0.0.1:8000/openapi.json | jq '.paths | keys'
```

## Route Example

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post('/api/items', status_code=201)
def create_item(item: Item):
    return {'id': 1, **item.model_dump()}
```

## Testing
- Use TestClient for route tests without a server
- Verify 422s for schema violations
- Test dependency overrides for auth

## Best Practices
- Define response_model to shape output
- Organize routes with APIRouter
- Add tags and operation summaries for docs

## Capabilities

### fastapi-routes
Define typed FastAPI routes with automatic validation

**Commands:**
- `pip install fastapi uvicorn`
- `uvicorn main:app --reload`
- `curl -s http://127.0.0.1:8000/openapi.json | jq '.paths | keys'`
- `curl -s http://127.0.0.1:8000/docs -o /dev/null -w '%{http_code}\n'`
- `curl -s -X POST http://127.0.0.1:8000/api/items -H 'Content-Type: application/json' -d '{"name":"widget"}' -w '\n%{http_code}\n'`

**Examples:**
- uvicorn main:app --reload hot-reloads the API
- GET /openapi.json returns the generated contract
- Invalid payloads return 422 automatically

### dependency-injection
Share auth and DB logic via FastAPI dependencies

**Commands:**
- `curl -s -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer invalid' http://127.0.0.1:8000/api/me`
- `pytest -q`
- `uvicorn main:app --host 0.0.0.0 --port 8000`

**Examples:**
- -cli --help
- -api --help
