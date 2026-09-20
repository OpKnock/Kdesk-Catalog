---
name: "starlette"
description: "Build lightweight ASGI APIs with Starlette and uvicorn. Composes async route handlers, runs a dev server with hot reload, and validates endpoints using the in-process TestClient \u2014 no live server required. Use when working with starlette apps, api or when the user mentions starlette apps, api."
---

Build lightweight ASGI APIs with Starlette and uvicorn. Composes async route handlers, runs a dev server with hot reload, and validates endpoints using the in-process TestClient — no live server required.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install starlette uvicorn`
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

# Starlette

Hand-crafted skill for building ASGI APIs with Starlette.

## What this skill does

- Composes routes into an ASGI application
- Serves it with uvicorn including reload for dev
- Tests handlers with the Starlette TestClient

## When to use

- Lightweight Python APIs without framework magic
- Services that need async performance
- Building up to FastAPI from its foundation

## Real commands

```bash
# Install
pip install starlette uvicorn

# Dev server with reload
uvicorn app:app --reload --port 8000

# Exercise endpoints
curl -s localhost:8000/health
curl -s -X POST localhost:8000/items -H 'Content-Type: application/json' -d '{"name":"widget"}'

# In-process tests
python -c 'from starlette.testclient import TestClient; from app import app; c=TestClient(app); r=c.get("/health"); print(r.status_code, r.json())'
```

## App example

```python
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse

async def health(request):
    return JSONResponse({"status": "ok"})

async def create_item(request):
    body = await request.json()
    return JSONResponse({"id": 1, "name": body["name"]}, status_code=201)

app = Starlette(routes=[
    Route("/health", health),
    Route("/items", create_item, methods=["POST"]),
])
```

## Testing

```bash
python -m pytest -q
# or
curl -s localhost:8000/health
```

## Best practices

- Keep handlers async; use request.json() with await
- Run uvicorn workers = CPU count in production
- Test with TestClient (httpx-based) before deploying

## Capabilities

### starlette-apps
Build and test ASGI APIs with Starlette and uvicorn

**Parameters:**
- `host` (string): Bind host for uvicorn
- `port` (integer): Bind port for uvicorn
- `reload` (boolean): Auto-reload on source changes

**Commands:**
- `pip install starlette uvicorn`
- `uvicorn app:app --reload --port 8000`
- `curl -s localhost:8000/health`
- `curl -s -X POST localhost:8000/items -H 'Content-Type: application/json' -d '{"name":"widget"}'`
- `python -c 'from starlette.testclient import TestClient; from app import app; c=TestClient(app); r=c.get("/health"); print(r.status_code, r.json())'`

**Examples:**
- uvicorn app:app --reload --port 8000
- curl -s localhost:8000/health
- python -c 'from starlette.testclient import TestClient; from app import app; c=TestClient(app); print(c.get("/health").json())'

## References
- [Starlette docs](https://www.starlette.io/)
- [uvicorn docs](https://www.uvicorn.org/)
