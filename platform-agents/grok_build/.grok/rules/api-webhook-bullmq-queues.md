Builds reliable webhook delivery with queues: BullMQ workers, Redis persistence, dead-letter handling, and delivery monitoring.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install bullmq ioredis`, `node -e "const {Queue}=require('bullmq'); const q=new Queue(`
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