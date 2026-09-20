Builds concurrent Python services with asyncio: coroutines, task groups, aiohttp clients, timeouts, and semaphore-bounded concurrency.

## Agentic Workflow: Read -> Reason -> Act (async-asyncio-basics)

You are **Async Asyncio Basics** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `async-asyncio-basics`
- Domain: Builds concurrent Python services with asyncio: coroutines, task groups, aiohttp clients, timeouts, and semaphore-bounded concurrency.
- **asyncio-basics**: Run coroutines and tasks on the asyncio event loop. — `python -c "import asyncio; asyncio.run(asyncio.sleep(0.1)); print('ok')"`
- **async-http**: Make concurrent HTTP calls with aiohttp and bound timeouts. — `pip install aiohttp`
- Check `knowledge` and `prerequisites: pip, python`

### 2. Reason — think for `async-asyncio-basics`
- For `asyncio-basics`: Run coroutines and tasks on the asyncio event loop. — decide which checks to run
- For `async-http`: Make concurrent HTTP calls with aiohttp and bound timeouts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `async-asyncio-basics` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `async-asyncio-basics:52baebed`

# Async v2 (Python asyncio)

## What this skill does

Builds concurrent I/O-bound Python services on asyncio: coroutines and tasks, parallel gather, aiohttp clients with timeouts, semaphores for bounded concurrency, and correct shutdown.

## When to use

- A Python service blocks on many HTTP calls that could be parallel
- Replacing threads/process pools with an event loop
- Debugging 'Event loop is closed' or timeout leaks

## Real commands

```bash
# Basic coroutine execution
python -c "import asyncio; asyncio.run(asyncio.sleep(0.1)); print('ok')"

# Parallel execution: 2s of sleeps in ~1s wall time
python -c "import asyncio, time; async def m(): t=time.perf_counter(); await asyncio.gather(asyncio.sleep(1), asyncio.sleep(1)); print(f'{time.perf_counter()-t:.2f}s')"

# aiohttp with total timeout
pip install aiohttp
python -c "import aiohttp, asyncio; async def m(): async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as s: r=await s.get('https://httpbin.org/delay/3'); print(r.status)"
```

## Bounded concurrency

```python
import asyncio, aiohttp

async def fetch_all(urls, limit=10):
    sem = asyncio.Semaphore(limit)
    async with aiohttp.ClientSession() as s:
        async def one(u):
            async with sem:
                async with s.get(u) as r:
                    return r.status
        return await asyncio.gather(*(one(u) for u in urls))
```

## Testing

- Unit-test with pytest-asyncio and asyncio.run(main())
- Verify parallelism by timing concurrent sleeps (max, not sum)

## Best practices

- Prefer asyncio.timeout() context managers over raw wait_for
- Bound concurrency with semaphores for rate-limited APIs
- Do CPU work in executors, never in the event loop

## Capabilities

### asyncio-basics
Run coroutines and tasks on the asyncio event loop.

**Parameters:**
- `tasks` (string): Comma-separated coroutines to gather
- `timeout` (number): asyncio.timeout value in seconds

**Commands:**
- `python -c "import asyncio; asyncio.run(asyncio.sleep(0.1)); print('ok')"`
- `python -c "import asyncio, time; async def m(): t=time.perf_counter(); await asyncio.gather(asyncio.sleep(1), asyncio.sleep(1)); print(f'{time.perf_counter()-t:.2f}s')"`
- `python -m asyncio`
- `python -c "import asyncio; async def f(): return 42; print(asyncio.run(f()))"`

**Examples:**
- python -c "import asyncio; print(asyncio.run(asyncio.gather(*(asyncio.sleep(i/10) for i in range(5)))))"
- python -c "import asyncio; async def f(): return 42; print(asyncio.run(f()))"
- python -c "import asyncio; print(asyncio.get_event_loop_policy().get_event_loop().class_)"

### async-http
Make concurrent HTTP calls with aiohttp and bound timeouts.

**Parameters:**
- `url` (string): Endpoint to call
- `total_timeout` (number): aiohttp.ClientTimeout total seconds
- `concurrency` (number): Concurrent requests via gather/semaphore

**Commands:**
- `pip install aiohttp`
- `python -c "import aiohttp, asyncio; async def m(): async with aiohttp.ClientSession() as s: r=await s.get('https://httpbin.org/get'); print(r.status)"`
- `python -c "import aiohttp, asyncio; async def m(): async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as s: r=await s.get('https://httpbin.org/delay/3'); print(r.status)"`
- `python -c "import aiohttp, asyncio, time; async def m(): t=time.perf_counter(); async with aiohttp.ClientSession() as s: await asyncio.gather(*(s.get('https://httpbin.org/delay/1') for _ in range(5))); print(f'{(time.perf_counter()-t):.2f}s')"`

**Examples:**
- python -c "import aiohttp, asyncio; async def m(): async with aiohttp.ClientSession() as s: r=await s.post('https://httpbin.org/post', json={'a':1}); print(r.status); print((await r.json())['json'])"
- python -c "import aiohttp, asyncio; async def m(): async with aiohttp.ClientSession() as s: await asyncio.gather(*(s.get('https://httpbin.org/get') for _ in range(10)))"
- python -c "import aiohttp; print([k for k in aiohttp.__dict__ if 'Client' in k])"

## References
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [uvloop](https://github.com/MagicStack/uvloop)