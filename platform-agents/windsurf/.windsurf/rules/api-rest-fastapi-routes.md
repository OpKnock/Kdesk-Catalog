---
trigger: glob
description: "Implements REST APIs with FastAPI and Pydantic: typed routes, automatic OpenAPI docs, dependency injection, and TestClient-based testing. Use when working with fastapi routes, dependency injection or when the user mentions fastapi routes, dependency injection."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Implements REST APIs with FastAPI and Pydantic: typed routes, automatic OpenAPI docs, dependency injection, and TestClient-based testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install fastapi uvicorn`, `curl -s -o /dev/null -w '%{http_code}\n' -H 'Authorization: `
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
