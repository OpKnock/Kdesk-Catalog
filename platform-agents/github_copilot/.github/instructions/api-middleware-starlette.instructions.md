---
applyTo: "**/*.json **/*.py **/*.r **/*.rs **/*.sh"
---

Builds Python ASGI middleware for FastAPI and Starlette: CORSMiddleware, GZipMiddleware, TrustedHostMiddleware, and custom BaseHTTPMiddleware for auth and logging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install fastapi uvicorn`, `python -c "from starlette.middleware.base import BaseHTTPMid`
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

# API Middleware v4 - Python ASGI

Middleware for FastAPI and Starlette ASGI apps.

## What This Skill Does
- Adds CORS, gzip, trusted-host, and session middleware via add_middleware
- Writes custom BaseHTTPMiddleware subclasses
- Tests middleware with pytest and curl

## When to Use
- Securing a FastAPI backend behind a browser SPA
- Compressing JSON responses over slow links
- Validating the Host header against an allowlist

## Real Commands

```bash
pip install fastapi uvicorn
uvicorn app:app --reload --port 8000
curl -s -H 'Origin: http://localhost:5173' -D- http://localhost:8000/api | grep -i access-control
```

## Middleware Example

```python
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['api.example.com'])
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'])
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Testing
- Preflight OPTIONS requests must include the right Access-Control headers
- Wrong Host header must return 400 from TrustedHostMiddleware
- Compressible responses must include Content-Encoding: gzip

## Best Practices
- Register CORS before custom middleware that inspects requests
- Use pure ASGI classes for hot paths; BaseHTTPMiddleware adds buffering
- Pin allowed_hosts in production; never use wildcards

## Capabilities

### starlette-middleware
Apply Starlette built-in middleware classes to a FastAPI app

**Parameters:**
- `allow_origins` (array): CORS allowed origins list
- `minimum_size` (integer): Minimum response bytes before gzip compression
- `allowed_hosts` (array): Hosts allowed through TrustedHostMiddleware

**Commands:**
- `pip install fastapi uvicorn`
- `uvicorn app:app --reload --port 8000`
- `curl -s -H 'Origin: http://localhost:5173' -D- http://localhost:8000/api | grep -i access-control`
- `curl -s -H 'Host: evil.example.com' -o /dev/null -w '%{http_code}\n' http://localhost:8000/`
- `pytest -q`

**Examples:**
- app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_methods=['GET','POST'])
- app.add_middleware(GZipMiddleware, minimum_size=1000)
- app.add_middleware(TrustedHostMiddleware, allowed_hosts=['api.example.com'])

### custom-asgi-middleware
Write custom BaseHTTPMiddleware subclasses for auth and request logging

**Commands:**
- `python -c "from starlette.middleware.base import BaseHTTPMiddleware; print(BaseHTTPMiddleware.__mro__)"`
- `curl -s -H 'Authorization: Bearer test' -o /dev/null -w '%{http_code}\n' http://localhost:8000/secure`
- `curl -s http://localhost:8000/openapi.json | python -m json.tool | head -20`

**Examples:**
- -cli --help
- -api --help

## References
- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Starlette Middleware](https://www.starlette.io/middleware/)
