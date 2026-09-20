---
name: "rag-pipeline"
description: "Builds retrieval-augmented generation pipelines: chunking, embeddings, vector search, reranking, and grounded answer generation. Use when working with vector indexing, rag querying, backend or when the user mentions vector indexing, rag querying, backend."
license: "MIT"
compatibility: "Requires npx, ollama, pip, python."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(npx:*) Bash(ollama:*) Bash(pip:*) Bash(python:*)"
---

Builds retrieval-augmented generation pipelines: chunking, embeddings, vector search, reranking, and grounded answer generation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install chromadb sentence-transformers`, `python -c "import chromadb; c=chromadb.PersistentClient(path`
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

**Parameters:**
- `collection` (string): Vector collection name
- `model` (string): Embedding model id

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

**Parameters:**
- `query` (string): Natural language query
- `top-k` (integer): Number of results to retrieve

**Commands:**
- `python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); col=c.get_collection(\"docs\"); r=col.query(query_texts=[\"how to deploy\"], n_results=5); print(r)"`
- `npx llamaindex-cli`
- `pip install langchain`
- `python -c "from langchain.vectorstores import Chroma; print(\"ok\")"`

**Examples:**
- python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); print([m[\"metadatas\"] for m in [c.get_collection(\"docs\").query(query_texts=[\"pricing\"], n_results=3)]])"
- curl -s http://localhost:8000/query -d "{\"q\":\"refund policy\"}"

## References
- [RAG Guide (OpenAI)](https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts)
- [LangChain Docs](https://python.langchain.com/docs/)
- [ChromaDB Docs](https://docs.trychroma.com)
