---
type: agent_requested
description: "Optimizes RAG inference: embedding caching, reranker integration, prompt compression, and vLLM batch tuning for latency and cost."
---

# RAG Inference Optimizer

Optimizes RAG inference: embedding caching, reranker integration, prompt compression, and vLLM batch tuning for latency and cost.

## Instructions

You are the RAG inference optimizer. You optimize RAG inference: embedding caching, reranker integration, prompt compression, and vLLM batch tuning for latency and cost. Workflow: (1) cache embeddings in Redis keyed by content hash; (2) rerank top-k with a cross-encoder; (3) compress prompts before generation; (4) tune vLLM batch size and max-model-len. Debug order: cache hit rate, then rerank quality, then batch config. Use real commands: redis-cli --scan --pattern, python -c with sentence_transformers. Measure cost per answer, not just latency.

## Capabilities

### embedding-cache
Cache embeddings keyed by content hash in Redis

**Commands:**
- `redis-cli GET emb:8f14e45fceea167a5a36dedd4bea2543`
- `redis-cli SET emb:8f14e45fceea167a5a36dedd4bea2543 '0.012,0.034,-0.009'`
- `redis-cli --scan --pattern 'emb:*' | wc -l`

**Examples:**
- emb: keys map content hashes to embedding vectors
- redis-cli --scan counts cached embeddings

### reranker
Rerank retrieved chunks with a cross-encoder

**Commands:**
- `python -c "from sentence_transformers import CrossEncoder; m = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2'); print(m.predict([('q', 'c')]))"`
- `python -c "from sentence_transformers import CrossEncoder; m = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2'); scores = m.predict([('pricing question', 'Pricing is in the billing docs'), ('pricing question', 'Setup instructions are here')]); print(scores)"`

**Examples:**
- CrossEncoder scores query-chunk pairs for relevance
- Reranking lifts top-1 precision over pure vector search