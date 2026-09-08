---
name: "async-retry"
description: "Implements resilient retry strategies with tenacity (Python) and async-retry (Node.js): backoff, jitter, bounded retries, and bail conditions. Use when working with python tenacity, node async retry, api or when the user mentions python tenacity, node async retry, api."
---

Implements resilient retry strategies with tenacity (Python) and async-retry (Node.js): backoff, jitter, bounded retries, and bail conditions.

## Agentic Workflow: Read -> Reason -> Act (async-retry)

You are **Async Retry** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `async-retry`
- Domain: Implements resilient retry strategies with tenacity (Python) and async-retry (Node.js): backoff, jitter, bounded retries, and bail conditions.
- **python-tenacity**: Add retry logic to Python async calls with tenacity. — `pip install tenacity`
- **node-async-retry**: Wrap Node.js async functions with async-retry. — `npm install async-retry`
- Check `knowledge` and `prerequisites: node, npm, npx, pip`

### 2. Reason — think for `async-retry`
- For `python-tenacity`: Add retry logic to Python async calls with tenacity. — decide which checks to run
- For `node-async-retry`: Wrap Node.js async functions with async-retry. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `async-retry` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `async-retry:c3af4901`

# Async Retry

## What this skill does

Adds production-grade retry behavior to async code: tenacity for Python, async-retry for Node.js. Covers exponential backoff, full jitter, bounded retries, retry-on-specific exceptions, and tests.

## When to use

- Transient failures (connection resets, 503s) should not crash jobs
- A third-party API occasionally times out but succeeds on retry
- Retries must not amplify load during an outage (jitter matters)

## Real commands

```bash
pip install tenacity
npm install async-retry
```

## Python example

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(stop=stop_after_attempt(4), wait=wait_exponential_jitter(initial=0.5, max=8))
async def fetch():
    async with aiohttp.ClientSession() as s:
        async with s.get("https://httpbin.org/status/500") as r:
            r.raise_for_status()
            return await r.json()
```

## Node example

```js
const retry = require('async-retry')
const fetchOrders = async () => {
  return retry(async bail => {
    const res = await fetch('https://httpbin.org/status/500')
    if (res.status === 404) bail(new Error('not found'))  // do not retry
    if (!res.ok) throw new Error('retryable')
    return res.json()
  }, { retries: 3, minTimeout: 200, factor: 2, randomize: true })
}
```

## Testing

- Mock failures N times then success; assert call count equals N+1
- Assert non-retryable errors (4xx) are not retried

## Best practices

- Never retry non-idempotent writes without dedupe keys
- Cap attempts and total elapsed time
- Add jitter to avoid thundering herds
- Respect the upstream Retry-After header

## Capabilities

### python-tenacity
Add retry logic to Python async calls with tenacity.

**Parameters:**
- `attempts` (number): Maximum retry attempts
- `backoff` (string): fixed, exponential, or random backoff
- `retry_on` (string): Exception types or predicates to retry on

**Commands:**
- `pip install tenacity`
- `python -c "from tenacity import retry, wait_exponential, stop_after_attempt; print('ok')"`
- `python -m pytest tests/test_retry.py -k retry`
- `python -m unittest discover -s tests`

**Examples:**
- python -c "from tenacity import retry, stop_after_attempt, wait_exponential; print(retry.__module__)"
- pytest tests/test_retry.py -x
- python -m pip install tenacity==8.2.3

### node-async-retry
Wrap Node.js async functions with async-retry.

**Parameters:**
- `retries` (number): Number of retry attempts
- `minTimeout` (number): Minimum backoff in ms
- `factor` (number): Exponential backoff factor

**Commands:**
- `npm install async-retry`
- `npm install --save-dev mocha`
- `npx mocha test/retry.test.js`
- `node -e "const retry=require('async-retry'); retry(async()=>{throw new Error('x')},{retries:2}).catch(e=>console.log('gave up', e.message))"`

**Examples:**
- npm init -y && npm install async-retry
- node -e "const retry=require('async-retry'); retry(()=>Promise.resolve(42),{retries:3}).then(console.log)"
- npx mocha --reporter spec test/retry.test.js

## References
- [tenacity](https://tenacity.readthedocs.io/en/latest/)
- [async-retry](https://github.com/vercel/async-retry)
- [Azure Retry Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
