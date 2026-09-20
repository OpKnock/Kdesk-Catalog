---
name: "flower"
description: "Start and configure the it monitoring server. Query task and worker state through the it HTTP API. with optional basic auth."
type: knowledge
triggers: ["flower", "flower-server", "flower-api"]
---

# flower

Start and configure the it monitoring server. Query task and worker state through the it HTTP API. with optional basic auth.

## Instructions

# Flower

Real-time web monitor for Celery.

## When to Use

- Observing task states (started, succeeded, failed) live
- Checking worker heartbeats and load per process
- Inspecting queue lengths without touching Redis directly
- Alerting from the REST API in scripts

## Commands

```bash
pip install flower

# Start on port 5555
celery -A proj flower --port=5555

# Bind all interfaces
celery -A proj flower --address=0.0.0.0

# Require auth
celery -A proj flower --basic_auth=user:password

# Persist state across restarts
celery -A proj flower --persistent --state-dir=/tmp/flower

# API endpoints
curl http://localhost:5555/api/workers
curl http://localhost:5555/api/tasks
curl http://localhost:5555/api/queues/length
curl http://localhost:5555/api/task/info/<task_id>
```

## Best Practices

- Always enable basic_auth when exposing beyond localhost
- Use --persistent to retain state across redeploys
- Point alerts at /api/queues/length and /api/workers
- Correlate task UUIDs from app logs to the UI
- Run Flower as a managed process, not an ad-hoc terminal

## Capabilities

### flower-server
Start and configure the Flower monitoring server.

**Commands:**
- `pip install flower`
- `celery -A proj flower --port=5555`
- `celery -A proj flower --basic_auth=user:password`
- `celery -A proj flower --url_prefix=flower`
- `celery -A proj flower --broker=redis://localhost:6379/0`

**Examples:**
- celery -A proj flower --port=5555 --address=0.0.0.0
- celery -A proj flower --basic_auth=admin:s3cret
- celery -A proj flower --persistent --state-dir=/tmp/flower

### flower-api
Query task and worker state through the Flower HTTP API.

**Commands:**
- `curl http://localhost:5555/api/workers`
- `curl http://localhost:5555/api/tasks`
- `curl http://localhost:5555/api/tasks?task_type=tasks.send_email`
- `curl http://localhost:5555/api/queues/length`
- `curl http://localhost:5555/api/task/info/{task_id}`

**Examples:**
- curl -s http://localhost:5555/api/workers | python -m json.tool
- curl -s http://localhost:5555/api/queues/length
- curl -s http://localhost:5555/api/tasks | jq -r "keys[]" | head
