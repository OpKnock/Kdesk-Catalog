Start and configure the it monitoring server. Query task and worker state through the it HTTP API. with optional basic auth.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install flower`, `curl http://localhost:5555/api/workers`
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

**Parameters:**
- `port` (integer): Web UI port
- `basic_auth` (string): user:password for the UI
- `address` (string): Bind address

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

**Parameters:**
- `task_id` (string): Celery task UUID
- `task_type` (string): Filter by task name

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

## References
- [Flower Docs](https://flower.readthedocs.io)
- [Flower on PyPI](https://pypi.org/project/flower/)