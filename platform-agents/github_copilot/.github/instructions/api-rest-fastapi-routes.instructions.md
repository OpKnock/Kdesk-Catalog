---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

Implements REST APIs with FastAPI and Pydantic: typed routes, automatic OpenAPI docs, dependency injection, and TestClient-based testing.

## Agentic Workflow: Read -> Reason -> Act (api-rest-fastapi-routes)

You are **Api Rest Fastapi Routes** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-rest-fastapi-routes`
- Domain: Implements REST APIs with FastAPI and Pydantic: typed routes, automatic OpenAPI docs, dependency injection, and TestClient-based testing.
- **fastapi-routes**: Define typed FastAPI routes with automatic validation — `pip install fastapi uvicorn`
- **dependency-injection**: Share auth and DB logic via FastAPI dependencies — `curl -s -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer invalid' http`
- Check `knowledge` and `prerequisites: node.js, python, express, fastapi`

### 2. Reason — think for `api-rest-fastapi-routes`
- For `fastapi-routes`: Define typed FastAPI routes with automatic validation — decide which checks to run
- For `dependency-injection`: Share auth and DB logic via FastAPI dependencies — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-rest-fastapi-routes` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Uvicorn` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-rest-fastapi-routes:d8f9c0c3`

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

**Parameters:**
- `model` (object): Pydantic request model
- `status-code` (integer): Route response status
- `response-model` (object): Pydantic response model

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

## References
- [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
