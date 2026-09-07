Expert reference covering exponential backoff with tenacity, curl retry flags, Retry-After handling, and jitter to survive cascading failures.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl --retry 5 --retry-delay 2 --retry-all-errors --retry-co`
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

# Retry Pattern

Expert skill for resilient retries with exponential backoff.

## What this skill does

- Retries transient failures a bounded number of times
- Grows delays exponentially with jitter
- Honors Retry-After headers from rate-limited APIs

## When to use

- Downstream services return 503/429 or refuse connections
- Batch jobs should survive brief network blips
- Rate-limited third-party APIs need polite retries

## Real commands

```bash
# curl: 5 attempts, 2s base delay, retry on everything including connection refused
curl --retry 5 --retry-delay 2 --retry-all-errors --retry-connrefused https://api.your-app.test/health

# Honoring Retry-After from a 429
curl -si https://api.your-app.test/rate-limited | grep -i retry-after

# Python tenacity: 3 attempts, exponential 1s..10s
pip install tenacity
```

## Python retry

```python
from tenacity import retry, stop_after_attempt, wait_exponential, wait_jitter

@retry(stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=1, max=10) + wait_jitter(1, 3),
       retry_on=lambda e: isinstance(e, ConnectionError))
def call_downstream():
    return requests.get("https://api.your-app.test/health", timeout=5)
```

## Testing

```bash
# Simulate flakiness with a proxy like toxiproxy, then:
curl --retry 5 --retry-delay 2 --retry-all-errors -s https://api.your-app.test/health
```

## Best practices

- Always bound retries: stop_after_attempt or a deadline
- Add jitter so retries do not synchronize across clients
- For 429s, sleep on Retry-After when present, else back off
- Do not retry 4xx validation errors: they will never succeed

## Capabilities

### exponential-backoff
Retry failing calls with exponential backoff, jitter, and Retry-After

**Parameters:**
- `max_attempts` (integer): Total attempts before giving up
- `backoff_multiplier` (integer): Base delay in seconds for exponential growth
- `jitter` (boolean): Randomize delay to avoid thundering herd

**Commands:**
- `curl --retry 5 --retry-delay 2 --retry-all-errors --retry-connrefused https://api.your-app.test/health`
- `pip install tenacity`
- `curl -si https://api.your-app.test/rate-limited | grep -i retry-after`
- `curl --retry 3 --retry-connrefused -s https://api.your-app.test/data -o data.json`

**Examples:**
- curl --retry 5 --retry-delay 2 --retry-all-errors https://api.your-app.test/health
- python -c 'from tenacity import retry, stop_after_attempt, wait_exponential; print(retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))(__import__("requests").get).__name__)'
- curl -si https://api.your-app.test/429 | grep -i retry-after

## References
- [Azure retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
- [tenacity docs](https://tenacity.readthedocs.io/en/latest/)