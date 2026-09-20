---
trigger: glob
description: "Builds retrieval-augmented generation pipelines: chunking, embeddings, vector search, reranking, and grounded answer generation."
globs: ["**/*.go", "**/*.py", "**/*.r", "**/*.sh"]
---

# Rag Pipeline

Builds retrieval-augmented generation pipelines: chunking, embeddings, vector search, reranking, and grounded answer generation.

## Instructions

# RAG Pipeline

Build retrieval-augmented generation pipelines.

## When to Use

- Answering questions from private or changing document sets
- Grounding LLM output in verified source material
- Reducing hallucinations in summarization and Q&A features
- Handling content that is too large for the model context window

## Pipeline Stages

1. Ingestion: parse documents, split into chunks
2. Embedding: map chunks to vectors
3. Indexing: store vectors with metadata in a vector DB
4. Retrieval: query the index by similarity
5. Reranking: refine top-k with a cross-encoder
6. Generation: answer with retrieved chunks as context

## Commands

```bash
# Install tools
pip install chromadb sentence-transformers langchain
ollama pull nomic-embed-text

# Create a collection
python -c "import chromadb; c=chromadb.PersistentClient(path='./db'); c.create_collection('docs'); print('ok')"

# Query the index
python -c "import chromadb; c=chromadb.PersistentClient(path='./db'); col=c.get_collection('docs'); r=col.query(query_texts=['how to deploy'], n_results=5); print(r)"

# Inspect count
python -c "import chromadb; c=chromadb.PersistentClient(path='./db'); print(c.get_collection('docs').count())"
```

## Best Practices

- Chunk by semantic boundaries (sections), not fixed sizes only
- Store metadata (source, date, page) with every chunk
- Set the LLM temperature low and instruct: cite only retrieved facts
- Rerank with a cross-encoder when retrieval quality matters
- Evaluate with a golden set of Q/A pairs before launch
- Embed query and docs with the same model

## Capabilities

### vector-indexing
Index documents into vector stores with embedding models.

**Commands:**
- `pip install chromadb sentence-transformers`
- `python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); c.create_collection(\"docs\"); print(\"ok\")"`
- `ollama pull nomic-embed-text`
- `python -c "from sentence_transformers import SentenceTransformer; m=SentenceTransformer(\"all-MiniLM-L6-v2\"); print(m.encode([\"hi\"]).shape)"`

**Examples:**
- python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); col=c.get_collection(\"docs\"); print(col.count())"
- ollama list

### rag-querying
Retrieve context and generate grounded answers.

**Commands:**
- `python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); col=c.get_collection(\"docs\"); r=col.query(query_texts=[\"how to deploy\"], n_results=5); print(r)"`
- `npx llamaindex-cli`
- `pip install langchain`
- `python -c "from langchain.vectorstores import Chroma; print(\"ok\")"`

**Examples:**
- python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); print([m[\"metadatas\"] for m in [c.get_collection(\"docs\").query(query_texts=[\"pricing\"], n_results=3)]])"
- curl -s http://localhost:8000/query -d "{\"q\":\"refund policy\"}"
