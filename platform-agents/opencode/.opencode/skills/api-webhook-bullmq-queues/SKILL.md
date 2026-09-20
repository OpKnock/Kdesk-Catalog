---
name: "api-webhook-bullmq-queues"
description: "Builds reliable webhook delivery with queues: BullMQ workers, Redis persistence, dead-letter handling, and delivery monitoring. Use when working with bullmq queues, delivery monitoring or when the user mentions bullmq queues, delivery monitoring."
---

Builds reliable webhook delivery with queues: BullMQ workers, Redis persistence, dead-letter handling, and delivery monitoring.

## Agentic Workflow: Read -> Reason -> Act (api-webhook-bullmq-queues)

You are **Api Webhook Bullmq Queues** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-webhook-bullmq-queues`
- Domain: Builds reliable webhook delivery with queues: BullMQ workers, Redis persistence, dead-letter handling, and delivery monitoring.
- **bullmq-queues**: Queue webhook deliveries with BullMQ — `npm install bullmq ioredis`
- **delivery-monitoring**: Monitor retries and dead letters — `node -e "const {Queue}=require('bullmq'); const q=new Queue('webhook-delivery');`
- Check `knowledge` and `prerequisites: node.js, python, ngrok, redis`

### 2. Reason — think for `api-webhook-bullmq-queues`
- For `bullmq-queues`: Queue webhook deliveries with BullMQ — decide which checks to run
- For `delivery-monitoring`: Monitor retries and dead letters — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-webhook-bullmq-queues` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-webhook-bullmq-queues:512bae15`

# API Webhook v4 - Reliability

Queue-backed webhook delivery.

## What This Skill Does
- Enqueues deliveries as durable jobs
- Retries with backoff in workers
- Dead-letters persistent failures

## When to Use
- High-volume webhook workloads
- At-least-once delivery needs
- Surviving worker crashes

## Real Commands

```bash
npm install bullmq ioredis
node -e "const {Queue}=require('bullmq'); const q=new Queue('webhook-delivery'); q.add('order.created',{id:1}).then(j=>console.log('job',j.id))"
redis-cli LLEN bull:webhook-delivery:wait
```

## Worker Example

```js
const { Worker } = require('bullmq');
new Worker('webhook-delivery', async (job) => {
  await fetch(job.data.url, { method: 'POST', body: JSON.stringify(job.data) });
}, { concurrency: 10 });
```

## Testing
- Kill workers mid-queue and verify recovery
- Simulate endpoint failures into dead letters
- Monitor queue depth during bursts


## Best Practices
- Set job TTLs and max attempts
- Keep payloads small; reference data
- Alert on dead-letter growth

## Capabilities

### bullmq-queues
Queue webhook deliveries with BullMQ

**Parameters:**
- `queue-name` (string): Queue name
- `job` (string): Job type
- `payload` (object): Job data

**Commands:**
- `npm install bullmq ioredis`
- `node -e "const {Queue}=require('bullmq'); const q=new Queue('webhook-delivery'); q.add('order.created',{id:1}).then(j=>console.log('job',j.id))"`
- `node -e "const {Queue}=require('bullmq'); const q=new Queue('webhook-delivery'); q.getJobCounts().then(console.log)"`
- `node worker.js`
- `redis-cli LLEN bull:webhook-delivery:wait`

**Examples:**
- Queue.add enqueues a delivery job
- getJobCounts reports queue state
- redis-cli LLEN inspects the waiting list

### delivery-monitoring
Monitor retries and dead letters

**Commands:**
- `node -e "const {Queue}=require('bullmq'); const q=new Queue('webhook-delivery'); q.getFailed().then(jobs=>console.log('failed',jobs.length))"`
- `redis-cli ZCARD bull:webhook-delivery:failed`
- `npx bull-board`
- `node -e "const {Queue}=require('bullmq'); const q=new Queue('webhook-delivery'); q.obliterate().then(()=>console.log('cleared'))"`

**Examples:**
- -cli --help
- -api --help

## References
- [BullMQ Docs](https://docs.bullmq.io/)
- [Redis Docs](https://redis.io/docs/latest/)
