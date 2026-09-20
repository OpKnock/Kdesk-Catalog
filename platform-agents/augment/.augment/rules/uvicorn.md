---
type: agent_requested
description: "Serves ASGI applications with uvicorn: dev reload, production workers, HTTP/2, lifecycle, and container deployment."
---

# uvicorn

Serves ASGI applications with uvicorn: dev reload, production workers, HTTP/2, lifecycle, and container deployment.

## Instructions

# Uvicorn

ASGI server for Python async apps.

## When to Use

- Serving FastAPI, Starlette, and other ASGI apps
- Development with hot reload
- Production serving with multiple workers

## Commands

```bash
# Dev with reload
uvicorn main:app --reload

# Watch a directory
uvicorn main:app --reload --reload-dir app

# Production: 4 workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# HTTP/2 support
uvicorn main:app --http2

# App factory pattern
uvicorn --factory main:create_app

# Keep-alive tuning
uvicorn main:app --timeout-keep-alive 65

# Debug logging
uvicorn main:app --log-level debug
```

## Deployment

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Best Practices

- Workers > 1 only when the app is async and dependency-free of globals
- Use uvloop loop for better throughput on Linux
- Terminate cleanly on SIGTERM; uvicorn handles it
- Put a proxy (nginx/traefik) in front for TLS and buffering
- Verify with curl before declaring deploy healthy

## Capabilities

### uvicorn-serving
Run ASGI apps in dev and production.

**Commands:**
- `uvicorn main:app --reload`
- `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4`
- `uvicorn main:app --http2`
- `uvicorn main:app --timeout-keep-alive 65`
- `uvicorn --factory main:create_app`

**Examples:**
- uvicorn main:app --reload --reload-dir app
- uvicorn main:app --workers 4 --loop uvloop
- uvicorn main:app --log-level debug

### uvicorn-health
Verify the server is up and accepting requests.

**Commands:**
- `curl -s http://localhost:8000/health`
- `curl -sI http://localhost:8000 | head -1`
- `ss -tlnp | grep 8000`
- `lsof -i :8000`

**Examples:**
- curl -s -o /dev/null -w "%{http_code}" http://localhost:8000
- netstat -ano | findstr :8000