Operates vector databases (Chroma, Qdrant, Pinecone, Weaviate) for embeddings: collections, indexing, search, and maintenance.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install chromadb`, `docker run -p 6333:6333 qdrant/qdrant`
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