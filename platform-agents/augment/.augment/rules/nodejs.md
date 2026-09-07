---
type: agent_requested
description: "Develops Node.js backends: npm project setup, debugging, worker threads, dependency auditing, and production runtime management. Use when working with nodejs runtime, nodejs quality, backend or when the user mentions nodejs runtime, nodejs quality, backend."
---

Develops Node.js backends: npm project setup, debugging, worker threads, dependency auditing, and production runtime management.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm init -y`, `npm audit`
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

# Node.js

Backend development on the Node.js runtime.

## When to Use

- HTTP APIs, WebSockets, and real-time services
- CLI tools and automation scripts
- Polyglot teams already using JavaScript/TypeScript

## Commands

```bash
# Project setup
npm init -y
npm install express
npm install --save-dev nodemon typescript

# Run
node server.js
node --watch server.js

# Memory control
node --max-old-space-size=4096 app.js

# Debugging
node --inspect-brk server.js

# Production deps only
npm ci --omit=dev

# Audit and updates
npm audit --audit-level=high
npm audit fix
npm outdated

# Tests
npm test
node --test
```

## HTTP Server

```javascript
const http = require("node:http");

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ ok: true }));
});

server.listen(3000);
```

## Best Practices

- Pin dependency versions and use package-lock.json in VCS
- Run npm audit in CI and fix high+ findings
- Use worker threads or child processes for CPU-heavy work
- Always set a graceful shutdown handler (SIGTERM)
- Use --watch in dev, a process manager in prod
- Enable NODE_ENV=production to skip dev-only work

## Capabilities

### nodejs-runtime
Manage Node.js projects and run scripts.

**Parameters:**
- `script` (string): Script to run
- `flags` (string): Node runtime flags

**Commands:**
- `npm init -y`
- `npm install express`
- `node --version`
- `node --watch server.js`
- `node --max-old-space-size=4096 app.js`

**Examples:**
- npm install --save-dev nodemon typescript
- node --inspect-brk server.js
- npm ci --omit=dev

### nodejs-quality
Audit dependencies and run tests.

**Parameters:**
- `audit-level` (string): low, moderate, high, critical
- `fix` (boolean): Apply audit fixes

**Commands:**
- `npm audit`
- `npm audit fix`
- `npm test`
- `npm outdated`
- `node --test`

**Examples:**
- npm audit --audit-level=high
- npm run lint
- node --test test/

## References
- [Node.js Docs](https://nodejs.org/api/)
- [npm Docs](https://docs.npmjs.com)