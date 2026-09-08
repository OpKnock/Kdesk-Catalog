---
name: "vector-db-operations"
description: "Operates vector databases (Chroma, Qdrant, Pinecone, Weaviate) for embeddings: collections, indexing, search, and maintenance. Use when working with chroma ops, qdrant ops, backend or when the user mentions chroma ops, qdrant ops, backend."
---

Operates vector databases (Chroma, Qdrant, Pinecone, Weaviate) for embeddings: collections, indexing, search, and maintenance.

## Agentic Workflow: Read -> Reason -> Act (vector-db-operations)

You are **Vector Db Operations** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `vector-db-operations`
- Domain: Operates vector databases (Chroma, Qdrant, Pinecone, Weaviate) for embeddings: collections, indexing, search, and maintenance.
- **chroma-ops**: Create and query ChromaDB collections. — `pip install chromadb`
- **qdrant-ops**: Operate Qdrant collections via CLI and REST. — `docker run -p 6333:6333 qdrant/qdrant`
- Check `knowledge` and `prerequisites: docker, pip, python`

### 2. Reason — think for `vector-db-operations`
- For `chroma-ops`: Create and query ChromaDB collections. — decide which checks to run
- For `qdrant-ops`: Operate Qdrant collections via CLI and REST. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `vector-db-operations` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `vector-db-operations:6271e6ca`

# Vector DB Operations

Run vector databases for embeddings and similarity search.

## When to Use

- RAG retrieval backends
- Semantic search and deduplication
- Recommendation by embedding proximity
- Anomaly detection on vectorized events

## Concepts

- Collection: named group of vectors with one metric
- Dimension: must match the embedding model output
- Distance: cosine, L2 (euclidean), or inner product
- Payload/metadata: filters applied before or after search
- HNSW: default index algorithm, tunable for speed vs recall

## Chroma Commands

```bash
pip install chromadb

# Create
python -c "import chromadb; c=chromadb.PersistentClient(path='./db'); c.create_collection('docs', metadata={'hnsw:space':'cosine'})"

# Insert
python -c "import chromadb; c=chromadb.PersistentClient(path='./db'); col=c.get_collection('docs'); col.add(ids=['1'], documents=['hello'], metadatas=[{'src':'x.md'}])"

# Search
python -c "import chromadb; c=chromadb.PersistentClient(path='./db'); print(c.get_collection('docs').query(query_texts=['greeting'], n_results=3))"
```

## Qdrant Commands

```bash
docker run -p 6333:6333 qdrant/qdrant

# Create collection
curl -X PUT http://localhost:6333/collections/demo -H "Content-Type: application/json" \
  -d '{"vectors":{"size":384,"distance":"Cosine"}}'

# Search
curl http://localhost:6333/collections/demo/points/search -H "Content-Type: application/json" \
  -d '{"vector":[0.1,0.2],"limit":5}'

# Count
curl http://localhost:6333/collections/demo/points/count -H "Content-Type: application/json" -d '{}'
```

## Best Practices

- Match vector dimension to the embedding model exactly
- Store metadata with every vector; filter before brute force
- Back up persistent storage (Chroma dir / Qdrant volumes)
- Monitor collection growth; re-index when recall degrades
- Test with the exact queries your app will send

## Capabilities

### chroma-ops
Create and query ChromaDB collections.

**Parameters:**
- `collection` (string): Collection name
- `space` (string): Similarity metric: cosine, l2, ip

**Commands:**
- `pip install chromadb`
- `python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); c.create_collection(\"docs\", metadata={\"hnsw:space\":\"cosine\"}); print(\"created\")"`
- `python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); col=c.get_collection(\"docs\"); col.add(ids=[\"1\"], documents=[\"hello world\"], metadatas=[{\"src\":\"x.md\"}]); print(col.count())"`
- `python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); print(c.get_collection(\"docs\").query(query_texts=[\"greeting\"], n_results=3))"`

**Examples:**
- python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); c.delete_collection(\"docs\"); print(\"deleted\")"
- python -c "import chromadb; c=chromadb.PersistentClient(path=\"./db\"); print([x.name for x in c.list_collections()])"

### qdrant-ops
Operate Qdrant collections via CLI and REST.

**Parameters:**
- `collection` (string): Collection name
- `dimension` (integer): Vector dimension

**Commands:**
- `docker run -p 6333:6333 qdrant/qdrant`
- `curl -s http://localhost:6333/collections`
- `curl -s -X PUT http://localhost:6333/collections/demo -H "Content-Type: application/json" -d "{\"vectors\":{\"size\":384,\"distance\":\"Cosine\"}}"`
- `curl -s http://localhost:6333/collections/demo/points/count -H "Content-Type: application/json" -d "{}"`

**Examples:**
- curl -s "http://localhost:6333/collections/demo/points/search" -H "Content-Type: application/json" -d "{\"vector\":[0.1,0.2],\"limit\":5}"
- curl -s http://localhost:6333/collections/demo

## References
- [ChromaDB Docs](https://docs.trychroma.com)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
