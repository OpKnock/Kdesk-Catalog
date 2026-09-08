---
trigger: glob
description: "Writes correct async code in Node.js: promises, async/await, error handling, concurrency control with the async library, and streaming. Use when working with node async, promises await, api or when the user mentions node async, promises await, api."
globs: ["**/*.r", "**/*.sh"]
---

Writes correct async code in Node.js: promises, async/await, error handling, concurrency control with the async library, and streaming.

## Agentic Workflow: Read -> Reason -> Act (async)

You are **Async** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `async`
- Domain: Writes correct async code in Node.js: promises, async/await, error handling, concurrency control with the async library, and streaming.
- **node-async**: Control concurrency and build async flows with the async library. — `npm install async`
- **promises-await**: Write and debug modern async/await flows with proper error handling. — `node -e "Promise.all([fetch('https://httpbin.org/get'), fetch('https://httpbin.o`
- Check `knowledge` and `prerequisites: node, npm`

### 2. Reason — think for `async`
- For `node-async`: Control concurrency and build async flows with the async library. — decide which checks to run
- For `promises-await`: Write and debug modern async/await flows with proper error handling. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `async` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `async:0596516c`

# Async (Node.js)

## What this skill does

Applies async patterns in Node.js: promise composition, async/await error handling, concurrency control with the async library, unhandled-rejection discipline, and streaming.

## When to use

- Async code has race conditions or unhandled rejections
- Bounding concurrent API calls to avoid rate limits
- Sequentializing dependent async steps

## Real commands

```bash
npm install async

# Limit concurrency to 2
node -e "const async=require('async'); async.eachLimit([1,2,3,4], 2, (n,cb)=>setTimeout(()=>{console.log(n);cb()},100), ()=>console.log('done'))"

# Parallel fan-out
node -e "const async=require('async'); async.parallel([cb=>cb(null,1),cb=>cb(null,2)], (e,r)=>console.log(r))"

# Sequential steps
node -e "const async=require('async'); async.waterfall([cb=>cb(null,'a'),(x,cb)=>cb(null,x+'b')],(e,r)=>console.log(r))"

# Strict unhandled rejection behavior
node --unhandled-rejections=strict app.js
```

## Concurrency pattern

```js
const { queue } = require('async')
const q = queue(async id => {
  await fetch(`/api/items/${id}`)
}, 3)  // max 3 concurrent
q.push([1, 2, 3, 4, 5])
```

## Testing

- Use Promise.allSettled in tests to assert per-item outcomes
- Run with --unhandled-rejections=strict to surface gaps

## Best practices

- Never mix .then() and await in one flow
- Always attach a catch to top-level async entry points
- Bound concurrency when calling rate-limited APIs

## Capabilities

### node-async
Control concurrency and build async flows with the async library.

**Parameters:**
- `concurrency` (number): Max parallel tasks
- `collection` (string): Array or object to iterate

**Commands:**
- `npm install async`
- `node -e "const async=require('async'); async.eachLimit([1,2,3,4], 2, (n,cb)=>setTimeout(()=>{console.log(n);cb()},100), ()=>console.log('done'))"`
- `node -e "const async=require('async'); async.parallel([cb=>cb(null,1),cb=>cb(null,2)], (e,r)=>console.log(r))"`
- `node -e "const async=require('async'); async.waterfall([cb=>cb(null,'a'),(x,cb)=>cb(null,x+'b')],(e,r)=>console.log(r))"`

**Examples:**
- node -e "const async=require('async'); async.eachOfLimit({a:1,b:2,c:3},1,(v,k,cb)=>cb(),console.log)"
- node -e "const async=require('async'); async.mapLimit([1,2,3,4,5],2,n=>Promise.resolve(n*2),console.log)"
- node -e "const async=require('async'); async.queue(w=>new Promise(r=>setTimeout(r,50)),3).push([1,2,3,4,5,6])"

### promises-await
Write and debug modern async/await flows with proper error handling.

**Parameters:**
- `timeout` (number): Race timeout in ms
- `mode` (string): all, allSettled, race, or any semantics

**Commands:**
- `node -e "Promise.all([fetch('https://httpbin.org/get'), fetch('https://httpbin.org/get')]).then(console.log)"`
- `node --unhandled-rejections=strict app.js`
- `node -e "Promise.allSettled([Promise.resolve(1),Promise.reject(new Error('x'))]).then(r=>console.log(r.map(x=>x.status)))"`
- `node -e "Promise.race([Promise.resolve(1), Promise.reject(new Error('late'))]).catch(e=>console.log('raced', e.message))"`

**Examples:**
- node --unhandled-rejections=strict -e "Promise.reject(new Error('boom'))"
- node -e "Promise.allSettled([Promise.resolve(1),Promise.reject(new Error('e'))]).then(console.log)"
- node -e "(async()=>{const [a,b]=await Promise.all([Promise.resolve(1),Promise.resolve(2)]); console.log(a+b)})()"

## References
- [Node.js async_hooks](https://nodejs.org/api/async_hooks.html)
- [async library](https://caolan.github.io/async/v3/)
- [MDN Using Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
