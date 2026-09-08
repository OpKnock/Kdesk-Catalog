Configures and exposes the Dramatiq task queue dashboard for inspecting workers, brokers, and message flow in real time.

## Agentic Workflow: Read -> Reason -> Act (dramatiq-dashboard)

You are **dramatiq-dashboard** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `dramatiq-dashboard`
- Domain: Configures and exposes the Dramatiq task queue dashboard for inspecting workers, brokers, and message flow in real time.
- **dashboard-serving**: Mount and serve the Dramatiq dashboard from a WSGI/ASGI app. — `pip install dramatiq[watch]`
- **dashboard-metrics**: Query worker and queue state through the dashboard API. — `curl http://localhost:8000/dashboard/api/workers`
- Check `knowledge` and `prerequisites: gunicorn, pip, python, redis-cli`

### 2. Reason — think for `dramatiq-dashboard`
- For `dashboard-serving`: Mount and serve the Dramatiq dashboard from a WSGI/ASGI app. — decide which checks to run
- For `dashboard-metrics`: Query worker and queue state through the dashboard API. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `dramatiq-dashboard` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Gunicorn` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `dramatiq-dashboard:c372d260`

# Dramatiq Dashboard

Visualize and monitor a Dramatiq broker from a web dashboard.

## When to Use

- Watching queue depth and worker utilization in dev
- Debugging stalled messages and delayed queues
- Providing ops teams a read-only view of the task system
- Verifying that workers registered all expected actors

## Setup

```bash
pip install dramatiq[watch] dramatiq-dashboard
```

## Mounting

```python
# dashboard.py
from dramatiq_dashboard import Dashboard
from dramatiq_dashboard.__main__ import make_dashboard_app

app = make_dashboard_app(broker, middleware=[...])
```

## Commands

```bash
# Serve with gunicorn
gunicorn -b 0.0.0.0:8000 dashboard:app

# Serve with uvicorn
uvicorn dashboard:app --reload

# Query workers via the API
curl http://localhost:8000/dashboard/api/workers
curl -s http://localhost:8000/dashboard/api/workers | python -m json.tool

# Inspect the broker queues
curl http://localhost:8000/dashboard/api/broker/queues

# Raw broker inspection
redis-cli llen dramatiq:default
redis-cli zrange dramatiq:delayed 0 -1
```

## Best Practices

- Protect the dashboard behind auth in shared environments
- Mount on a separate port or path from the public API
- Watch the delayed set for messages stuck on backoff
- Pair the dashboard with worker CLI logging for correlation
- Use the API endpoints in scripts for alerting on queue growth

## Capabilities

### dashboard-serving
Mount and serve the Dramatiq dashboard from a WSGI/ASGI app.

**Parameters:**
- `host` (string): Bind host
- `port` (integer): Bind port

**Commands:**
- `pip install dramatiq[watch]`
- `gunicorn dashboard:app`
- `uvicorn dashboard:app --reload`
- `python dashboard.py`
- `curl http://localhost:8000/dashboard`

**Examples:**
- gunicorn -b 0.0.0.0:8000 dashboard:app
- uvicorn dashboard:app --port 9000
- python -m dashboard

### dashboard-metrics
Query worker and queue state through the dashboard API.

**Parameters:**
- `endpoint` (string): Dashboard API path
- `format` (string): Output format: json or table

**Commands:**
- `curl http://localhost:8000/dashboard/api/workers`
- `curl http://localhost:8000/dashboard/api/broker/queues`
- `redis-cli llen dramatiq:default`
- `redis-cli info clients`

**Examples:**
- curl -s http://localhost:8000/dashboard/api/workers | python -m json.tool
- redis-cli zrange dramatiq:delayed 0 -1

## References
- [Dramatiq Docs](https://dramatiq.io/)
- [Dramatiq Dashboard](https://dramatiq-dashboard.readthedocs.io)