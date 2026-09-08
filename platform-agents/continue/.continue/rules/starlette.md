---
name: "Starlette"
description: "Build lightweight ASGI APIs with Starlette and uvicorn. Composes async route handlers, runs a dev server with hot reload, and validates endpoints using the in-process TestClient \u2014 no live server required. Use when working with starlette apps, api or when the user mentions starlette apps, api."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Build lightweight ASGI APIs with Starlette and uvicorn. Composes async route handlers, runs a dev server with hot reload, and validates endpoints using the in-process TestClient — no live server required.

## Agentic Workflow: Read -> Reason -> Act (starlette)

You are **Starlette** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `starlette`
- Domain: Build lightweight ASGI APIs with Starlette and uvicorn. Composes async route handlers, runs a dev server with hot reload, and validates endpoints using the in-process TestClient — no live server requi
- **starlette-apps**: Build and test ASGI APIs with Starlette and uvicorn — `pip install starlette uvicorn`
- Check `knowledge` and `prerequisites: pip, python, uvicorn`

### 2. Reason — think for `starlette`
- For `starlette-apps`: Build and test ASGI APIs with Starlette and uvicorn — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `starlette` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Uvicorn` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `starlette:954ab640`

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