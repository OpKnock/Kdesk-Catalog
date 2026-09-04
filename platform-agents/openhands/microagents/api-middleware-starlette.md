---
name: "api-middleware-starlette"
description: "Builds Python ASGI middleware for FastAPI and Starlette: CORSMiddleware, GZipMiddleware, TrustedHostMiddleware, and custom BaseHTTPMiddleware for auth and logging."
type: knowledge
triggers: ["api-middleware-starlette", "starlette-middleware", "custom-asgi-middleware"]
---

# Api Middleware Starlette

Builds Python ASGI middleware for FastAPI and Starlette: CORSMiddleware, GZipMiddleware, TrustedHostMiddleware, and custom BaseHTTPMiddleware for auth and logging.

## Instructions

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
