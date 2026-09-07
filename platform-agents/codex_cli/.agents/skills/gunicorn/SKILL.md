---
name: "gunicorn"
description: "Serves Python WSGI apps in production with gunicorn: workers, preloading, timeouts, and systemd/container integration. Use when working with gunicorn serving, gunicorn monitoring, backend or when the user mentions gunicorn serving, gunicorn monitoring, backend."
license: "MIT"
compatibility: "Requires gunicorn, kill. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(gunicorn:*) Bash(kill:*) Bash(ps:*)"
---

Serves Python WSGI apps in production with gunicorn: workers, preloading, timeouts, and systemd/container integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gunicorn myapp:app`, `kill -HUP $(cat /tmp/gunicorn.pid)`
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

**Parameters:**
- `workers` (integer): Number of worker processes
- `bind` (string): Host:port to bind
- `worker-class` (string): sync, gthread, gevent, eventlet

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

**Parameters:**
- `pid-file` (string): Path to pidfile
- `signal` (string): Signal to send: HUP, TERM, INT

**Commands:**
- `kill -HUP $(cat /tmp/gunicorn.pid)`
- `kill -TERM $(cat /tmp/gunicorn.pid)`
- `curl -s http://localhost:8000/health`
- `ps aux | grep gunicorn`

**Examples:**
- kill -HUP 12345
- systemctl reload myapp
- curl -sI http://localhost:8000 | head -1

## References
- [Gunicorn Docs](https://docs.gunicorn.org/en/stable/)
- [Gunicorn Deployment](https://docs.gunicorn.org/en/stable/deploy.html)
