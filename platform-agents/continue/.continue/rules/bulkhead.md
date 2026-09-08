---
name: "Bulkhead"
description: "Implements bulkhead isolation with opossum (Node.js) and Resilience4j (Java): semaphores, per-dependency pools, and testing. Use when working with opossum node, resilience4j java, verify, api or when the user mentions opossum node, resilience4j java, verify, api."
globs: ["**/*.java", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Implements bulkhead isolation with opossum (Node.js) and Resilience4j (Java): semaphores, per-dependency pools, and testing.

## Agentic Workflow: Read -> Reason -> Act (bulkhead)

You are **Bulkhead** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `bulkhead`
- Domain: Implements bulkhead isolation with opossum (Node.js) and Resilience4j (Java): semaphores, per-dependency pools, and testing.
- **opossum-node**: Add bulkhead limits to Node.js calls with opossum. — `npm install opossum`
- **resilience4j-java**: Configure Resilience4j bulkheads in Java apps. — `mvn dependency:tree | grep resilience4j-bulkhead`
- **verify**: Load-test bulkhead behavior. — `ab -n 1000 -c 100 http://localhost:8080/api/calls`
- Check `knowledge` and `prerequisites: kubectl, mvn, node, npm`

### 2. Reason — think for `bulkhead`
- For `opossum-node`: Add bulkhead limits to Node.js calls with opossum. — decide which checks to run
- For `resilience4j-java`: Configure Resilience4j bulkheads in Java apps. — decide which checks to run
- For `verify`: Load-test bulkhead behavior. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `bulkhead` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Mvn` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `bulkhead:c27ff877`

# Bulkhead

## What this skill does

Implements bulkhead isolation in code: opossum bulkheads for Node.js, Resilience4j bulkheads for Java, and load-test verification that rejected calls fail fast.

## When to use

- Limiting concurrent calls to a dependency in application code
- Protecting a service from slow downstreams
- Adding queueing with bounded size

## Real commands

```bash
# Node.js (opossum)
npm install opossum
node -e "const opossum=require('opossum'); const b=opossum.bulkhead(async()=>42, {maxConcurrent:2}); b.call().then(console.log)"

# Rejection beyond the limit
node -e "const opossum=require('opossum'); const b=opossum.bulkhead(async()=>{await new Promise(r=>setTimeout(r,1000)); return 1},{maxConcurrent:1}); b.call().then(console.log).catch(e=>console.log('rejected', e.message))"

# Java (Resilience4j) metrics
curl -s http://localhost:8080/actuator/metrics/resilience4j.bulkhead.available.concurrent.calls

# Verify with load
ab -n 1000 -c 100 http://localhost:8080/api/calls
```

## Config (resilience4j)

```yaml
resilience4j.bulkhead:
  instances:
    db:
      maxConcurrentCalls: 10
      maxWaitDuration: 100ms
```

## Testing

- Load until rejection rate matches (concurrency - maxConcurrent)
- Assert rejected calls return quickly, not hang

## Best practices

- Size bulkhead = dependency concurrency limit
- Expose rejected.calls metrics and alert on them
- Combine with timeouts so queued calls do not pile up

## Capabilities

### opossum-node
Add bulkhead limits to Node.js calls with opossum.

**Parameters:**
- `max_concurrent` (number): Max concurrent executions
- `queue_size` (number): Max queued executions

**Commands:**
- `npm install opossum`
- `node -e "const opossum=require('opossum'); const b=opossum.bulkhead(async()=>42, {maxConcurrent:2}); b.call().then(console.log)"`
- `node -e "const opossum=require('opossum'); const b=opossum.bulkhead(async()=>{await new Promise(r=>setTimeout(r,1000)); return 1},{maxConcurrent:1}); b.call().then(console.log).catch(e=>console.log('rejected', e.message))"`
- `npm run test`

**Examples:**
- node -e "const opossum=require('opossum'); const b=opossum.bulkhead(async()=>42,{maxConcurrent:2}); Promise.all([b.call(),b.call(),b.call()]).catch(e=>console.log('blocked'))"
- node -e "const opossum=require('opossum'); const b=opossum.bulkhead(async()=>1,{maxConcurrent:1, queue:3, maxQueue:3}); console.log(b.status)"
- node -e "const opossum=require('opossum'); const b=opossum.bulkhead(async()=>1,{maxConcurrent:1}); b.call().then(()=>console.log(b.status.stats.active))"

### resilience4j-java
Configure Resilience4j bulkheads in Java apps.

**Parameters:**
- `max_concurrent` (number): resilience4j bulkhead maxConcurrentCalls
- `wait_timeout` (number): maxWaitDuration

**Commands:**
- `mvn dependency:tree | grep resilience4j-bulkhead`
- `mvn test`
- `curl -s http://localhost:8080/actuator/health`
- `curl -s http://localhost:8080/actuator/metrics/resilience4j.bulkhead.available.concurrent.calls`

**Examples:**
- curl -s http://localhost:8080/actuator/metrics/resilience4j.bulkhead.available.concurrent.calls | jq '.measurements'
- mvn test -Dtest=BulkheadTest
- curl -s http://localhost:8080/actuator/health | jq '.components.resilience4jBulkhead'

### verify
Load-test bulkhead behavior.

**Parameters:**
- `endpoint` (string): Protected endpoint
- `concurrency` (number): Load test concurrency

**Commands:**
- `ab -n 1000 -c 100 http://localhost:8080/api/calls`
- `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/calls`
- `curl -s http://localhost:8080/actuator/metrics/resilience4j.bulkhead.max.allowed.concurrent.calls`
- `kubectl get hpa`

**Examples:**
- ab -n 1000 -c 100 http://localhost:8080/api/calls | grep -E 'Non-2xx|Failed'
- curl -s http://localhost:8080/actuator/metrics/resilience4j.bulkhead.rejected.calls | jq '.measurements'
- watch -n1 'curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/calls'

## References
- [opossum npm](https://github.com/nodeshift/opossum)
- [Resilience4j Bulkhead](https://resilience4j.readme.io/docs/bulkhead)