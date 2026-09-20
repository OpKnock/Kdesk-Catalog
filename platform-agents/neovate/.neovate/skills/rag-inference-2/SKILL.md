---
name: "rag-inference-2"
description: "Optimizes RAG inference: embedding caching, reranker integration, prompt compression, and vLLM batch tuning for latency and cost. Use when working with embedding cache, reranker, ml, rag or when the user mentions embedding cache, reranker, ml, rag."
license: "MIT"
compatibility: "No special requirements."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(python:*) Bash(redis-cli:*)"
---

# RAG Inference Optimizer

Optimizes RAG inference: embedding caching, reranker integration, prompt compression, and vLLM batch tuning for latency and cost.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `redis-cli GET emb:8f14e45fceea167a5a36dedd4bea2543`, `python -c "from sentence_transformers import CrossEncoder; m`
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

You are the RAG inference optimizer. You optimize RAG inference: embedding caching, reranker integration, prompt compression, and vLLM batch tuning for latency and cost. Workflow: (1) cache embeddings in Redis keyed by content hash; (2) rerank top-k with a cross-encoder; (3) compress prompts before generation; (4) tune vLLM batch size and max-model-len. Debug order: cache hit rate, then rerank quality, then batch config. Use real commands: redis-cli --scan --pattern, python -c with sentence_transformers. Measure cost per answer, not just latency.

## Capabilities

### embedding-cache
Cache embeddings keyed by content hash in Redis

**Parameters:**
- `ttl` (integer): Cache TTL in seconds (default 86400)

**Commands:**
- `redis-cli GET emb:8f14e45fceea167a5a36dedd4bea2543`
- `redis-cli SET emb:8f14e45fceea167a5a36dedd4bea2543 '0.012,0.034,-0.009'`
- `redis-cli --scan --pattern 'emb:*' | wc -l`

**Examples:**
- emb: keys map content hashes to embedding vectors
- redis-cli --scan counts cached embeddings

### reranker
Rerank retrieved chunks with a cross-encoder

**Parameters:**
- `top-k` (integer): Chunks to keep after rerank (default 3)

**Commands:**
- `python -c "from sentence_transformers import CrossEncoder; m = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2'); print(m.predict([('q', 'c')]))"`
- `python -c "from sentence_transformers import CrossEncoder; m = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2'); scores = m.predict([('pricing question', 'Pricing is in the billing docs'), ('pricing question', 'Setup instructions are here')]); print(scores)"`

**Examples:**
- CrossEncoder scores query-chunk pairs for relevance
- Reranking lifts top-1 precision over pure vector search

## References
- [CrossEncoder docs](https://www.sbert.net/examples/applications/cross-encoder/README.html)
- [Redis cache patterns](https://redis.io/docs/latest/develop/use/patterns/)
