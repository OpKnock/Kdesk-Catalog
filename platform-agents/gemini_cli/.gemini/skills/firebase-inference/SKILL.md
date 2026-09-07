---
name: "firebase-inference"
description: "Firebase inference server agent. Manages Firebase ML inference server. Use when working with Ml Firebase Inference Server Agent or when the user mentions Ml Firebase Inference Server Agent."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(firebase:*)"
---

# Firebase Inference

Firebase inference server agent. Manages Firebase ML inference server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST http://localhost:8080/v1/predict -H 'Content-Ty`
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

## Instructions

Firebase inference server expert. Call on this agent to set up and operate the Firebase inference server. Verify with `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`, chat completions via `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "firebase", "messages": []}'`, list models with `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`, and probe liveness with `curl -s -o firebase --version --agent firebase-inference`. Failure modes: server down, model not loaded (empty model list), schema drift (400/422); check health, then models, then payload. Cross-check with tooling such as `firebase deploy --only functions` and `firebase ml:model:list`. Report the health code, model IDs, a sample prediction, and errors with fixes.

## Capabilities

### Ml Firebase Inference Server Agent
Firebase inference server agent. Manages Firebase ML inference server.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "firebase", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `firebase --version`

**Examples:**
- firebase deploy --only functions
- firebase functions:shell
- firebase experiments:enable ml
- firebase ml:model:list

## References
- [Firebase Documentation](https://firebase.google.com/docs)
- [curl Documentation](https://curl.se/docs/)
- [jq Manual](https://jqlang.github.io/jq/)
