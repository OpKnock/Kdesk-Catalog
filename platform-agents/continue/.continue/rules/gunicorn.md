---
name: "gunicorn"
description: "Serves Python WSGI apps in production with gunicorn: workers, preloading, timeouts, and systemd/container integration."
globs: ["**/*.go", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# gunicorn

Serves Python WSGI apps in production with gunicorn: workers, preloading, timeouts, and systemd/container integration.

## Instructions

# Gunicorn

WSGI HTTP server for Python apps.

## When to Use

- Serving Flask, Django, and other WSGI apps in production
- HTTP hosting behind nginx or a cloud load balancer
- When you need worker tuning beyond the dev server

## Commands

```bash
# Basic serve
gunicorn myapp:app

# 4 workers on all interfaces
gunicorn -w 4 -b 0.0.0.0:8000 myapp:app

# Threaded workers
gunicorn -k gthread --threads 8 -w 2 myapp:app

# Gevent workers for async I/O
gunicorn --worker-class gevent --worker-connections 1000 myapp:app

# Config file
gunicorn -c gunicorn.conf.py myapp:app

# Graceful reload (HUP) and shutdown (TERM)
kill -HUP $(cat /tmp/gunicorn.pid)
kill -TERM $(cat /tmp/gunicorn.pid)
```

## Config Example

```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "gthread"
threads = 8
timeout = 30
max_requests = 1000
max_requests_jitter = 100
graceful_timeout = 30
preload_app = True
```

## Best Practices

- Rule of thumb: (2 * CPU cores) + 1 sync workers
- Use gthread or gevent when apps do blocking I/O
- Set max_requests to recycle workers and prevent leaks
- Put gunicorn behind nginx or a proxy that buffers responses
- Use preload_app only when app code is fork-safe
- Add graceful_timeout so long requests drain on deploy

## Capabilities

### gunicorn-serving
Run WSGI applications with tuned worker configurations.

**Commands:**
- `gunicorn myapp:app`
- `gunicorn -w 4 -b 0.0.0.0:8000 myapp:app`
- `gunicorn -k gthread --threads 8 -w 2 myapp:app`
- `gunicorn -c gunicorn.conf.py myapp:app`
- `gunicorn --worker-class gevent --worker-connections 1000 myapp:app`

**Examples:**
- gunicorn -w 4 --timeout 30 -b 127.0.0.1:8000 myapp:app
- gunicorn -k gthread --threads 4 -w 4 --max-requests 1000 myapp:app
- gunicorn --preload -c gunicorn.conf.py myapp:app

### gunicorn-monitoring
Send signals and check worker health.

**Commands:**
- `kill -HUP $(cat /tmp/gunicorn.pid)`
- `kill -TERM $(cat /tmp/gunicorn.pid)`
- `curl -s http://localhost:8000/health`
- `ps aux | grep gunicorn`

**Examples:**
- kill -HUP 12345
- systemctl reload myapp
- curl -sI http://localhost:8000 | head -1